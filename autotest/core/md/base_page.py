import json
import operator
import os
import re
import time

import allure
from datetime import datetime

from selenium.webdriver import Keys
from colorama import init
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from utils.logger import get_test_name, configure_logging

from utils.exception import *
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException,
    NoSuchElementException,
    JavascriptException
)

init(autoreset=True)

class BasePage:
    # ==================================================================================================================

    def __init__(self, driver):
        self.driver = driver
        self.test_name = get_test_name()
        self.logger = configure_logging(self.test_name)
        self.default_timeout = 30
        self.default_page_load_timeout = 180
        self.actions = ActionChains(driver)

    # ==================================================================================================================

    def take_screenshot(self, filename=None):
        """Fayl nomiga vaqt va test nomini qo'shib, screenshot saqlash."""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = self.test_name if self.test_name != "unknown_test" else "default"
        if filename:
            filename = f"{test_name}_{timestamp}_{filename}"
        else:
            filename = f"{test_name}_{timestamp}"
        screenshot_dir = "screenshot_dir"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        screenshot_path = os.path.join(screenshot_dir, f"{filename}.png")
        self.driver.save_screenshot(screenshot_path)
        self.logger.info(f"Screenshot saved at {screenshot_path}")
        allure.attach.file(screenshot_path, name="Error Screenshot", attachment_type=allure.attachment_type.PNG)

    # ==================================================================================================================

    def _wait_for_async_operations(self, timeout=None, retry_interval=0.5):
        """Sahifadagi asinxron operatsiyalar tugashini kutish."""

        timeout = timeout or self.default_timeout
        end_time = time.time() + timeout
        start_time = time.time()

        async_check_script = """
            return (
                document.readyState === 'complete' &&
                (typeof jQuery !== 'undefined' ? jQuery.active === 0 : true) &&
                window.performance
                    .getEntriesByType('resource')
                    .filter(r => !r.responseEnd && 
                        (r.initiatorType === 'fetch' || r.initiatorType === 'xmlhttprequest'))
                    .length === 0 &&
                !document.querySelector('html.ng-scope.ng-isolate-scope')
            );
        """

        while time.time() < end_time:
            try:
                if self.driver.execute_script(async_check_script):
                    # elapsed_time = time.time() - start_time
                    # self.logger.debug(f"Asinxron operatsiyalar yakunlandi ({elapsed_time:.2f}s)")
                    return True
                else:
                    elapsed_time = time.time() - start_time
                    self.logger.debug(f"Asinxron operatsiyalar davom etmoqda, qayta tekshirilmoqda... ({elapsed_time:.2f}s)")
            except JavascriptException as e:
                message = f"Asinxron tekshiruvda JavaScript xatosi."
                self.logger.error(f"{message}: {str(e)}")
                raise JavaScriptError(message, original_error=e)

            time.sleep(retry_interval)

        message = f"Asinxron operatsiyalar {timeout}s ichida tugallanmadi"
        self.logger.error(message)
        raise LoaderTimeoutError(message)

    # ==================================================================================================================

    def _wait_for_block_ui_absence(self, timeout=None, retry_interval=0.5):
        """Block UI yo'qolishini kutish. JavaScript va DOM orqali Block UI holatini tekshiradi."""

        timeout = timeout or self.default_timeout
        end_time = time.time() + timeout
        start_time = time.time()

        block_ui_selector = "div.block-ui-container"

        block_ui_script = """
            var blockUI = document.querySelector(arguments[0]);
            if (!blockUI) return true;  // Agar element yo'q bo'lsa, allaqachon yo'qolgan
            var style = window.getComputedStyle(blockUI);
            return (
                style.display === 'none' || 
                style.visibility === 'hidden' || 
                style.opacity === '0' || 
                blockUI.offsetWidth === 0 || 
                blockUI.offsetHeight === 0
            );
        """

        while time.time() < end_time:
            elapsed_time = time.time() - start_time
            try:
                # Block UI elementi DOM ichida mavjudmi?
                block_ui_elements = self.driver.find_elements(By.CSS_SELECTOR, block_ui_selector)
                if not block_ui_elements:
                    # self.logger.debug(f"Block UI elementi DOM ichida topilmadi ({elapsed_time:.2f}s).")
                    return True  # Agar element umuman yo‘q bo‘lsa, yuklanish tugagan.

                # Agar element mavjud bo‘lsa, uni yashirin yoki yo‘qligini tekshiramiz
                js_result = self.driver.execute_script(block_ui_script, block_ui_selector)
                if js_result:
                    # self.logger.debug(f"Block UI nol o‘lchamda - yuklanish tugadi ({elapsed_time:.2f}s).")
                    return True  # Agar element mavjud bo‘lsa, lekin ko‘rinmasa - yuklanish tugagan.
                else:
                    self.logger.debug(f"Block UI hali ham ko‘rinmoqda, kutish davom etmoqda... ({elapsed_time:.2f}s)")

            except JavascriptException as e:
                message = f"Block UI tekshirishda JavaScript xatosi: {str(e)}"
                self.logger.warning(f"{message}: locator={block_ui_selector}: {str(e)}")
                raise JavaScriptError(message, locator=block_ui_selector, original_error=e)

            time.sleep(retry_interval)

        # Agar timeout tugasa va hali ham bloklangan bo‘lsa, xatolik chiqariladi
        total_time = time.time() - start_time
        message = f"Block UI {timeout}s ichida yo'qolmadi (Jami vaqt: {total_time:.2f}s)"
        self.logger.error(message)
        raise LoaderTimeoutError(message, locator=block_ui_selector)

    # ==================================================================================================================

    def _check_spinner_absence(self, timeout=None, retry_interval=0.5):
        timeout = timeout or self.default_timeout
        end_time = time.time() + timeout
        start_time = time.time()

        block_ui_locators = [
            (By.CSS_SELECTOR, "div.block-ui-container"),
            (By.CSS_SELECTOR, "div.block-ui-overlay"),
            (By.CSS_SELECTOR, "div.block-ui-message-container"),
            (By.CSS_SELECTOR, "img[src='assets/img/loading.svg']")
        ]

        while time.time() < end_time:
            elapsed_time = time.time() - start_time

            try:
                is_visible = False

                for by, locator in block_ui_locators:
                    elements = self.driver.find_elements(by, locator)
                    for element in elements:
                        if element.is_displayed():
                            style = self.driver.execute_script("""
                                var style = window.getComputedStyle(arguments[0]);
                                return {
                                    display: style.display,
                                    opacity: style.opacity,
                                    visibility: style.visibility,
                                    width: style.width,
                                    height: style.height
                                };
                            """, element)

                            width = float(style["width"].replace('px', ''))
                            height = float(style["height"].replace('px', ''))

                            if style["display"] != "none" and style["opacity"] != "0" and \
                                    width > 0 and height > 0:
                                is_visible = True
                                self.logger.debug(f"{locator}: hali ham ko‘rinib turibdi. ({elapsed_time:.2f}s)")
                                break

                    if is_visible:
                        break

                if not is_visible:
                    # self.logger.debug(f"block-ui-container yo‘qoldi ({elapsed_time:.2f}s)")
                    return True

            except JavascriptException as e:
                message = "Spinner tekshirishda JavaScript xatosi."
                self.logger.warning(f"{message}: {locator}: {str(e)}")
                raise JavaScriptError(message, locator, e)

            time.sleep(retry_interval)

        message = f"Spinner {timeout}s ichida yo‘qolmadi!"
        self.logger.error(message)
        raise LoaderTimeoutError(message, locator)

    # ==================================================================================================================

    def _wait_for_all_loaders(self, timeout=None):
        """Sahifaning to'liq barqaror holatga kelishini kutish."""

        timeout = timeout or self.default_page_load_timeout
        errors = []

        try:
            self._wait_for_async_operations(timeout)
        except (JavaScriptError, LoaderTimeoutError) as e:
            message = f"_wait_for_async_operations xatosi: {str(e)}"
            self.logger.warning(message)
            errors.append(message)

        try:
            self._wait_for_block_ui_absence(timeout)
        except (JavaScriptError, LoaderTimeoutError) as e:
            message = f"_wait_for_block_ui_absence xatosi: {str(e)}"
            self.logger.warning(message)
            errors.append(message)

        try:
            self._check_spinner_absence(timeout)
        except (JavaScriptError, LoaderTimeoutError) as e:
            message = f"_check_spinner_absence xatosi: {str(e)}"
            self.logger.warning(message)
            errors.append(message)

            full_error_message = "\n".join(errors)
            self.logger.error(f"Barcha yuklanish funksiyalari muvaffaqiyatsiz tugadi.\n{full_error_message}")
            self.take_screenshot("timeout_error")
            raise LoaderTimeoutError(message=full_error_message)

    # ==================================================================================================================

    def _click(self, element, locator=None, retry=False, error_message=True):
        """Oddiy click urinishi"""
        page_name = self.__class__.__name__
        try:
            element.click()
            self.logger.info(f"⏺ {page_name}: {'Retry ' if retry else ''}Click: {locator}")
            return True
        except WebDriverException:
            if error_message:
                self.logger.warning(f"❗{'Retry ' if retry else ''}Click ishlamadi: {locator}")
            return False

    # ==================================================================================================================

    def _click_js(self, element, locator=None, retry=False):
        """JavaScript orqali majburiy bosish."""
        page_name = self.__class__.__name__
        try:
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info(f"⏺ {page_name}: {'Retry ' if retry else ''}JS-Click: {locator}")
            return True
        except WebDriverException:
            self.logger.warning(f"❗{'Retry ' if retry else ''}JS-Click ishlamadi: {locator}")
            return False

    # ==================================================================================================================

    def _scroll_to_element(self, element, locator, timeout=None):
        """Elementga scroll qilish."""

        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        try:
            if element is None:
                raise ElementNotFoundError(message="Element topilmadi, scroll qilish imkonsiz", locator=locator)
            if element.is_displayed():
                return element

            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", element)

            if element.is_displayed():
                self.logger.info(f"{page_name}: Scroll muvaffaqiyatli bajarildi: {locator}")
                return element

        except NoSuchElementException as e:
            message = f"Element topilmadi, scroll ishlamadi."
            self.logger.warning(f"{page_name}: {message}: {locator}: {str(e)}")
            raise ElementNotFoundError(message, locator, e)

        except StaleElementReferenceException as e:
            message = f"Element DOM da yangilandi (scroll)."
            self.logger.warning(f"{page_name}: {message}: {locator}: {str(e)}")
            raise ElementStaleError(message, locator, e)

        except TimeoutException as e:
            message = f"Element {timeout}s ichida sahifada ko'rinmadi (scroll)."
            self.logger.warning(f"{page_name}: {message}: {locator}: {str(e)}")
            raise ScrollError(message, locator, e)

        except JavascriptException as je:
            message = f"JavaScript scrollIntoView xatoligi (scroll)."
            self.logger.warning(f"{page_name}: {message}: {locator}: {str(je)}")
            raise JavaScriptError(message, locator, je)

        except Exception as e:
            message = f"Scroll qilishda kutilmagan xatolik."
            self.logger.warning(f"{page_name}: {message}: {locator}: {str(e)}")
            raise ElementInteractionError(message, locator, e)

    # ==================================================================================================================

    def wait_for_element(self, locator, timeout=None, wait_type="presence", error_message=True, screenshot=False):
        """
        Umumiy kutish funksiyasi:
        - "presence" => DOMda mavjudligini kutadi
        - "visibility" => Ko‘rinishini kutadi
        - "clickable" => Bosiladigan holatga kelishini kutadi
        """

        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        wait_types = {
            "presence": EC.presence_of_element_located,
            "visibility": EC.visibility_of_element_located,
            "clickable": EC.element_to_be_clickable
        }

        if wait_type not in wait_types:
            raise ValueError(
                f"Notog'ri wait_type: '{wait_type}'. Faqat 'presence', 'visibility', yoki 'clickable' bo'lishi mumkin.")

        try:
            element = WebDriverWait(self.driver, timeout).until(wait_types[wait_type](locator))
            return element

        except StaleElementReferenceException as e:
            message = f"Element {wait_type} kutishida DOM yangilandi."
            if error_message:
                self.logger.warning(f"{page_name}: {message}: {locator}: {str(e)}")
            raise ElementStaleError(message, locator, e)

        except TimeoutException as e:
            message = f"Element {timeout}s ichida {wait_type} shartiga yetmadi."
            if error_message:
                self.logger.warning(f"{page_name}: {message}: {locator}: {str(e)}")
            if screenshot:
                self.take_screenshot(f"{page_name}_{screenshot}")

            if wait_type == "visibility":
                raise ElementVisibilityError(message, locator, e)
            elif wait_type == "clickable":
                raise ElementNotClickableError(message, locator, e)
            else:  # presence
                raise ElementNotFoundError(message, locator, e)

        except Exception as e:
            message = f"Element {wait_type} kutishda kutilmagan xato."
            if error_message:
                self.logger.warning(f"{page_name}: {message}: {locator}: {str(e)}")
            raise ElementInteractionError(message, locator, e)

    # ==================================================================================================================

    def click_checkbox(self, locator, state=True):
        """Checkbox holatini kerakli qiymatga o‘zgartiradi."""

        caller_chain = self._get_caller_chain()
        self.logger.debug(f"{caller_chain}: {locator}")

        try:
            self._wait_for_all_loaders()
            element_presence = self.wait_for_element(locator, wait_type="presence")
            self._scroll_to_element(element_presence, locator)

            start_state = element_presence.is_selected()
            self.logger.info(f"Checkbox start_state: {start_state}")

            if start_state != state:
                self._click_js(element_presence, locator)
                self.logger.info(f"Checkbox {'yoqildi' if state else 'o‘chirildi'}: {locator}")
            else:
                self.logger.info(f"Checkbox avvaldan {'yoqilgan' if state else 'o‘chirilgan'}: {locator}")

            element_presence = self.wait_for_element(locator, wait_type="presence")
            final_state = element_presence.is_selected()
            self.logger.info(f"Checkbox final_state: {final_state}")

            if final_state == state:
                return True
            else:
                self.logger.warning(f"Checkbox state_error: {start_state} != {final_state}")
                return False

        except Exception as e:
            message = "Checkbox holatini o‘zgartirishda xatolik yuz berdi."
            self.logger.warning(f"{message}: {locator}: {str(e)}")
            raise

    # ==================================================================================================================

    def click_drag_and_drop(self, source, target):
        source = self.wait_for_element(source, wait_type="clickable")
        target = self.wait_for_element(target, wait_type="clickable")

        self.actions.drag_and_drop(source, target).perform()

    # ==================================================================================================================

    def _get_caller_chain(self, depth=5):
        import inspect

        try:
            stack = inspect.stack()
        except Exception:
            return "UnknownPage → stack_error"

        # ⚙️ Filtrlab tashlanadigan funksiyalar va modullar
        ignored_names = {
            '<module>', 'pytest_pyfunc_call', 'runpy', '__call__',
            '_call_with_frames_removed', '_run_code', '_run_module_as_main',
            'async_run', 'run', 'inner', '_multicall', '_hookexec'
        }
        ignored_modules = {'pytest', 'importlib', 'runpy'}

        # 🔹 Page class nomini aniqlaymiz
        try:
            frame_self = stack[1].frame.f_locals.get("self", None)
            page_name = frame_self.__class__.__name__ if frame_self else "UnknownPage"
        except Exception:
            page_name = "UnknownPage"

        # 🔍 Stack ichidan funksiyalarni yig‘amiz
        chain = []
        for frame in stack[1:]:  # stack[0] = _get_caller_chain o‘zi
            try:
                func = frame.function
                module = frame.frame.f_globals.get('__name__', '')

                if func.startswith("test_"):
                    continue
                if func in ignored_names or any(m in module for m in ignored_modules):
                    continue

                chain.append(func)
                if len(chain) >= depth:
                    break
            except Exception:
                continue  # muammo bo‘lsa, bu frame’ni tashlab ketamiz

        function_chain = " → ".join(reversed(chain))
        return f"{page_name} → {function_chain if chain else 'no_function_trace'}"


    def click(self, locator, retries=3, retry_delay=2, _click=True, _click_retry=True, _click_js=True):
        """Elementni bosish funksiyasi"""

        caller_chain = self._get_caller_chain()
        self.logger.debug(f"{caller_chain}: {locator}")

        time.sleep(1)
        attempt = 0
        while attempt < retries:
            try:
                if _click:
                    self._wait_for_all_loaders()
                    element_dom = self.wait_for_element(locator, wait_type="presence")
                    self._scroll_to_element(element_dom, locator)
                    self.wait_for_element(locator, wait_type="visibility")
                    element_clickable = self.wait_for_element(locator, wait_type="clickable")
                    if element_clickable and self._click(element_clickable, locator):
                        return True

                if _click_retry:
                    time.sleep(retry_delay)
                    self.logger.info("Retry Click sinab ko'riladi...")
                    self._wait_for_all_loaders()
                    element_clickable = self.wait_for_element(locator, wait_type="clickable")
                    if element_clickable and self._click(element_clickable, locator, retry=True):
                        return True

                if _click_js:
                    time.sleep(retry_delay)
                    self.logger.info("JS Click sinab ko'riladi...")
                    self._wait_for_all_loaders()
                    element_dom = self.wait_for_element(locator, wait_type="presence")
                    if element_dom and self._click_js(element_dom, locator):
                        return True

            except (ElementStaleError, ScrollError, JavaScriptError) as e:
                self.logger.warning(f"Qayta urinish ({attempt + 1}/{retries}): {str(e)}")
                time.sleep(retry_delay)

            except Exception as e:
                self.logger.warning(f"Kutilmagan xatolik: {str(e)}: {locator}")
                self.take_screenshot(f"{__class__.__name__.lower()}_click_error")
                raise

            attempt += 1

        message = f"Element barcha usullar bilan bosilmadi ({attempt}/{retries})"
        self.logger.warning(f"{message}: {locator}")
        self.take_screenshot(f"{__class__.__name__.lower()}_click_all_error")
        raise

    # ==================================================================================================================

    def wait_for_element_visible(self, locator, retries=3, retry_delay=1):
        """Elementni ko'rinishini kutish funksiyasi"""

        caller_chain = self._get_caller_chain()
        self.logger.debug(f"{caller_chain}: {locator}")

        time.sleep(1)
        attempt = 0
        while attempt < retries:
            try:
                self._wait_for_all_loaders()
                element_dom = self.wait_for_element(locator, wait_type="presence")
                self._scroll_to_element(element_dom, locator)
                element = self.wait_for_element(locator, wait_type="visibility")

                if element:
                    self.logger.info(f"⏺ Element topildi: {locator}")
                    return element

            except (ElementStaleError, ScrollError, JavaScriptError) as e:
                self.logger.warning(f"{e.message}, qayta urinish ({attempt + 1}/{retries})")
                time.sleep(retry_delay)

            except Exception as e:
                self.logger.warning(f"Kutilmagan xatolik: {str(e)}: {locator}")
                self.take_screenshot(f"{__class__.__name__.lower()}_visible_error")
                raise

            attempt += 1

        message = f"Element barcha usullar bilan topilmadi ({attempt}/{retries})"
        self.logger.warning(f"{message}: {locator}")
        self.take_screenshot(f"{__class__.__name__.lower()}_visible_all_error")
        raise

    # ==================================================================================================================

    def _wait_for_presence_all(self, locator, timeout=None, visible_only=False):
        """Elementlar ro'yxatini kutish funksiyasi."""

        caller_chain = self._get_caller_chain()
        self.logger.debug(f"{caller_chain}: {locator}")

        timeout = timeout or self.default_timeout

        try:
            elements = WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))
            if visible_only:
                elements = [el for el in elements if el.is_displayed()]
            return elements

        except StaleElementReferenceException as e:
            message = "Elementlar ro'yhati DOM da yangilandi."
            self.logger.warning(f"{message}: {locator}")
            raise ElementStaleError(message, locator, e)

        except TimeoutException as e:
            message = "Elementlar ro'yhati topilmadi."
            self.logger.warning(f"{message}: {locator}")
            raise ElementNotFoundError(message, locator, e)

        except Exception as e:
            message = "Elementlarni ro'yhatini qidirishda kutilmagan xato."
            self.logger.error(f"{message}: {str(e)}")
            raise

    # ==================================================================================================================

    def _wait_for_invisibility_of_element(self, element, timeout=None, error_message=None):
        """Element ni ko'rinmas bo'lishini kutish."""

        timeout = timeout or self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element(element))
        except TimeoutException as e:
            if error_message:
                self.logger.error(f"Element interfeys dan yo'qolmadi: {e}")
            return False

    # ==================================================================================================================

    def _wait_for_invisibility_of_locator(self, locator, timeout=None, raise_error=True):
        """Locator ko'rinmas bo'lishini kutish funksiyasi."""

        caller_chain = self._get_caller_chain()
        self.logger.debug(f"{caller_chain}: {locator}")

        timeout = timeout or self.default_timeout

        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
            return True

        except StaleElementReferenceException as e:
            message = "Element DOM da yangilandi."
            self.logger.warning(f"{message}: {locator}")
            raise ElementStaleError(message, locator, e)

        except TimeoutException as e:
            message = "Element ko'rinmas bo'lmadi."
            self.logger.warning(f"{message}: {locator}")
            if raise_error:
                raise ElementVisibilityError(message, locator, e)
            else:
                return False

        except Exception as e:
            message = "Element kutishda kutilmagan xato."
            self.logger.warning(f"{message}: {locator}: {str(e)}")
            raise ElementInteractionError(message, locator, e)

    # ==================================================================================================================

    def input_text(self, locator, text=None, retries=3, retry_delay=2, check=False, get_value=False):
        """Element topib, matn kiritish funksiyasi"""

        caller_chain = self._get_caller_chain()
        self.logger.debug(f"{caller_chain}: {locator}")

        attempt = 0
        while attempt < retries:
            try:
                self._wait_for_all_loaders()
                element_dom = self.wait_for_element(locator, wait_type="presence")
                self._scroll_to_element(element_dom, locator)

                if get_value:
                    value = element_dom.get_attribute("value")
                    self.logger.info(f"Input: get_value -> '{value}'")
                    return value

                if text:
                    element_clickable = self.wait_for_element(locator, wait_type="clickable")
                    element_clickable.clear()
                    element_clickable.send_keys(text)
                    self.logger.info(f"Input: send_key -> '{text}'")

                if check:
                    check_text = self.driver.execute_script("return arguments[0].value;", element_dom)
                    self.logger.info(f"Check Input Value: -> '{check_text}'")
                    if check_text != text:
                        self.driver.execute_script(f"arguments[0].value = '{text}';", element_dom)
                return True

            except ElementStaleError:
                self.logger.warning(f"Input yangilandi, qayta urinish ({attempt + 1})...")
                attempt += 1
                time.sleep(retry_delay)

            except Exception as e:
                self.logger.error(f"Matn kiritishda kutilmagan xatolik: {str(e)}: {locator}")
                self.take_screenshot(f"{__class__.__name__.lower()}_input_error")
                raise

    # ==================================================================================================================

    def clear_element(self, locator, retries=3, retry_delay=2):
        """ Elementni tozalash."""

        caller_chain = self._get_caller_chain()
        self.logger.debug(f"{caller_chain}: {locator}")

        attempt = 0
        while attempt < retries:
            try:
                self._wait_for_all_loaders()
                element_dom = self.wait_for_element(locator, wait_type="presence")
                self._scroll_to_element(element_dom, locator)
                element = self.wait_for_element(locator, wait_type="clickable")

                # Element readonly yoki disable emasligini tekshirish
                if not element.is_enabled() or element.get_attribute("readonly"):
                    self.logger.warning(f"Elementni tozalab bo‘lmadi, u readonly yoki disabled! {locator}")
                    return False

                # Elementning ko‘rinadiganligini tekshirish
                if not element.is_displayed():
                    self.logger.warning(f"Element ko‘rinmayapti, JavaScript orqali tozalaymiz: {locator}")
                    self.driver.execute_script("arguments[0].value = '';", element)
                    return True

                element.clear()
                self.logger.info(f"Element muvaffaqiyatli tozalandi: {locator}")
                return True

            except ElementStaleError:
                self.logger.warning(f"Element yangilandi, qayta urinish ({attempt + 1})...")
                attempt += 1
                time.sleep(retry_delay)

            except Exception as e:
                self.logger.error(f"Element textni o‘chirishda kutilmagan xato: {str(e)}")
                raise

        message = f"Element {retries} marta urinishdan keyin ham tozalanmadi: {locator}"
        self.logger.warning(message)
        raise ElementInteractionError(message)

    # ==================================================================================================================

    def get_text(self, locator, retries=3, retry_delay=1, clean=False):
        """Elementning matnini olish."""

        self.logger.debug(f"{self._get_caller_chain()}: {locator}")

        attempt = 0
        while attempt < retries:
            try:
                self._wait_for_all_loaders()
                element_dom = self.wait_for_element(locator, wait_type="presence")
                self._scroll_to_element(element_dom, locator)
                element = self.wait_for_element(locator, wait_type="visibility")

                text = element.text

                if text == '':
                    self.logger.warning(f"Element ko‘rindi, lekin bo‘sh holatda: {locator}")
                    return False

                if clean:
                    self.logger.info(f"Element: before clean text -> <str'{text}'>")
                    text = text.replace(" ", "").replace("\u00A0", "").strip()
                    self.logger.info(f"Element: after clean text -> <str'{text}'>")

                self.logger.info(f"Element: return text -> <str'{text}'>")
                return text

            except (StaleElementReferenceException, ElementStaleError):
                self.logger.warning(f"Element yangilandi, qayta urinish ({attempt + 1})...")
                attempt += 1
                time.sleep(retry_delay)

            except Exception as e:
                self.logger.error(f"Element matnini olishda xato: {str(e)}")
                raise

        self.logger.error(f"Barcha urinishlarda ham text olinmadi.")
        return False

    # ==================================================================================================================

    def get_numeric_value(self, locator):
        """Elementdan raqamli qiymatni ajratib olish va float formatiga o'tkazish."""

        self.logger.debug(f"{self._get_caller_chain()}: {locator}")

        text = self.get_text(locator)

        if not text:
            self.logger.error(f"Element topilmadi yoki text yo‘q -> '{text}'")
            raise ElementNotFoundError(locator=locator)

        text = text.strip()

        # Faqat raqamlar, nuqta va vergulni qoldiramiz
        numeric_value = re.sub(r'[^0-9.,]', '', text)

        # Agar vergul bor bo'lsa, uni nuqtaga almashtiramiz
        if ',' in numeric_value and '.' in numeric_value:
            numeric_value = numeric_value.replace(',', '')  # `1,234.56` -> `1234.56`
        elif ',' in numeric_value:
            numeric_value = numeric_value.replace(',', '.')  # `1.234,56` -> `1234.56`

        # Bir nechta nuqta bo‘lsa, noto‘g‘ri format deb hisoblaymiz
        if numeric_value.count('.') > 1:
            self.logger.error(f"Noto'g'ri raqam formati -> '{text}'")
            return None

        try:
            result = float(numeric_value) if numeric_value else None  # `None` bo‘lsa, `None` qaytadi
            self.logger.info(f"Element -> Float -> '{result}'")
            return result

        except ValueError as e:
            self.logger.error(f"Float ga o'tkazishda xato - {str(e)}")
            return None

    # ==================================================================================================================

    def cut_url(self):
        current_url = self.driver.current_url

        try:
            base_path = current_url.split('#')[0]  # https://smartup.online
            after_hash = current_url.split('#')[1]  # /!6lybkj03t/anor/mdeal/return/return_list

            # '/!' dan keyingi birinchi '/' gacha bo'lgan ID ni olish
            user_id = after_hash.split('/!')[1].split('/')[0]  # 6lybkj03t

            return f"{base_path}#/!{user_id}/"

        except Exception as e:
            self.logger.error(f"cut_url URL ni kesishda xatolik: {str(e)}", exc_info=True)
            raise

    # ==================================================================================================================

    def switch_window(self, direction, url=None):
        """
        Brauzer oynalar (tabs/windows) o‘rtasida o'tishni amalga oshiradi.

        Parameters:
            direction (str):
                - "prepare" -> hozirgi oynalar ro‘yxatini eslab qoladi
                - "back"    -> avvalgi oynaga o‘tadi (joriy oynani yopadi)
                - "forward" -> yangi oyna ochilganini aniqlaydi va unga o‘tadi
                - "new"     -> yangi tab ochadi va URL'ga o'tadi
        """
        try:
            current_window_id = self.driver.current_window_handle
            self.logger.debug(f"Joriy oyna ID: {current_window_id}")

            if direction == "prepare":
                self._saved_handles = self.driver.window_handles.copy()
                self.logger.debug(f"Oynalar ro'yxati saqlandi: {self._saved_handles}")
                return

            elif direction == "back":
                handles = self.driver.window_handles
                self.driver.close()
                self.driver.switch_to.window(handles[-2])
                target_window_id = handles[-2]
                self.logger.info(f"Avvalgi oynaga o'tilmoqda: {current_window_id} -> {target_window_id}")

            elif direction == "forward":
                saved_handles = getattr(self, '_saved_handles', [])
                self.logger.debug("Yangi oynaning ochilishini kutish boshlandi...")

                new_window_id = None
                for i in range(20):  # 0.5s * 20 = 10s
                    time.sleep(1)
                    handles_now = self.driver.window_handles
                    new_ids = list(set(handles_now) - set(saved_handles))
                    self.logger.debug(f"Tekshiruv {i + 1}: handles = {handles_now}")
                    if new_ids:
                        new_window_id = new_ids[0]
                        self.logger.info(f"⏺ Yangi oyna topildi: {new_window_id}")
                        break

                if not new_window_id:
                    self.logger.warning("Yangi oyna topilmadi, oxirgi oynaga o‘tilmoqda.")
                    new_window_id = self.driver.window_handles[-1]

                self.driver.switch_to.window(new_window_id)
                self.logger.info(f"Yangi oynaga o'tilmoqda: {current_window_id} -> {new_window_id}")

            elif direction == "new" and url:
                handles_before = self.driver.window_handles.copy()
                self.driver.execute_script("window.open('');")
                time.sleep(1)
                new_handles = self.driver.window_handles
                new_ids = list(set(new_handles) - set(handles_before))
                target_window_id = new_ids[0] if new_ids else new_handles[-1]
                self.driver.switch_to.window(target_window_id)
                self.driver.get(url)
                self.logger.info(f"url bo'yicha yangi oyna ochildi: {current_window_id} -> {target_window_id} | URL: {url}")

            else:
                raise Exception(f"Noto‘g‘ri direction: {direction}")

            time.sleep(2)
            if self._wait_for_all_loaders():
                self.logger.info(f"direction='{direction}' bo‘yicha oynaga muvaffaqiyatli o‘tildi")
                return True

        except LoaderTimeoutError:
            self.logger.error(f"{direction} oynaga o‘tish uchun vaqt tugadi")
            self.take_screenshot(f"switch_{direction}_timeout_error")
            raise

        except Exception as e:
            self.logger.error(f"{direction} oynaga o‘tishda xato: {str(e)}")
            self.take_screenshot(f"switch_{direction}_error")
            raise

    # ==================================================================================================================

    def check_file_and_status_code(self, url_part, code=200, comparison="==", log=False, document_type=None, timeout=10):
        """
        Performance log orqali sahifa (yoki berilgan turdagi fayl) yuklanishining status kodini solishtiradi.

        Parametrlar:
        - url_part: URLning ichida bo'lishi kerak bo'lgan qism
        - code: qaysi status code bilan solishtirilsin (masalan: 200, 404, 500)
        - comparison: solishtirish turi: "==", "!=", ">", ">=", "<", "<="
        - log: True bo'lsa, barcha Network.responseReceived loglar yoziladi
        - document_type: faqat ma'lum turdagi fayllarni tekshiradi
        - timeout: kutish vaqti (sekundlarda)
        """
        compare_ops = {
            "==": operator.eq,
            "!=": operator.ne,
            ">": operator.gt,
            ">=": operator.ge,
            "<": operator.lt,
            "<=": operator.le
        }

        if comparison not in compare_ops:
            raise ValueError(f"Noto'g'ri comparison: {comparison}. Faqat: {list(compare_ops.keys())}")

        start_time = time.time()
        last_error = None

        while time.time() - start_time < timeout:
            try:
                logs = self.driver.get_log("performance")

                if log:
                    self.logger.debug("📊 URL orqali performance log tekshirilmoqda...")

                for entry in reversed(logs):
                    try:
                        message = json.loads(entry["message"])["message"]
                        if message["method"] != "Network.responseReceived":
                            continue

                        response = message["params"]["response"]
                        url = response.get("url", "")
                        status = response.get("status")
                        resource_type = message["params"].get("type")

                        if log:
                            self.logger.debug(f"{status} → {resource_type} → {url}")

                        # document_type bo'lsa, tekshiramiz
                        if document_type and resource_type != document_type:
                            continue

                        if url_part in url:
                            self.logger.info(f"✅ Topildi: {status} → {resource_type} → {url}")
                            if compare_ops[comparison](status, code):
                                return True
                            else:
                                last_error = f"❌ Status mos emas: {status} {comparison} {code}"
                                continue

                    except Exception as e:
                        self.logger.warning(f"⚠️ Logda xatolik: {e}")
                        continue

                time.sleep(0.5)  # Yangi log'lar yozilishini kutamiz

            except Exception as e:
                last_error = f"❌ Performance logni o'qishda xatolik: {str(e)}"
                continue

        raise Exception(last_error or f"{url_part} bo'yicha so'rov {timeout} sekund ichida topilmadi")

    # ==================================================================================================================

    def refresh_page(self):
        """Joriy sahifani yangilash."""

        caller_chain = self._get_caller_chain()
        self.logger.debug(f"{caller_chain}")

        try:
            self.driver.refresh()
            if self._wait_for_all_loaders():
                self.logger.info("Sahifa muvaffaqiyatli yangilandi")
                return True

        except LoaderTimeoutError:
            self.logger.error("Sahifa yangilangandan so'ng to'liq yuklanmadi")
            self.take_screenshot("refresh_window_timeout_error")
            raise

        except Exception as e:
            self.logger.error(f"Sahifani yangilashda xato: {str(e)}")
            self.take_screenshot("refresh_page_error")
            raise

    # ==================================================================================================================

    def _is_choose_dropdown_option(self, input_locator, element_text):
        input_element = self.wait_for_element(input_locator, wait_type="visibility")
        selected_text = input_element.get_attribute("value")
        if selected_text == element_text:
            self.logger.info(f"Option avvaldan tanlangan: {selected_text}")
            return True
        else:
            self.logger.info(f"Input tozalanmoqda...")
            self.clear_element(input_locator)
            return False

    # ==================================================================================================================

    def click_options(self, input_locator, options_locator, element_text, scroll=30, screenshot=True):
        """
        Dropdown bilan ishlash uchun funksiya.
        options_locator = (By.XPATH, '//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

        """
        caller_chain = self._get_caller_chain()
        self.logger.debug(f"{caller_chain}: {element_text} - {input_locator}")

        try:
            # 1-qadam: Avvaldan tanlanganligini tekshirish
            if self._is_choose_dropdown_option(input_locator, element_text):
                return True

            # 2-qadam: Dropdown ochish uchun inputga click qilish
            element_clickable = self.wait_for_element(input_locator, wait_type="clickable")

            # SCROLL: Input elementni sahifada ko‘rinadigan qilamiz
            try:
                self._scroll_to_element(element_clickable, input_locator)
            except Exception as e:
                self.logger.warning(f"Scroll qilishda muammo bo‘ldi: {str(e)}")

            self._click(element_clickable, input_locator)

            # 3-qadam: Optionlar yuklanishini kutish
            self.logger.info("Optionlar yuklanmoqda...")
            try:
                options = self._wait_for_presence_all(options_locator, visible_only=True)
            except ElementNotFoundError:
                self.logger.warning("Optionlar DOM da topilmadi!")
                if self._is_choose_dropdown_option(input_locator, element_text):
                    return True  # DOMda yo‘q, ammo allaqachon tanlangan
                raise  # DOMda yo‘q va tanlanmagan → xatoni qayta chiqarish

            # Agar ro‘yxat bo‘sh bo‘lsa
            if not options:
                self.logger.warning("Optionlar ro‘yxati bo‘sh (visible_only=True)")
                if self._is_choose_dropdown_option(input_locator, element_text):
                    return True  # bo‘sh ro‘yxat, lekin allaqachon tanlangan

            # 4-qadam: Option ichidan qidirib topish va bosish
            if self._find_and_click_option(element_text, options, options_locator):
                if self._check_dropdown_closed(options_locator):
                    return True

            # Agar topilmasa scroll orqali qidirish
            self.logger.info(f"{element_text} topilmadi. Scroll orqali qidirilmoqda...")
            dropdown_container = self._find_visible_container(options_locator)

            for attempt in range(scroll):
                self.driver.execute_script("arguments[0].scrollTop += arguments[0].offsetHeight;", dropdown_container)
                time.sleep(0.5)

                options = self._wait_for_presence_all(options_locator, visible_only=True)
                if self._find_and_click_option(element_text, options, options_locator):
                    if self._check_dropdown_closed(options_locator):
                        return True

                # Scroll tugaganligini aniqlash
                current_scroll = self.driver.execute_script("return arguments[0].scrollTop;", dropdown_container)
                max_scroll = self.driver.execute_script(
                    "return arguments[0].scrollHeight - arguments[0].clientHeight;", dropdown_container
                )
                if current_scroll >= max_scroll:
                    self.logger.info(f"Scroll oxiriga yetildi.")
                    break

            # Option topilmasa xatolik
            message = f"'{element_text}' option scroll dan so‘ng ham topilmadi"
            self.logger.warning(message)
            raise ElementNotFoundError(message, options_locator)

        except ElementNotFoundError as e:
            message = f"ElementNotFoundError - {str(e)}"
            self.logger.error(message)
            if screenshot:
                self.take_screenshot(f"{__class__.__name__.lower()}_click_options_not_found_error")
            raise

        except Exception as e:
            message = f"Kutilmagan xatolik - {str(e)}"
            self.logger.error(message)
            self.take_screenshot(f"{__class__.__name__.lower()}_click_options_error")
            raise

    # ==================================================================================================================

    def _find_and_click_option(self, element, options, options_locator):
        """Element topish va bosish funksiyasi

        Params:
            element: kerakli element matni
            options: elementlar ro'yxati
            options_locator: umumiy locator (retry uchun)
            any_option: True bo‘lsa, birinchi uchragan elementni bosadi
        """
        element_str = str(element).strip()

        for option in options:
            for _ in range(3):
                option_text = option.text.strip()
                if option_text:
                    break
                self.logger.warning(f"Option text topilmadi, qayta uriniladi...")
                time.sleep(1)

            if option_text == element_str:
                self.logger.info(f"Element topildi: '{option_text}', click qilinadi...")
                if self._click(option, options_locator) or self._click(option, options_locator, retry=True):
                    return True
        return False

    # ==================================================================================================================

    def _check_dropdown_closed(self, options_locator, retry_count=3):
        """Dropdown yopilganligini tekshirish."""

        self._wait_for_all_loaders()

        # Agar dropdown allaqachon yopilgan bo‘lsa, qaytib ketish
        if self._wait_for_invisibility_of_locator(options_locator, timeout=2, raise_error=False):
            self.logger.info(f"Dropdown muvaffaqiyatli yopildi")
            return True

        for attempt in range(retry_count):
            try:
                self.logger.info(f"Dropdown yopilmadi, urinish {attempt + 1}/{retry_count}")
                self.logger.info("Sahifani bosh joyiga bosiladi")
                self.driver.execute_script("document.body.click();")
                if self._wait_for_invisibility_of_locator(options_locator, timeout=1, raise_error=False):
                    self.logger.info("Dropdown muvaffaqiyatli yopildi (Sahifani bosh joyiga bosish bilan)")
                    return True

                self.logger.info("Dropdown yopilmadi, ESCAPE bosiladi")
                body = self.wait_for_element((By.TAG_NAME, 'body'), wait_type="presence")
                body.send_keys(Keys.ESCAPE)
                if self._wait_for_invisibility_of_locator(options_locator, timeout=1, raise_error=False):
                    self.logger.info("Dropdown muvaffaqiyatli yopildi (ESCAPE bosish bilan)")
                    return True

            except (ElementNotFoundError, ElementStaleError) as ee:
                self.logger.warning(f"ESCAPE bosishda xatolik: {str(ee)}")
                continue

            except ElementVisibilityError as eve:
                self.logger.warning(f"Dropdown yopilmadi! {str(eve)}")
                continue

        self.logger.error(f"Dropdown yopilmadi ({retry_count} marta urinishdan keyin ham).")
        self.take_screenshot(f"{self.__class__.__name__.lower()}_dropdown_close_error")
        return False

    # ==================================================================================================================

    def _find_visible_container(self, options_locator, timeout=None):
        """Dropdown uchun ko'rinadigan konteynerni topish."""

        timeout = timeout or self.default_timeout

        possible_container_selectors = [
            "//div[contains(@class, 'hint-body')]",
            "//div[contains(@class, 'dropdown-menu')]",
            "//div[contains(@class, 'select-dropdown')]",
            f"{options_locator[1]}/ancestor::div[contains(@class, 'hint')]",
            f"{options_locator[1]}/ancestor::div[contains(@class, 'dropdown')]",
        ]

        try:
            for selector in possible_container_selectors:
                try:
                    containers = self._wait_for_presence_all((By.XPATH, selector), timeout)

                    for container in containers:
                        try:
                            if container.is_displayed():
                                elements_inside = container.find_elements(By.XPATH, ".//*")
                                self.logger.info(f"Tanlangan konteyner: '{selector}', elementlar soni: {len(elements_inside)}")
                                return container
                        except StaleElementReferenceException:
                            self.logger.warning(f"StaleElementReferenceException: '{selector}' qayta yuklanmoqda")
                            continue

                except TimeoutException:
                    self.logger.warning(f"Timeout kutish: '{selector}' topilmadi")
                    continue

            message = f"Ko'rinadigan dropdown konteyner topilmadi"
            self.logger.error(message)
            raise ElementNotFoundError(message, locator=(By.XPATH, " | ".join(possible_container_selectors)))

        except Exception as e:
            message = f"Konteyner qidirishda kutilmagan xato"
            self.logger.error(f"{message}: {str(e)}")
            self.take_screenshot(f"{__class__.__name__.lower()}_dropdown_error")
            raise

    # ==================================================================================================================

    def find_row_and_click(self, element_name, timeout=5, retries=3, xpath_pattern=None, limit_and_search=True,
                           click=True, _click=True, _click_retry=True, checkbox=False):
        """Jadvaldagi qatorni topish va ustiga bosish funksiyasi."""

        # caller_chain = self._get_caller_chain()
        # self.logger.debug(f"{caller_chain}: Jadval qatori qidirilmoqda: {element_name}")

        timeout = timeout or self.default_timeout

        if not xpath_pattern:
            xpath_pattern = ("//div[contains(@class, 'tbl')]//div[contains(@class, 'tbl-row')]"
                             "//div[contains(@class, 'tbl-cell') and normalize-space(text())='{}']")

        row_locator = (By.XPATH, xpath_pattern.format(element_name))
        limit_change_button = (By.XPATH, '//button[@class="btn btn-default rounded-0 ng-binding"]')
        limit_option = (By.XPATH, f'//button[@class="btn btn-default rounded-0 ng-binding"]/following-sibling::div/a[4]')
        checkbox_locator = (By.XPATH, f"//div[contains(@class, 'tbl-row') and .//div[text()='{element_name}']]//span")
        search_input = (By.XPATH, '//b-grid-controller//input[@type="search"]')

        limit_raised = False
        search_used = False

        attempt = 0
        while attempt < retries:
            self._wait_for_all_loaders()
            try:
                try:
                    elements = self._wait_for_presence_all(row_locator, timeout)
                except ElementNotFoundError:
                    if limit_and_search:
                        self.logger.info(f"'{element_name}' topilmadi.")
                        if not limit_raised:
                            self.logger.info(f"'{element_name}' topilmadi, jadval limiti oshirilmoqda...")
                            self._click(self.wait_for_element(limit_change_button, wait_type="clickable"))
                            self._click(self.wait_for_element(limit_option, wait_type="clickable"))
                            self.logger.info("Limit oshirildi.")
                            limit_raised = True
                            continue

                        elif not search_used:
                            self.logger.warning(f"'{element_name}' topilmadi. Qidiruvga berilmoqda...")
                            element = self.wait_for_element(search_input, wait_type="clickable")
                            if element:
                                element.clear()
                                element.send_keys(element_name)
                                element.send_keys(Keys.RETURN)
                            search_used = True
                            continue

                        else:
                            message = f"{element_name} topilmadi, Limit va Qidiruv da ham"
                            self.logger.error(message)
                            raise ElementNotFoundError(message, row_locator)
                    raise
                self._scroll_to_element(elements[0], row_locator)

                if click:
                    if self.click(row_locator, _click=_click, _click_retry=_click_retry):
                        return True

                if checkbox:
                    element_dom = self.wait_for_element(checkbox_locator, wait_type="presence")
                    if element_dom and self._click_js(element_dom, checkbox_locator):
                        return True

            except (ElementStaleError, JavaScriptError) as e:
                self.logger.warning(f"{str(e)}, qayta urinish ({attempt + 1}/{retries})")
                time.sleep(2)

            except Exception as e:
                self.logger.error(f"Kutilmagan xatolik: {str(e)}")
                self.take_screenshot(f"{__class__.__name__.lower()}_find_row_error")
                raise

            attempt += 1

        message = f"Element barcha usullar bilan bosilmadi ({attempt}/{retries})"
        self.logger.error(f"{message}: {row_locator}")
        self.take_screenshot(f"{__class__.__name__.lower()}_click_row_error")
        raise

    # ==================================================================================================================