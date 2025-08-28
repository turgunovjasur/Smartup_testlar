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

from utils.assertions import Assertions
from utils.log_helpers import log_start_end_for_current_method, get_caller_chain
from utils.logger import get_test_name, configure_logging
from utils.exception import *
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException,
    NoSuchElementException,
    JavascriptException)

from utils.ui_loaders import UILoaders

init(autoreset=True)

class BasePage:
    # ==================================================================================================================

    def __init__(self, driver):
        self.driver = driver
        self.default_timeout = 20
        self.page_load_timeout = 60
        self.test_name = get_test_name()
        self.actions = ActionChains(driver)
        self.logger = configure_logging(self.test_name)
        self.assertions = Assertions(page=self, timeout=self.default_timeout)
        self._loaders = UILoaders(
            driver=self.driver, logger=self.logger,
            page_load_timeout=self.page_load_timeout,  # umumiy limit
            block_ui_absence_window=0.5,               # Block UI barqaror yo'qligi
            screenshot_cb=self.take_screenshot)        # ixtiyoriy

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

    def _get_caller_chain(self, depth=5, invoker_name=False, log_name=None):
        """
        1) _get_caller_chain()                -> zanjir stringini qaytaradi (default depth=5)
        2) _get_caller_chain(invoker_name=True)
           -> start/end header yozadi: "===== start: <method> - <invoker> ====="
        3) _get_caller_chain(log_name='payment')
           -> start/end header yozadi: "===== start: <method> - payment ====="
        """
        if log_name:
            log_start_end_for_current_method(self.logger, label=log_name, use_invoker=False)
        elif invoker_name:
            log_start_end_for_current_method(self.logger, label=None, use_invoker=True)

        return get_caller_chain(depth=depth)

    # ==================================================================================================================

    def _wait_for_all_loaders(self, page_load_timeout=None, block_ui_absence_window=None):
        """
        Loader kutish funksiyasi — agar timeoutlar berilsa, vaqtincha ularni qo‘llaydi.
        """
        return self._loaders.wait_for_all_loaders(
            page_load_timeout=page_load_timeout,
            block_ui_absence_window=block_ui_absence_window
        )

    # ==================================================================================================================

    def _click(self, element, locator=None, retry=False, _click_js=False):
        """Elementga oddiy yoki JavaScript orqali click qilish."""

        try:
            if _click_js:
                self.driver.execute_script("arguments[0].click();", element)
                self.logger.info(f"⏺ JS Click SUCCESS: {locator}")
            else:
                element.click()
                if retry:
                    self.logger.info(f"🔁 Retry Click SUCCESS: {locator}")
                else:
                    self.logger.info(f"⏺ Click SUCCESS: {locator}")
            return True

        except WebDriverException as e:
            if _click_js:
                self.logger.warning(f"⏺ JS Click FAILED: {locator} | Error: {e}")
            else:
                if retry:
                    self.logger.warning(f"🔁 Retry Click FAILED: {locator} | Error: {e}")
                else:
                    self.logger.warning(f"⏺ Click FAILED: {locator} | Error: {e}")
            return False

    # ==================================================================================================================

    def _scroll_to_element(self, element, locator, timeout=None, scroll_center=False):
        """Elementga scroll qilish."""

        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        try:
            if element is None:
                raise ElementNotFoundError(message="Element yo'q, scroll qilish imkonsiz", locator=locator)

            if not scroll_center:
                if element.is_displayed():
                    return element

            self.driver.execute_script( "arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", element)

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
            raise

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
            element = WebDriverWait(
                self.driver, timeout,
                poll_frequency=0.3,
                ignored_exceptions=(StaleElementReferenceException, NoSuchElementException)).until(wait_types[wait_type](locator))
            return element

        except TimeoutException as e:
            message = f"{wait_type} sharti {timeout:.1f}s ichida bajarilmadi"
            if error_message:
                self.logger.warning(f"{page_name}: {message}: {locator}")
            if screenshot:
                self.take_screenshot(f"{page_name}_{wait_type}_timeout")

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
            raise

    # ==================================================================================================================

    def click_checkbox(self, locator, state=True):
        """Checkbox holatini kerakli qiymatga o‘zgartiradi."""

        caller_chain = self._get_caller_chain()
        self.logger.debug(f"{caller_chain}: {locator}")

        try:
            # self._wait_for_all_loaders()
            element_presence = self.wait_for_element(locator, wait_type="presence")
            self._scroll_to_element(element_presence, locator)

            start_state = element_presence.is_selected()
            self.logger.info(f"Checkbox start_state: {start_state}")

            if start_state != state:
                self._click(element_presence, locator, _click_js=True)
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

    def click(self, locator):
        """Elementni bosish (aqlli retrylar bilan)."""

        self.logger.debug(f"{self._get_caller_chain()}: {locator}")
        self._wait_for_all_loaders()

        for attempt in range(3):
            try:
                element = self.wait_for_element(locator, wait_type="clickable")
                self._scroll_to_element(element, locator)
                if self._click(element, locator):
                    return True

                # 2) Qayta clickable (kuchsiz kechikish)
                time.sleep(0.5)
                element = self.wait_for_element(locator, wait_type="clickable")
                if self._click(element, locator, retry=True):
                    return True

                # 3) JS fallback: presence + scroll
                element = self.wait_for_element(locator, wait_type="presence")
                self._scroll_to_element(element, locator)
                if self._click(element, locator, _click_js=True):
                    return True

            except (ElementStaleError, ScrollError, JavaScriptError) as e:
                self.logger.warning(f"Qayta urinish ({attempt + 1}/3): {e} -> {locator}")
                time.sleep(1)

            except Exception as e:
                # Bu bosqichda kutilmagan xatoni kontekst bilan ko‘taramiz
                self.logger.error(f"Kutilmagan xatolik: {e}: {locator}")
                self.take_screenshot(f"{__class__.__name__.lower()}_click_error")
                raise ElementInteractionError("Elementni bosishda kutilmagan xato", locator, e)

        message = f"Element barcha usullar bilan bosilmadi (3/3)"
        self.logger.warning(f"{message}: {locator}")
        self.take_screenshot(f"{__class__.__name__.lower()}_click_all_error")
        raise ElementNotClickableError(message, locator=locator)

    # ==================================================================================================================

    def wait_for_element_visible(self, locator):
        """Elementni ko'rinishini kutish funksiyasi"""

        self.logger.debug(f"{self._get_caller_chain()}: {locator}")

        for attempt in range(3):
            try:
                self._wait_for_all_loaders()
                element = self.wait_for_element(locator, wait_type="presence")
                self._scroll_to_element(element, locator)
                element = self.wait_for_element(locator, wait_type="visibility")
                self.logger.info(f"⏺ Visible SUCCESS: {locator}")
                return element

            except (ElementStaleError, ScrollError, JavaScriptError) as e:
                self.logger.warning(f"{e.message}, qayta urinish ({attempt + 1}/{3})")
                time.sleep(1)

        self.logger.warning(f"Element topilmadi: {locator}")
        self.take_screenshot(f"{__class__.__name__.lower()}_visible_all_error")
        raise

    # ==================================================================================================================

    def _wait_for_presence_all(self, locator, timeout=None, visible_only=False):
        """Elementlar ro'yxatini kutish funksiyasi."""

        self.logger.debug(f"{self._get_caller_chain()}: {locator}")

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

        self.logger.debug(f"{self._get_caller_chain()}")

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

        self.logger.debug(f"{self._get_caller_chain()}: {locator}")

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

    def input_text(self, locator, text=None, check=False, get_value=False):
        """Element topib, matn kiritish funksiyasi"""

        self.logger.debug(f"{self._get_caller_chain()}: {locator}")
        self._wait_for_all_loaders()

        for attempt in range(3):
            try:
                element_dom = self.wait_for_element(locator, wait_type="presence")
                self._scroll_to_element(element_dom, locator)

                if get_value:
                    tag_name = element_dom.tag_name.lower()
                    if tag_name == "input" or tag_name == "textarea":
                        value = element_dom.get_attribute("value")
                    else:
                        value = element_dom.text
                    self.logger.info(f"Input: get_value -> '{value}'")
                    return value

                if text is not None:
                    element_clickable = self.wait_for_element(locator, wait_type="clickable")
                    element_clickable.clear()
                    element_clickable.send_keys(text)
                    self.logger.info(f"Input: send_key -> '{text}'")

                if check and text is not None:
                    check_text = self.driver.execute_script("return arguments[0].value;", element_dom)
                    self.logger.info(f"Check Input Value: -> '{check_text}'")
                    if check_text != text:
                        self.driver.execute_script("arguments[0].value = arguments[1];", element_dom, text)
                return True

            except ElementStaleError:
                self.logger.warning(f"Input yangilandi, qayta urinish ({attempt + 1})...")
                time.sleep(1)

            except Exception as e:
                self.logger.error(f"Matn kiritishda kutilmagan xatolik: {str(e)}: {locator}")
                self.take_screenshot(f"{__class__.__name__.lower()}_input_error")
                raise ElementInteractionError("Matn kiritishda kutilmagan xato", locator, e)

        message = f"Elementga matn kiritib bo‘lmadi (3/3)"
        self.logger.warning(f"{message}: {locator}")
        self.take_screenshot(f"{__class__.__name__.lower()}_input_text_all_error")
        raise ElementInteractionError(message, locator=locator)

    # ==================================================================================================================

    def clear_element(self, locator):
        """ Elementni tozalash."""

        self.logger.debug(f"{self._get_caller_chain()}: {locator}")

        attempt = 0
        while attempt < 3:
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
                time.sleep(1)

            except Exception as e:
                self.logger.error(f"Element textni o‘chirishda kutilmagan xato: {str(e)}")
                raise

        message = f"Element barcha urinishdan keyin ham tozalanmadi: {locator}"
        self.logger.warning(message)
        raise ElementInteractionError(message)

    # ==================================================================================================================

    def get_text(self, locator, clean=False):
        """Elementning matnini olish."""

        self.logger.debug(f"{self._get_caller_chain()}: {locator}")

        for attempt in range(3):
            try:
                self._wait_for_all_loaders()
                element_dom = self.wait_for_element(locator, wait_type="presence")
                self._scroll_to_element(element_dom, locator)
                element = self.wait_for_element(locator, wait_type="visibility")

                text = element.text

                if text == '':
                    self.logger.warning(f"Element ko‘rindi, lekin bo‘sh holatda (None): {locator}")
                    return None

                if clean:
                    self.logger.info(f"Element: before clean text -> <str'{text}'>")
                    text = text.replace(" ", "").replace("\u00A0", "").strip()
                    self.logger.info(f"Element: after clean text -> <str'{text}'>")

                self.logger.info(f"Element: return text -> <str'{text}'>")
                return text

            except (StaleElementReferenceException, ElementStaleError):
                self.logger.warning(f"Element yangilandi, qayta urinish ({attempt + 1})...")
                time.sleep(1)

            except Exception as e:
                self.logger.error(f"Element matnini olishda xato: {str(e)}")
                raise

        # funksiya oxiri:
        self.logger.error("Barcha urinishlarda ham text olinmadi (None).")
        return None

    # ==================================================================================================================

    def get_numeric_value(self, locator):
        """Elementdan raqamli qiymatni ajratib olish va float formatiga o'tkazish."""

        self.logger.debug(f"{self._get_caller_chain()}: {locator}")

        text = self.get_text(locator)

        if text is None:
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
        self.logger.debug(f"{self._get_caller_chain()}")

        self._wait_for_all_loaders()

        for attempt in range(3):
            try:
                current_url = self.driver.current_url
                self.logger.info(f"current_url: {current_url}/")

                base_path = current_url.split('#')[0]  # https://smartup.online
                after_hash = current_url.split('#')[1]  # /!6lybkj03t/anor/mdeal/return/return_list

                # '/!' dan keyingi birinchi '/' gacha bo'lgan ID ni olish
                user_id = after_hash.split('/!')[1].split('/')[0]  # 6lybkj03t
                self.logger.info(f"{base_path}#/!{user_id}/")

                return f"{base_path}#/!{user_id}/"

            except Exception as e:
                self.logger.error(f"[{attempt + 1}/3] cut_url bajarishda xatolik: {str(e)}", exc_info=True)
                time.sleep(1)

        message = f"server_name va user_id ni kesib bo'lmadi (3/3 urinishdan keyin)"
        self.logger.warning(message)
        self.take_screenshot(f"{__class__.__name__.lower()}_cut_url_error")
        raise ElementInteractionError(message)

    # ==================================================================================================================

    def switch_window(self, direction, url=None, new_window_timeout=None, loader_timeout=None):
        """
        Brauzer oynalar (tabs/windows) o‘rtasida o'tish.
        new_window_timeout: yangi handle paydo bo‘lishini kutish limiti (s)
        loader_timeout: oynaga o'tgandan keyin UILoaders uchun page_load_timeout (s)
        """

        try:
            current_window_id = self.driver.current_window_handle
            self.logger.debug(f"Joriy oyna ID: {current_window_id}")

            # Defaultlar: yangi oyna kutishi va loader kutishlari
            new_window_timeout = float(new_window_timeout or max(getattr(self, "page_load_timeout", 10), 15))
            loader_timeout = float(loader_timeout or getattr(self, "page_load_timeout", 10))

            if direction == "prepare":
                self._saved_handles = self.driver.window_handles.copy()
                self.logger.debug(f"Oynalar ro'yxati saqlandi: {self._saved_handles}")
                return True

            elif direction == "forward":
                # ❗ MUHIM: eski oynada loader kutmaymiz, avval yangi handle’ni kutamiz
                saved_handles = getattr(self, "_saved_handles", self.driver.window_handles.copy())
                self.logger.debug("Yangi oynaning ochilishini kutish boshlandi...")

                end = time.time() + new_window_timeout
                new_window_id = None
                while time.time() < end:
                    handles_now = self.driver.window_handles
                    new_ids = [h for h in handles_now if h not in saved_handles]
                    if new_ids:
                        new_window_id = new_ids[0]
                        self.logger.info(f"⏺ Yangi oyna topildi: {new_window_id}")
                        break
                    time.sleep(0.2)

                if not new_window_id:
                    self.logger.warning("Yangi oyna aniqlanmadi, oxirgi handle tanlanadi.")
                    new_window_id = self.driver.window_handles[-1]

                self.driver.switch_to.window(new_window_id)
                self.logger.info(f"Yangi oynaga o'tilmoqda: {current_window_id} -> {new_window_id}")

                # Endi yangi oynada sizning loader kutishingiz
                self._wait_for_all_loaders()
                self.logger.info(f"direction='{direction}' bo‘yicha oynaga muvaffaqiyatli o‘tildi")
                return True

            elif direction == "back":
                # Joriy oynani yopamiz va saved_handles/remaining asosida avvalgiga qaytamiz
                saved_handles = getattr(self, "_saved_handles", None)
                self.driver.close()
                remaining = self.driver.window_handles
                if not remaining:
                    raise Exception("Qolgan oyna topilmadi (remaining handles bo‘sh).")

                target_window_id = None
                if saved_handles:
                    for h in reversed(saved_handles):
                        if h in remaining:
                            target_window_id = h
                            break
                if not target_window_id:
                    target_window_id = remaining[-1]

                self.driver.switch_to.window(target_window_id)
                self.logger.info(f"Avvalgi oynaga o'tilmoqda: {current_window_id} -> {target_window_id}")

                # Qaytilgan oynada sizning loader kutishingiz
                self._wait_for_all_loaders()
                self.logger.info(f"direction='{direction}' bo‘yicha oynaga muvaffaqiyatli o‘tildi")
                return True

            elif direction == "new" and url:
                handles_before = self.driver.window_handles.copy()
                self.driver.execute_script("window.open('about:blank','_blank');")

                # Yangi handle’ni kutish (sizdagi polling uslubida)
                end = time.time() + new_window_timeout
                target_window_id = None
                while time.time() < end:
                    new_handles = self.driver.window_handles
                    new_ids = [h for h in new_handles if h not in handles_before]
                    if new_ids:
                        target_window_id = new_ids[0]
                        break
                    time.sleep(0.2)

                if not target_window_id:
                    target_window_id = self.driver.window_handles[-1]

                self.driver.switch_to.window(target_window_id)
                self.driver.get(url)
                self.logger.info(
                    f"url bo'yicha yangi oyna ochildi: {current_window_id} -> {target_window_id} | URL: {url}")

                # Yangi oynada sizning loader kutishingiz
                self._wait_for_all_loaders()
                self.logger.info(f"direction='{direction}' bo‘yicha oynaga muvaffaqiyatli o‘tildi")
                return True

            else:
                raise Exception(f"Noto‘g‘ri direction: {direction}")

        except LoaderTimeoutError:
            self.logger.error(f"{direction} oynaga o‘tish uchun vaqt tugadi")
            self.take_screenshot(f"switch_{direction}_timeout_error")
            raise

        except Exception as e:
            self.logger.error(f"{direction} oynaga o‘tishda xato: {str(e)}")
            self.take_screenshot(f"switch_{direction}_error")
            raise

    # def switch_window(self, direction, url=None):
    #     """
    #     Brauzer oynalar (tabs/windows) o‘rtasida o'tishni amalga oshiradi.
    #
    #     Parameters:
    #         direction (str):
    #             - "prepare" -> hozirgi oynalar ro‘yxatini eslab qoladi
    #             - "back"    -> avvalgi oynaga o‘tadi (joriy oynani yopadi)
    #             - "forward" -> yangi oyna ochilganini aniqlaydi va unga o‘tadi
    #             - "new"     -> yangi tab ochadi va URL'ga o'tadi
    #     """
    #     try:
    #         # time.sleep(2)
    #         self._wait_for_all_loaders()
    #         current_window_id = self.driver.current_window_handle
    #         self.logger.debug(f"Joriy oyna ID: {current_window_id}")
    #
    #         if direction == "prepare":
    #             self._saved_handles = self.driver.window_handles.copy()
    #             self.logger.debug(f"Oynalar ro'yxati saqlandi: {self._saved_handles}")
    #             return True
    #
    #         elif direction == "back":
    #             handles = self.driver.window_handles
    #             self.driver.close()
    #             self.driver.switch_to.window(handles[-2])
    #             target_window_id = handles[-2]
    #             self.logger.info(f"Avvalgi oynaga o'tilmoqda: {current_window_id} -> {target_window_id}")
    #
    #         elif direction == "forward":
    #             saved_handles = getattr(self, '_saved_handles', [])
    #             self.logger.debug("Yangi oynaning ochilishini kutish boshlandi...")
    #
    #             new_window_id = None
    #             for i in range(20):  # 0.5s * 20 = 10s
    #                 time.sleep(1)
    #                 handles_now = self.driver.window_handles
    #                 new_ids = list(set(handles_now) - set(saved_handles))
    #                 self.logger.debug(f"Tekshiruv {i + 1}: handles = {handles_now}")
    #                 if new_ids:
    #                     new_window_id = new_ids[0]
    #                     self.logger.info(f"⏺ Yangi oyna topildi: {new_window_id}")
    #                     break
    #
    #             if not new_window_id:
    #                 self.logger.warning("Yangi oyna topilmadi, oxirgi oynaga o‘tilmoqda.")
    #                 new_window_id = self.driver.window_handles[-1]
    #
    #             self.driver.switch_to.window(new_window_id)
    #             self.logger.info(f"Yangi oynaga o'tilmoqda: {current_window_id} -> {new_window_id}")
    #
    #         elif direction == "new" and url:
    #             handles_before = self.driver.window_handles.copy()
    #             self.driver.execute_script("window.open('');")
    #             time.sleep(1)
    #             new_handles = self.driver.window_handles
    #             new_ids = list(set(new_handles) - set(handles_before))
    #             target_window_id = new_ids[0] if new_ids else new_handles[-1]
    #             self.driver.switch_to.window(target_window_id)
    #             self.driver.get(url)
    #             self.logger.info(f"url bo'yicha yangi oyna ochildi: {current_window_id} -> {target_window_id} | URL: {url}")
    #
    #         else:
    #             raise Exception(f"Noto‘g‘ri direction: {direction}")
    #
    #         time.sleep(2)
    #         if self._wait_for_all_loaders():
    #             self.logger.info(f"direction='{direction}' bo‘yicha oynaga muvaffaqiyatli o‘tildi")
    #             return True
    #
    #     except LoaderTimeoutError:
    #         self.logger.error(f"{direction} oynaga o‘tish uchun vaqt tugadi")
    #         self.take_screenshot(f"switch_{direction}_timeout_error")
    #         raise
    #
    #     except Exception as e:
    #         self.logger.error(f"{direction} oynaga o‘tishda xato: {str(e)}")
    #         self.take_screenshot(f"switch_{direction}_error")
    #         raise

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
        """Sahifani yangilash."""

        self.logger.debug(f"{self._get_caller_chain()}")

        try:
            self.driver.refresh()
            self._wait_for_all_loaders()
            self.logger.info("Sahifa muvaffaqiyatli yangilandi")

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
        selected_text = self.input_text(input_locator, get_value=True)
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
        self.logger.debug(f"{self._get_caller_chain(invoker_name=True)}: {input_locator}")

        try:
            # Avval tanlanganini tekshirish
            if self._is_choose_dropdown_option(input_locator, element_text):
                return True

            # Input elementini topish va ochish
            web_element = self.wait_for_element(input_locator, wait_type="presence")
            self._scroll_to_element(element=web_element, locator=input_locator, scroll_center=True)
            web_element = self.wait_for_element(input_locator, wait_type="clickable")
            self._click(web_element, input_locator) or self._click(web_element, input_locator, _click_js=True)

            # Optionlarni kutish
            try:
                self.logger.info("Option larni kutish boshlandi...")
                options = self._wait_for_presence_all(options_locator, visible_only=True)
            except ElementNotFoundError:
                self.logger.warning("Option lar DOM da mavjud emas!")
                if self._is_choose_dropdown_option(input_locator, element_text):
                    return True
                raise  # DOMda yo‘q va tanlanmagan

            # Bo‘sh ro‘yxat holati
            if not options:
                self.logger.warning("Optionlar ro‘yxati bo‘sh (visible_only=True)")
                if self._is_choose_dropdown_option(input_locator, element_text):
                    return True

            # Topishga urinib ko‘rish
            if self._find_and_click_option(element_text, options, options_locator):
                if self._check_dropdown_closed(options_locator):
                    return True

            # Scroll orqali qidirish
            self.logger.info(f"{element_text} topilmadi. Scroll orqali qidirilmoqda...")
            dropdown_container = self._find_visible_container(options_locator)

            for attempt in range(scroll):
                self.driver.execute_script("arguments[0].scrollTop += arguments[0].offsetHeight;", dropdown_container)
                options = self._wait_for_presence_all(options_locator, visible_only=True)
                if self._find_and_click_option(element_text, options, options_locator):
                    if self._check_dropdown_closed(options_locator):
                        return True

                # Scroll tugaganligini aniqlash
                current_scroll = self.driver.execute_script("return arguments[0].scrollTop;", dropdown_container)
                max_scroll = self.driver.execute_script("return arguments[0].scrollHeight - arguments[0].clientHeight;", dropdown_container)
                if current_scroll >= max_scroll:
                    self.logger.info(f"Scroll oxiriga yetdi.")
                    break

            # Topilmasa xatolik
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
        """Element topish va bosish funksiyasi."""

        element_str = str(element).strip().lower()

        for option in options:
            # Text olish
            for _ in range(3):
                option_text = option.text.strip()
                if option_text:
                    break
                option_text = option.get_attribute("innerText") or ""
                self.logger.warning(f"Option text topilmadi, qayta uriniladi...")
                time.sleep(0.1)

            # Textni tozalash (\n va ortiqcha bo‘sh joylarni olib tashlash)
            option_text_clean = " ".join(option_text.split()).lower()

            self.logger.debug(f"Comparing: '{option_text_clean}' ↔ '{element_str}'")

            # Qisman moslik
            if element_str in option_text_clean:
                self.logger.info(f"Element topildi: '{option_text}', click qilinadi...")
                if self._click(option, options_locator) or self._click(option, options_locator, _click_js=True):
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

    def find_row_and_click(self, element_name, timeout=5, **kwargs):
        """Jadvaldagi qatorni topish va ustiga bosish funksiyasi."""

        self.logger.debug(f"{self._get_caller_chain(invoker_name=True)}: element_name: {element_name}")

        xpath_pattern = kwargs.get("xpath_pattern")
        limit_pattern = kwargs.get("limit_pattern")
        limit_option_pattern = kwargs.get("limit_option_pattern")
        use_limit = kwargs.get("use_limit", True)
        use_search = kwargs.get("use_search", True)
        click = kwargs.get("click", True)
        checkbox = kwargs.get("checkbox", False)

        row_locator = (By.XPATH, xpath_pattern or f"//div[contains(@class, 'tbl-row')]//div[contains(@class, 'tbl-cell') and contains(.,'{element_name}')]")
        limit_change_button = (By.XPATH, limit_pattern or '//button[@class="btn btn-default rounded-0 ng-binding"]')
        limit_option = (By.XPATH, limit_option_pattern or '//button[@class="btn btn-default rounded-0 ng-binding"]/following-sibling::div/a[4]')
        checkbox_locator = (By.XPATH, f"//div[contains(@class, 'tbl-row') and .//div[text()='{element_name}']]//span")
        search_input = (By.XPATH, '//b-grid-controller//input[@type="search"]')

        show_more = use_limit
        search_used = use_search

        attempt = 0
        while attempt < 3:
            try:
                self._wait_for_all_loaders()
                try:
                    elements = self._wait_for_presence_all(row_locator, timeout)
                except ElementNotFoundError:
                    self.logger.warning(f"'{element_name}' topilmadi.")
                    if show_more:
                        self.logger.info(f"Ro'yhat limiti oshirilmoqda...")

                        element = self.wait_for_element(limit_change_button, timeout=5, wait_type="clickable")
                        self._click(element, limit_change_button)

                        element = self.wait_for_element(limit_option, timeout=3, wait_type="clickable")
                        self._click(element, limit_option)

                        self.logger.info("Limit oshirildi.")
                        show_more = False
                        continue

                    if search_used:
                        self.logger.info(f"Qidiruvga berilmoqda...")
                        element = self.wait_for_element(search_input, wait_type="clickable")
                        element.send_keys(element_name)
                        element.send_keys(Keys.RETURN)
                        search_used = False
                        continue

                    else:
                        message = f"Limit va Qidiruv da ham topilmadi"
                        self.logger.error(message)
                        raise ElementNotFoundError(message, row_locator)

                self._scroll_to_element(elements[0], row_locator, scroll_center=True)
                time.sleep(0.5)

                if click:
                    if (self._click(element=elements[0], locator=row_locator) or
                            self._click(element=elements[0], locator=row_locator, _click_js=True)):
                        return True

                if checkbox:
                    element_dom = self.wait_for_element(checkbox_locator, wait_type="presence")
                    self._click(element_dom, checkbox_locator, _click_js=True)

            except (ElementStaleError, JavaScriptError) as e:
                self.logger.warning(f"{str(e)}, qayta urinish ({attempt + 1}/{3})"), time.sleep(2)

            except Exception as e:
                self.logger.error(f"Kutilmagan xatolik: {str(e)}")
                self.take_screenshot(f"{__class__.__name__.lower()}_find_row_error")
                raise

            attempt += 1

        message = f"Element barcha usullar bilan bosilmadi ({attempt}/{3})"
        self.logger.error(f"{message}: {row_locator}")
        self.take_screenshot(f"{__class__.__name__.lower()}_click_row_error")
        raise

    # ==================================================================================================================