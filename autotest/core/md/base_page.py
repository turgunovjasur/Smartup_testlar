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

from utils.exception import (
    ElementInteractionError,
    ElementNotFoundError,
    ElementStaleError,
    ElementNotClickableError,
    ScrollError,
    LoaderTimeoutError,
    ElementVisibilityError,
    JavaScriptError
)
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException,
    NoSuchElementException,
    JavascriptException
)

init(autoreset=True)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.test_name = get_test_name()
        self.logger = configure_logging(self.test_name)
        self.default_timeout = 30
        self.default_page_load_timeout = 60
        self.actions = ActionChains(driver)

    # Screenshot -------------------------------------------------------------------------------------------------------

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

    # Halper function --------------------------------------------------------------------------------------------------

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
                    elapsed_time = time.time() - start_time
                    self.logger.debug(f"Asinxron operatsiyalar yakunlandi ({elapsed_time:.2f}s)")
                    return True
                else:
                    elapsed_time = time.time() - start_time
                    self.logger.debug(f"Asinxron operatsiyalar davom etmoqda, qayta tekshirilmoqda... ({elapsed_time:.2f}s)")
            except JavascriptException as js_err:
                message = f"Asinxron tekshiruvda JavaScript xatosi: {str(js_err)}"
                self.logger.error(message)
                raise JavaScriptError(message)

            time.sleep(retry_interval)

        message = f"Asinxron operatsiyalar {timeout}s ichida tugallanmadi"
        self.logger.error(message)
        raise LoaderTimeoutError(message)

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

            except JavascriptException as js_err:
                message = f"Block UI tekshirishda JavaScript xatosi: {str(js_err)}"
                self.logger.error(message)
                raise JavaScriptError(message)

            time.sleep(retry_interval)

        # Agar timeout tugasa va hali ham bloklangan bo‘lsa, xatolik chiqariladi
        total_time = time.time() - start_time
        message = f"Block UI {timeout}s ichida yo'qolmadi (Jami vaqt: {total_time:.2f}s)"
        self.logger.error(message)
        raise LoaderTimeoutError(message)

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
                    self.logger.debug(f"Barcha spinnerlar yo‘qoldi ({elapsed_time:.2f}s)")
                    return True

            except TimeoutException:
                message = f"Spinnerlar {timeout}s ichida yo‘qolmadi!"
                self.logger.error(message)
                raise LoaderTimeoutError(message)

            time.sleep(retry_interval)

        message = f"Spinner yoki block UI {timeout}s ichida yo‘qolmadi!"
        self.logger.error(message)
        raise LoaderTimeoutError(message)

    def _wait_for_all_loaders(self, timeout=None, log_text=None):
        """Sahifaning to'liq barqaror holatga kelishini kutish."""

        timeout = timeout or self.default_page_load_timeout

        status_text = f"{log_text}: ->" if log_text else ""

        errors = []
        self.logger.debug(f"{'='*10} {status_text}  Started waiting {'='*10}")

        try:
            self._wait_for_async_operations(timeout)
        except (JavaScriptError, LoaderTimeoutError) as e:
            message = f"{status_text} _wait_for_async_operations xatosi: {str(e)}"
            self.logger.warning(message)
            errors.append(message)

        try:
            self._wait_for_block_ui_absence(timeout)
        except (JavaScriptError, LoaderTimeoutError) as e:
            message = f"{status_text} _wait_for_block_ui_absence xatosi: {str(e)}"
            self.logger.warning(message)
            errors.append(message)

        try:
            self._check_spinner_absence(timeout)
        except (JavaScriptError, LoaderTimeoutError) as e:
            message = f"{status_text} _check_spinner_absence xatosi: {str(e)}"
            self.logger.warning(message)
            errors.append(message)

        if len(errors) == 3:
            full_error_message = "\n".join(errors)
            self.logger.error(f"{status_text} Barcha yuklanish funksiyalari muvaffaqiyatsiz tugadi.\n{full_error_message}")
            raise LoaderTimeoutError(full_error_message)

        self.logger.debug(f"{'='*10} {status_text} Finished waiting {'='*10}")
        return True

    # ------------------------------------------------------------------------------------------------------------------

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

    def _click_action_chains(self, element):
        """ActionChains yordamida veb-elementni bosish funksiyasi."""
        try:
            self.actions.move_to_element(element).click().perform()
            return True
        except Exception as e:
            self.logger.error(f"ActionChains yordamida bosishda xatolik: {e}")
            return False

    def _click_offset(self, element):
        """Offset orqali elementni bosish"""
        location = element.location
        size = element.size
        x = location['x'] + size['width'] // 2
        y = location['y'] + size['height'] // 2
        try:
            self.actions.move_by_offset(x, y).click().perform()
            return True
        except Exception as e:
            self.logger.error(f"Offset orqali bosishda xatolik: {e}")
            return False

    # ------------------------------------------------------------------------------------------------------------------

    def _wait_for_presence(self, locator, timeout=None):
        """Element DOMda mavjud ekanligini tekshirish"""
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return element

        except StaleElementReferenceException as e:
            self.logger.warning(f"{page_name}: Element DOM da yangilandi: {locator}")
            raise ElementStaleError("Element DOM da yangilandi", locator, e)

        except TimeoutException as e:
            self.logger.warning(f"{page_name}: Element {timeout}s ichida DOM da topilmadi: {locator}")
            raise ElementNotFoundError(f"Element {timeout}s ichida DOM da topilmadi", locator, e)

        except Exception as e:
            self.logger.warning(f"{page_name}: Element DOM da mavjudligi da kutilmagan xato: {str(e)}")
            raise ElementInteractionError(f"Kutilmagan xato - DOM", locator, e)

    def _scroll_to_element(self, element, locator, timeout=None):
        """Elementga scroll qilish."""

        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        try:
            if element is None:
                raise ElementNotFoundError("Element topilmadi, scroll qilish imkonsiz", locator)

            if element.is_displayed():
                return element

            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

            WebDriverWait(self.driver, timeout).until(lambda d: element.is_displayed())

            self.logger.info(f"{page_name}: Scroll muvaffaqiyatli bajarildi: {locator}")
            return element

        except NoSuchElementException as e:
            self.logger.warning(f"{page_name}: Element topilmadi, scroll ishlamadi: {locator}")
            raise ElementNotFoundError("Element topilmadi, scroll ishlamadi", locator, e)

        except StaleElementReferenceException as e:
            self.logger.warning(f"{page_name}: Element DOM da yangilandi: {locator}")
            raise ElementStaleError("Element DOM da yangilandi", locator, e)

        except TimeoutException as e:
            self.logger.warning(f"{page_name}: Element {timeout}s ichida sahifada ko'rinmadi: {locator}")
            raise ScrollError(f"Element {timeout}s ichida sahifada ko'rinmadi", locator, e)

        except JavascriptException as e:
            self.logger.warning(f"{page_name}: JavaScript scrollIntoView xatoligi: {locator} - Xato: {str(e)}")
            raise JavaScriptError("JavaScript scrollIntoView ishlamay qoldi", locator, e)

        except Exception as e:
            self.logger.warning(f"{page_name}: Scroll qilishda kutilmagan xatolik: {str(e)}")
            raise ElementInteractionError("Kutilmagan xatolik - Scroll", locator, e)

    def _wait_for_visibility(self, locator, timeout=None, error_message=True):
        """Element ko'rinishini kutish"""

        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        try:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return element

        except StaleElementReferenceException as e:
            if error_message:
                self.logger.warning(f"{page_name}: Element ko'rinishini kutishda DOM da yangilandi: {locator}")
            raise ElementStaleError("Element ko'rinishini kutishda DOM da yangilandi", locator, e)

        except TimeoutException as e:
            if error_message:
                self.logger.warning(f"{page_name}: Element {timeout}s ichida ko'rinmadi: {locator}")
            raise ElementVisibilityError(f"Element {timeout}s ichida ko'rinmadi", locator, e)

        except Exception as e:
            if error_message:
                self.logger.warning(f"{page_name}: Element kutishda kutilmagan xato: {str(e)}")
            raise ElementInteractionError("Kutilmagan xatolik - Visibility", locator, e)

    def _wait_for_clickable(self, locator, timeout=None):
        """ Element bosiladigan holatda ekanligini tekshirish """
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            return element

        except StaleElementReferenceException as e:
            self.logger.warning(f"{page_name}: Element bosiladigan holatga kelishda DOM da yangilandi: {locator}")
            raise ElementStaleError("Element bosiladigan holatga kelishda DOM da yangilandi", locator, e)

        except TimeoutException as e:
            self.logger.warning(f"{page_name}: Element {timeout}s ichida bosiladigan holga kelmadi: {locator}")
            raise ElementNotClickableError("Element bosilmaydigan holatda", locator, e)

        except Exception as e:
            self.logger.warning(f"{page_name}: Element bosilishi da kutilmagan xato: {str(e)}")
            raise ElementInteractionError("Kutilmagan xatolik - Clickable", locator, e)

    # Click ------------------------------------------------------------------------------------------------------------

    def is_checkbox_selected(self, locator):
        try:
            checkbox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))

            # Checkbox tanlangan yoki yo'qligini tekshiramiz
            return checkbox.is_selected()
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
            return False

    def click(self, locator, retries=3, retry_delay=2):
        """Elementni bosish funksiyasi"""

        page_name = self.__class__.__name__
        self.logger.debug(f"{page_name}: Running -> click: {locator}")

        attempt = 0
        while attempt < retries:
            try:
                self._wait_for_all_loaders(log_text='Run -> click')
                element_dom = self._wait_for_presence(locator)
                self._scroll_to_element(element_dom, locator)
                element_clickable = self._wait_for_clickable(locator)
                if element_clickable and self._click(element_clickable, locator):
                    return True

                time.sleep(retry_delay)
                self.logger.info(f"Retry Click sinab ko'riladi...")
                self._wait_for_all_loaders(log_text='Run -> retry click')
                element_clickable = self._wait_for_clickable(locator)
                if element_clickable and self._click(element_clickable, locator, retry=True):
                    return True

                time.sleep(retry_delay)
                self.logger.info(f"Majburiy JS Click sinab ko'riladi...")
                self._wait_for_all_loaders(log_text='Run -> JS click')
                element_dom = self._wait_for_presence(locator)
                if element_dom and self._click_js(element_dom, locator):
                    return True

            except (ElementStaleError, ScrollError, JavaScriptError) as e:
                self.logger.warning(f"{page_name}: {e.message}, qayta urinish ({attempt + 1}/{retries})")
                time.sleep(retry_delay)

            except (ElementNotFoundError, ElementNotClickableError, LoaderTimeoutError) as e:
                self.logger.error(f"{page_name}: {e.message} - Element topilmadi. Click bekor qilindi.")
                self.take_screenshot(f"{page_name.lower()}_click_elem_not_found_error")
                raise

            except Exception as e:
                self.logger.error(f"{page_name}: Kutilmagan xato: {str(e)}")
                self.take_screenshot(f"{page_name.lower()}_click_unexpected_error")
                raise

            attempt += 1

        message = f"{page_name}: Element barcha usullar bilan bosilmadi ({attempt}/{retries}) - {locator}"
        self.logger.error(message)
        self.take_screenshot(f"{page_name.lower()}_click_error")
        raise ElementInteractionError(message, locator)

    # Wait -------------------------------------------------------------------------------------------------------------

    def wait_for_element_visible(self, locator, retries=3, retry_delay=1):
        """Elementni ko'rinishini kutish funksiyasi"""

        page_name = self.__class__.__name__
        self.logger.debug(f"{page_name}: Running -> wait_for_element_visible: {locator}")

        time.sleep(1)
        attempt = 0

        while attempt < retries:
            try:
                self._wait_for_all_loaders(log_text='Run -> wait_for_element_visible')
                element_dom = self._wait_for_presence(locator)
                self._scroll_to_element(element_dom, locator)
                element = self._wait_for_visibility(locator)

                if element:
                    self.logger.info(f"⏺ {page_name}: Element topildi: {locator}")
                    return element

            except (ElementStaleError, ScrollError, JavaScriptError) as e:
                self.logger.warning(f"{page_name}: {e.message}, qayta urinish ({attempt + 1}/{retries})")
                time.sleep(retry_delay)

            except (ElementNotFoundError, ElementVisibilityError, LoaderTimeoutError) as e:
                self.logger.error(f"{page_name}: {e.message} - Element topilmadi. Qidirish bekor qilindi.")
                self.take_screenshot(f"{page_name.lower()}_visibility_elem_not_found_error")
                raise

            except Exception as e:
                self.logger.error(f"{page_name}: Kutilmagan xato: {str(e)}")
                self.take_screenshot(f"{page_name.lower()}_visibility_unexpected_error")
                raise

            attempt += 1

        message = f"{page_name}: Element barcha usullar bilan topilmadi ({attempt}/{retries}) - {locator}"
        self.logger.error(message)
        self.take_screenshot(f"{page_name.lower()}_visibility_error")
        raise ElementInteractionError(message, locator)

    # ------------------------------------------------------------------------------------------------------------------
    def _wait_for_presence_all(self, locator, timeout=None):
        """Elementlar ro'yxatini kutish funksiyasi."""

        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        try:
            elements = WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))
            return elements

        except StaleElementReferenceException as e:
            message = "Elementlar ro'yhati DOM da yangilandi"
            self.logger.warning(f"{page_name}: {message}: {locator}")
            raise ElementStaleError(message, locator, e)

        except TimeoutException as e:
            message = "Elementlar ro'yhati topilmadi"
            self.logger.error(f"{page_name}: {message}: {locator}")
            raise ElementNotFoundError(message, locator, e)

        except Exception as e:
            message = "Elementlarni ro'yhatini qidirishda kutilmagan xato"
            self.logger.error(f"{page_name}: {message}: {str(e)}")
            raise ElementInteractionError(f"{message}: {str(e)}", locator, e)

    def _wait_for_invisibility_of_element(self, element, timeout=None, error_message=None):
        """Element ni ko'rinmas bo'lishini kutish."""

        timeout = timeout or self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element(element))
        except TimeoutException as e:
            if error_message:
                self.logger.error(f"Element interfeys dan yo'qolmadi: {e}")
            return False

    def _wait_for_invisibility_of_locator(self, locator, timeout=None, error_message=True):
        """Locator ko'rinmas bo'lishini kutish funksiyasi."""

        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        try:
            result = WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
            if result:
                return True
            else:
                if error_message:
                    self.logger.warning(f"{page_name}: Element hali ham ko'rinmoqda: {locator}")
                return False

        except StaleElementReferenceException as e:
            message = f"{page_name}: Element DOM da yangilandi: {locator}"
            if error_message:
                self.logger.warning(message)
            raise ElementStaleError(message, locator, e)

        except TimeoutException as e:
            message = f"{page_name}: Element ko'rinmas bo'lmadi: {locator}"
            if error_message:
                self.logger.error(message)
            raise ElementVisibilityError(message, locator, e)

        except Exception as e:
            message = f"{page_name}: Element kutishda kutilmagan xato: {str(e)}"
            if error_message:
                self.logger.error(message)
            raise ElementInteractionError(message, locator, e)

    # ------------------------------------------------------------------------------------------------------------------

    def input_text(self, locator, text, retries=3, retry_delay=1):
        """Element topib, matn kiritish funksiyasi"""

        page_name = self.__class__.__name__
        self.logger.debug(f"{page_name}: Running -> input_text: {locator}")

        attempt = 0
        while attempt < retries:
            try:
                self._wait_for_all_loaders()

                element_dom = self._wait_for_presence(locator)
                self._scroll_to_element(element_dom, locator)
                element_clickable = self._wait_for_clickable(locator)

                # Matn kiritish
                element_clickable.clear()
                element_clickable.send_keys(text)
                self.logger.info(f"Input: send_key -> '{text}'")
                return True

            except ElementStaleError:
                self.logger.warning(f"Elementi yangilandi, qayta urinish ({attempt + 1})...")
                attempt += 1
                time.sleep(retry_delay)

            except (ElementNotFoundError, ScrollError, ElementNotClickableError, LoaderTimeoutError) as e:
                self.logger.error(f"{page_name}: {e.message}")
                self.take_screenshot(f"{page_name.lower()}_input_error")
                raise

            except Exception as e:
                message = "Matn kiritishda kutilmagan xatolik"
                self.logger.error(f"{message}: {str(e)}")
                self.take_screenshot(f"{page_name.lower()}_input_error")
                raise ElementInteractionError(f"{message}: {str(e)}", locator, e)

    # ------------------------------------------------------------------------------------------------------------------

    def clear_element(self, locator, retries=3, retry_delay=1):
        """ Elementni tozalash (clear) barqaror mexanizm bilan """

        page_name = self.__class__.__name__
        self.logger.debug(f"{page_name}: Running -> clear_element: {locator}")

        attempt = 0
        while attempt < retries:
            try:
                element = self._wait_for_clickable(locator)

                # 1️⃣ Element readonly yoki disable emasligini tekshirish
                if not element.is_enabled() or element.get_attribute("readonly"):
                    self.logger.warning(f"⚠️ Elementni tozalab bo‘lmadi, u readonly yoki disabled! {locator}")
                    return False

                # 2️⃣ Elementning ko‘rinadiganligini tekshirish
                if not element.is_displayed():
                    self.logger.warning(f"⚠️ Element ko‘rinmayapti, JavaScript orqali tozalaymiz: {locator}")
                    self.driver.execute_script("arguments[0].value = '';", element)
                    return True

                # 3️⃣ Avval click(), keyin clear()
                # element.click()
                # time.sleep(0.5)  # Kursorni inputga tushirish uchun biroz kutish
                element.clear()
                self.logger.info(f"✅ Element muvaffaqiyatli tozalandi: {locator}")
                return True

            except ElementStaleError:
                self.logger.warning(f"⚠️ Element yangilandi, qayta urinish ({attempt + 1})...")
                attempt += 1
                time.sleep(retry_delay)

            except ElementNotClickableError:
                self.logger.warning(f"⏳ Element {retry_delay}s ichida bosiladigan holga kelmadi: {locator}")
                return False

            except Exception as e:
                self.logger.error(f"❌ Element textni o‘chirishda kutilmagan xato: {str(e)}")
                return False

        self.logger.warning(f"⚠️ Element {retries} marta urinishdan keyin tozalanmadi: {locator}")
        return False

    # ------------------------------------------------------------------------------------------------------------------
    def get_text(self, locator, retries=3, retry_delay=1):
        """Elementning matnini olish."""

        page_name = self.__class__.__name__
        self.logger.debug(f"{page_name}: Running -> get_text: {locator}")

        attempt = 0
        while attempt < retries:
            try:
                element = self._wait_for_visibility(locator)
                self.logger.info(f"Element: text -> '{element.text}'")
                return element.text if element else None

            except ElementStaleError:
                self.logger.warning(f"Element yangilandi, qayta urinish ({attempt + 1})...")
                attempt += 1
                time.sleep(retry_delay)

            except ElementVisibilityError:
                self.logger.warning(f"Element topilmadi, vaqt tugadi!")
                return None

            except Exception as e:
                self.logger.error(f"Element matnini olishda kutilmagan xato: {str(e)}")
                return None

    # ------------------------------------------------------------------------------------------------------------------

    def get_numeric_value(self, locator):
        """Elementdan raqamli qiymatni ajratib olish va float formatiga o'tkazish."""

        page_name = self.__class__.__name__
        self.logger.debug(f"{page_name}: Running -> get_numeric_value: {locator}")

        text = self.get_text(locator)
        if text is None:
            self.logger.error(f"{page_name}: Element topilmadi -> None qiymat qaytdi")
            return None

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
            self.logger.error(f"{page_name}: Noto'g'ri raqam formati - {text}")
            return None

        try:
            return float(numeric_value) if numeric_value else None  # `None` bo‘lsa, `None` qaytadi
        except ValueError as e:
            self.logger.error(f"{page_name}: Float ga o'tkazishda xato - {str(e)}")
            return None

    # ------------------------------------------------------------------------------------------------------------------

    def get_current_url(self):
        """Joriy URL ni olish."""

        return self.driver.current_url

    # ------------------------------------------------------------------------------------------------------------------

    def cut_url(self):
        current_url = self.get_current_url()

        try:
            base_path = current_url.split('#')[0]  # https://smartup.online
            after_hash = current_url.split('#')[1]  # /!6lybkj03t/anor/mdeal/return/return_list

            # '/!' dan keyingi birinchi '/' gacha bo'lgan ID ni olish
            user_id = after_hash.split('/!')[1].split('/')[0]  # 6lybkj03t

            return f"{base_path}#/!{user_id}/"

        except Exception:
            self.logger.error("cut_url URL ni kesishda xatolik.")
            return current_url

    # ------------------------------------------------------------------------------------------------------------------
    def open_new_window(self, url: str) -> bool:
        """Yangi oynada URL ochish."""

        try:
            self._wait_for_all_loaders(log_text='open_new_window')

            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.get(url)

            if self._wait_for_all_loaders(log_text='check_new_window'):
                self.logger.info(f"URL muvaffaqiyatli ochildi: {url}")
                return True

        except LoaderTimeoutError:
            message = "Yangi oyna ochish uchun berilgan vaqt tugadi"
            self.logger.error(message)
            self.take_screenshot("open_new_timeout_error")
            raise LoaderTimeoutError(message)

        except Exception as e:
            self.logger.error(f"Yangi oyna ochishda xato: {str(e)}", exc_info=True)
            self.take_screenshot("open_new_window_error")
            raise

    # ------------------------------------------------------------------------------------------------------------------
    def switch_to_previous_window(self) -> bool:
        """Avvalgi oynaga qaytish."""

        try:
            # Barcha oyna handle'larini olish
            handles = self.driver.window_handles

            if len(handles) > 1:
                # Joriy oynani yopish
                self.driver.close()
                # Avvalgi oynaga o'tish
                self.driver.switch_to.window(handles[-2])
                if self._wait_for_all_loaders(log_text='switch_to_previous_window'):
                    self.logger.info("Avvalgi oynaga qaytildi")
                    return True
            else:
                self.logger.error("Avvalgi oyna topilmadi")
                return False

        except LoaderTimeoutError:
            message = "Avvalgi oynaga qaytish uchun berilgan vaqt tugadi"
            self.logger.error(message)
            self.take_screenshot("switch_to_timeout_error")
            raise LoaderTimeoutError(message)

        except Exception as e:
            self.logger.error(f"Avvalgi oynaga qaytishda xato: {str(e)}", exc_info=True)
            self.take_screenshot("switch_to_previous_window_error")
            return False

    # ------------------------------------------------------------------------------------------------------------------
    def refresh_page(self) -> bool:
        """Joriy sahifani yangilash."""

        try:
            self.driver.refresh()
            if self._wait_for_all_loaders(log_text='refresh_page'):
                self.logger.info("Sahifa muvaffaqiyatli yangilandi")
                return True

        except LoaderTimeoutError:
            message = "Sahifa yangilangandan so'ng to'liq yuklanmadi"
            self.logger.error(message)
            self.take_screenshot("refresh_window_timeout_error")
            raise LoaderTimeoutError(message)

        except Exception as e:
            self.logger.error(f"Sahifani yangilashda xato: {str(e)}", exc_info=True)
            self.take_screenshot("refresh_page_error")
            return False

    # ------------------------------------------------------------------------------------------------------------------
    def click_options(self, input_locator, options_locator, element, scroll=30):
        """Dropdown bilan ishlash uchun funksiya."""

        page_name = self.__class__.__name__
        self.logger.debug(f"{page_name}: Running: -> click_options: {input_locator}")

        try:
            # 1. Dropdown ochish
            if not self.click(input_locator):
                raise ElementNotClickableError("Dropdown ochilmadi", input_locator)

            # 2. Optionlarni yuklanishini kutish
            self.logger.info(f"{page_name}: Dropdown ochildi, elementlar yuklanmoqda...")
            options = self._wait_for_presence_all(options_locator)

            if not options:
                raise ElementNotFoundError("Dropdown elementlari topilmadi", options_locator)

            # 3. Element topish va bosish funksiyasi
            def find_and_click_option(options):
                element_str = str(element).strip()
                for option in options:
                    if option.text.strip() == element_str:
                        try:
                            if self._click(option, options_locator) or \
                                    self._click(option, options_locator, retry=True) or \
                                    self._click_js(option, options_locator):
                                self.logger.info(f"⏺ {page_name}: Element '{element}' bosildi")
                                return True
                        except Exception as e:
                            raise ElementNotClickableError(f"Elementni bosib bo‘lmadi: {str(e)}", options_locator)
                return False

            # 4. Elementni qidirish
            if find_and_click_option(options):
                if self._check_dropdown_closed(options_locator):
                    return True

            # 5. Scroll qilib qidirish
            self.logger.info(f"{page_name}: Element '{element}' topilmadi. Scroll qilinmoqda...")

            dropdown_container = self._find_visible_container(options_locator)
            if not dropdown_container:
                self.logger.error(f"❌ {page_name}: Dropdown konteyner topilmadi!")
                self.take_screenshot(f"{page_name.lower()}_dropdown_not_found")
                raise ElementNotFoundError("Dropdown konteyner topilmadi", options_locator)

            # 6. Scroll bilan qidirish
            last_height = 0
            for attempt in range(scroll):
                try:
                    self.driver.execute_script("arguments[0].scrollBy(0, 300);", dropdown_container)
                    time.sleep(0.5)

                    options = self._wait_for_presence_all(options_locator)
                    if options and find_and_click_option(options):
                        if self._check_dropdown_closed(options_locator):
                            return True

                    new_height = self.driver.execute_script("return arguments[0].scrollHeight", dropdown_container)
                    if new_height == last_height:
                        self.logger.warning(f"{page_name}: Element '{element}' scroll tugagandan keyin ham topilmadi.")
                        break

                    last_height = new_height

                except ElementStaleError:
                    self.logger.warning(f"{page_name}: Stale element topildi, qayta urinish...")
                    if attempt == scroll - 1:
                        raise
                    continue

            raise ElementNotFoundError(
                f"Element '{element}' {scroll} marta scroll qilingandan keyin ham topilmadi", options_locator)

        except (ElementNotFoundError, ElementNotClickableError, ScrollError) as e:
            self.logger.error(f"{page_name}: {e.message}")
            self.take_screenshot(f"{page_name.lower()}_click_options_error")
            raise

        except Exception as e:
            message = f"Kutilmagan xato"
            self.logger.error(f"{page_name}: {message}: {str(e)}")
            self.take_screenshot(f"{page_name.lower()}_click_options_error")
            raise ElementInteractionError(f"{message}: {str(e)}", options_locator, e)

    def _check_dropdown_closed(self, options_locator, retry_count=3):
        """Dropdown yopilganligini tekshirish."""

        page_name = self.__class__.__name__

        for attempt in range(retry_count):
            try:
                self.logger.info(f"{page_name}: Dropdown yopilishi tekshirilmoqda, urinish {attempt + 1}/{retry_count}")

                self.driver.execute_script("document.body.click();")
                time.sleep(0.2)

                body = self._wait_for_presence((By.TAG_NAME, 'body'))
                body.send_keys(Keys.ESCAPE)
                time.sleep(0.2)

                # **Agar dropdown allaqachon yopilgan bo‘lsa, qaytib ketish**
                if self._wait_for_invisibility_of_locator(options_locator):
                    self.logger.info(f"{page_name}: Dropdown muvaffaqiyatli yopildi")
                    return True

            except TimeoutException:
                self.logger.warning(f"{page_name}: TimeoutException - Dropdown allaqachon yopiq bo‘lishi mumkin.")
                return True  # **Agar dropdown topilmasa, demak yopiq, xatolik bermaslik kerak**

            except ElementVisibilityError:
                if attempt < retry_count - 1:
                    self.logger.warning(
                        f"⚠️ {page_name}: Dropdown yopilmadi, yana urinib ko‘ramiz... ({attempt + 1}/{retry_count})")
                    continue
                else:
                    self.logger.error(f"❌ {page_name}: Dropdown yopilmadi, xatolik chiqarilmoqda.")
                    self.take_screenshot(f"{page_name.lower()}_dropdown_close_error")
                    raise

        # **Agar barcha urinishlardan keyin ham dropdown yopilmagan bo‘lsa, xatolik beriladi**
        self.logger.error(f"❌ {page_name}: Dropdown yopilmadi ({retry_count} marta urinishdan keyin ham).")
        return False

    def _find_visible_container(self, options_locator, timeout=None):
        """Dropdown uchun ko'rinadigan konteynerni topish."""

        timeout = timeout or self.default_timeout
        page_name = self.__class__.__name__

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
                    WebDriverWait(self.driver, timeout).until(
                        lambda d: len(d.find_elements(By.XPATH, selector)) > 0)
                    containers = self.driver.find_elements(By.XPATH, selector)

                    for container in containers:
                        try:
                            if container.is_displayed():
                                elements_inside = container.find_elements(By.XPATH, ".//*")
                                self.logger.info(
                                    f"✅ {page_name}: Tanlangan konteyner: '{selector}', elementlar soni: {len(elements_inside)}")
                                return container
                        except StaleElementReferenceException:
                            self.logger.warning(
                                f"⚠️ {page_name}: StaleElementReferenceException: '{selector}' qayta yuklanmoqda")
                            continue  # Agar `stale element` bo‘lsa, keyingi elementga o‘tamiz

                except TimeoutException:
                    self.logger.warning(f"⚠️ {page_name}: Timeout kutish: '{selector}' topilmadi")
                    continue  # Agar `TimeoutException` bo‘lsa, keyingi selectorni tekshiramiz

            raise ElementNotFoundError(
                message=f"{page_name}: Ko'rinadigan dropdown konteyner topilmadi",
                locator=(By.XPATH, " | ".join(possible_container_selectors)))

        except ElementNotFoundError as e:
            self.logger.error(f"❌ {page_name}: {e.message}")
            self.take_screenshot(f"{page_name.lower()}_dropdown_not_found")
            raise

        except Exception as e:
            message = f"Konteyner qidirishda kutilmagan xato"
            self.logger.error(f"❌ {page_name}: {message}: {str(e)}")
            self.take_screenshot(f"{page_name.lower()}_dropdown_error")
            raise ElementInteractionError(f"{message}: {str(e)}", options_locator, e)

    # ------------------------------------------------------------------------------------------------------------------

    def find_row_and_click(self, element_name, timeout=5, retries=3, retry_delay=2, xpath_pattern=None, click=True, checkbox=False):
        """Jadvaldagi qatorni topish va ustiga bosish funksiyasi."""

        timeout = timeout or self.default_timeout
        page_name = self.__class__.__name__
        self.logger.info(f"{page_name}: Jadval qatori qidirilmoqda: {element_name}")

        if not xpath_pattern:
            xpath_pattern = ("//div[contains(@class, 'tbl')]//div[contains(@class, 'tbl-row')]"
                             "//div[contains(@class, 'tbl-cell') and normalize-space(text())='{}']")

        row_locator = (By.XPATH, xpath_pattern.format(element_name))
        limit_change_button = (By.XPATH, '//button[@class="btn btn-default rounded-0 ng-binding"]')
        limit_option = (
            By.XPATH, f'//button[@class="btn btn-default rounded-0 ng-binding"]/following-sibling::div/a[4]')
        checkbox_locator = (By.XPATH, f"//div[contains(@class, 'tbl-row') and .//div[text()='{element_name}']]//span")
        search_input = (By.XPATH, '//b-grid-controller//input[@type="search"]')

        limit_raised = False
        search_used = False

        attempt = 0
        while attempt < retries:
            try:
                self._wait_for_all_loaders(log_text='find_and_click_row')
                try:
                    elements = self._wait_for_presence_all(row_locator, timeout)
                except ElementNotFoundError:
                    if not limit_raised:
                        self.logger.info(f"{page_name}: '{element_name}' topilmadi, jadval limiti oshirilmoqda...")
                        self._click(self._wait_for_clickable(limit_change_button))
                        self._click(self._wait_for_clickable(limit_option))
                        self.logger.info("Limit oshirildi -> ro'yhatda 1000 ta elemet bor")
                        limit_raised = True
                        continue

                    elif not search_used:
                        self.logger.warning(
                            f"{page_name}: Limit oshirilganidan keyin ham '{element_name}' topilmadi. Qidiruvga berilmoqda...")
                        element = self._wait_for_clickable(search_input)
                        if element:
                            element.clear()
                            element.send_keys(element_name)
                            element.send_keys(Keys.RETURN)
                        search_used = True
                        continue

                    else:
                        raise ElementNotFoundError(f"{element_name} topilmadi, Limit va Qidiruv da ham", row_locator)

                target_element = elements[0]
                self._scroll_to_element(target_element, row_locator)
                self._wait_for_visibility(row_locator)

                if click:
                    element_clickable = self._wait_for_clickable(row_locator)
                    if element_clickable and self._click(element_clickable, row_locator):
                        return True

                    time.sleep(retry_delay)
                    self.logger.info(f"Retry Click sinab ko'riladi...")
                    self._wait_for_all_loaders(log_text='Run -> retry click')
                    element_clickable = self._wait_for_clickable(row_locator)
                    if element_clickable and self._click(element_clickable, row_locator, retry=True):
                        return True

                    time.sleep(retry_delay)
                    self.logger.info(f"Majburiy JS Click sinab ko'riladi...")
                    self._wait_for_all_loaders(log_text='Run -> JS click')
                    element_dom = self._wait_for_presence(row_locator)
                    if element_dom and self._click_js(element_dom, row_locator):
                        return True

                if checkbox:
                    element_dom = self._wait_for_presence(checkbox_locator)
                    if element_dom and self._click_js(element_dom, checkbox_locator):
                        return True

            except (ElementStaleError, ScrollError, JavaScriptError) as e:
                self.logger.warning(f"{page_name}: {e.message}, qayta urinish ({attempt + 1}/{retries})")
                time.sleep(retry_delay)

            except (ElementNotFoundError, ElementNotClickableError, LoaderTimeoutError) as e:
                self.logger.error(f"{page_name}: {e.message} - Element topilmadi. Click bekor qilindi.")
                self.take_screenshot(f"{page_name.lower()}_find_row_error")
                raise

            except Exception as e:
                self.logger.error(f"{page_name}: Kutilmagan xatolik: {str(e)}")
                self.take_screenshot(f"{page_name.lower()}_find_row_error")
                raise

            attempt += 1

        message = f"{page_name}: Element barcha usullar bilan bosilmadi ({attempt}/{retries}) - {row_locator}"
        self.logger.error(message)
        self.take_screenshot(f"{page_name.lower()}_click_row_error")
        raise ElementInteractionError(message, row_locator)

    # ------------------------------------------------------------------------------------------------------------------
