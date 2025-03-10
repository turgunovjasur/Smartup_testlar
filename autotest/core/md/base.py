import inspect
import os
import re
import time
import allure
from datetime import datetime, timedelta
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
        self.default_timeout = 20
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
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout
        end_time = time.time() + timeout
        start_time = time.time()  # Tekshirish boshlanish vaqti

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
                    elapsed_time = time.time() - start_time  # Qancha vaqt o'tgani hisoblanadi
                    # self.logger.debug(f"{page_name}: Asinxron operatsiyalar yakunlandi ({elapsed_time:.2f}s)")
                    return True
                else:
                    self.logger.debug(f"{page_name}: Asinxron operatsiyalar davom etmoqda, qayta tekshirilmoqda...")
            except JavascriptException as js_err:
                error_message = f"Asinxron tekshiruvda JavaScript xatosi: {str(js_err)}"
                self.logger.error(f"{page_name}: {error_message}")
                raise JavaScriptError(error_message)

            time.sleep(retry_interval)

        error_message = f"Asinxron operatsiyalar {timeout}s ichida tugallanmadi"
        self.logger.error(f"{page_name}: {error_message}")
        raise LoaderTimeoutError(error_message)

    def _wait_for_block_ui_absence(self, timeout=None, retry_interval=0.5):
        """
        Block UI yo'qolishini kutish.
        JavaScript va DOM orqali Block UI holatini tekshiradi.
        """
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout
        end_time = time.time() + timeout
        start_time = time.time()

        # Block UI ni DOM orqali tekshirish uchun CSS selektor
        block_ui_selector = "div.block-ui-container"

        # JavaScript orqali elementning ko'rinishi va bloklanishini tekshirish skripti
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
                    # self.logger.debug(f"{page_name}: Block UI elementi DOM ichida topilmadi ({elapsed_time:.2f}s).")
                    return True  # Agar element umuman yo‘q bo‘lsa, yuklanish tugagan.

                # Agar element mavjud bo‘lsa, uni yashirin yoki yo‘qligini tekshiramiz
                js_result = self.driver.execute_script(block_ui_script, block_ui_selector)
                if js_result:
                    # self.logger.debug(
                        # f"{page_name}: Block UI nol o‘lchamda - yuklanish tugadi ({elapsed_time:.2f}s).")
                    return True  # Agar element mavjud bo‘lsa, lekin ko‘rinmasa - yuklanish tugagan.
                else:
                    self.logger.debug(
                        f"{page_name}: Block UI hali ham ko‘rinmoqda, kutish davom etmoqda... ({elapsed_time:.2f}s)")

            except JavascriptException as js_err:
                error_message = f"Block UI tekshirishda JavaScript xatosi: {str(js_err)}"
                self.logger.error(f"{page_name}: {error_message}")
                raise JavaScriptError(error_message)

            time.sleep(retry_interval)

        # Agar timeout tugasa va hali ham bloklangan bo‘lsa, xatolik chiqariladi
        total_time = time.time() - start_time
        error_message = f"Block UI {timeout}s ichida yo'qolmadi (Jami vaqt: {total_time:.2f}s)"
        self.logger.error(f"{page_name}: {error_message}")
        raise LoaderTimeoutError(error_message)

    def _check_spinner_absence(self, timeout=None, retry_interval=0.5):
        page_name = self.__class__.__name__
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
                                self.logger.debug(
                                    f"{page_name}: {locator} hali ham ko‘rinib turibdi. ({elapsed_time:.2f}s)")
                                break

                    if is_visible:
                        break

                if not is_visible:
                    self.logger.debug(f"{page_name}: Barcha spinner/block UI yo‘qoldi ({elapsed_time:.2f}s)")
                    return True

            except TimeoutException:
                self.logger.error(
                    f"{page_name}: Spinner yoki block UI {timeout}s ichida yo‘qolmadi! Skrinshot olinmoqda...")
                self.take_screenshot("spinner_timeout_error")
                raise LoaderTimeoutError(f"{page_name}: Spinner yoki block UI {timeout}s ichida yo‘qolmadi!")

            time.sleep(retry_interval)

        self.logger.error(f"{page_name}: Spinner yoki block UI {timeout}s ichida yo‘qolmadi! Skrinshot olinmoqda...")
        self.take_screenshot("spinner_timeout_error")
        raise LoaderTimeoutError(f"{page_name}: Spinner yoki block UI {timeout}s ichida yo‘qolmadi!")

    def _wait_for_all_loaders(self, timeout=60, log_text=None):
        """Sahifaning to'liq barqaror holatga kelishini kutish."""
        page_name = self.__class__.__name__

        status_text = f"{log_text}: ->" if log_text else ""
        # self.logger.debug(f"{page_name}: {status_text} Sahifa yuklanishini kutish boshlandi")

        try:
            self._wait_for_async_operations(timeout)
            self._wait_for_block_ui_absence(timeout)
            # self._check_spinner_absence(timeout)
            self.logger.debug(f"{page_name}: {status_text} Sahifa yuklandi")
            return True

        except (LoaderTimeoutError, JavaScriptError) as e:
            self.logger.error(f"{page_name}: {status_text} Sahifa yuklanishida xato: {str(e)}")
            raise LoaderTimeoutError

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
            raise ElementStaleError(
                message="Element DOM da yangilandi",
                locator=locator,
                original_error=e
            )
        except TimeoutException as e:
            self.logger.warning(f"{page_name}: Element {timeout}s ichida DOM da topilmadi: {locator}")
            raise ElementNotFoundError(
                message=f"Element {timeout}s ichida DOM da topilmadi",
                locator=locator,
                original_error=e
            )
        except Exception as e:
            self.logger.warning(f"{page_name}: Element DOM da mavjudligi da kutilmagan xato: {str(e)}")
            raise ElementInteractionError(
                message=f"Kutilmagan xato - DOM",
                locator=locator,
                original_error=e
            )

    def _scroll_to_element(self, element, locator, timeout=None):
        """Elementga scroll qilish."""
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        try:
            if element is None:
                raise ElementNotFoundError(
                    message="Element topilmadi, scroll qilish imkonsiz",
                    locator=locator
                )

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
            raise ScrollError("Kutilmagan xatolik - Scroll", locator, e)

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
            raise ElementStaleError(
                message="Element ko'rinishini kutishda DOM da yangilandi",
                locator=locator,
                original_error=e
            )
        except TimeoutException as e:
            if error_message:
                self.logger.warning(f"{page_name}: Element {timeout}s ichida ko'rinmadi: {locator}")
            raise ElementVisibilityError(
                message=f"Element {timeout}s ichida ko'rinmadi",
                locator=locator,
                original_error=e
            )
        except Exception as e:
            if error_message:
                self.logger.warning(f"{page_name}: Element kutishda kutilmagan xato: {str(e)}")
            raise ElementInteractionError(
                message="Kutilmagan xatolik - Visibility",
                locator=locator,
                original_error=e
            )

    def _wait_for_clickable(self, locator, timeout=None):
        """ Element bosiladigan holatda ekanligini tekshirish """
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            return element

        except StaleElementReferenceException as e:
            self.logger.warning(f"{page_name}: Element bosiladigan holatga kelishda DOM da yangilandi: {locator}")
            raise ElementStaleError(
                message="Element bosiladigan holatga kelishda DOM da yangilandi",
                locator=locator,
                original_error=e
            )
        except TimeoutException as e:
            self.logger.warning(f"{page_name}: Element {timeout}s ichida bosiladigan holga kelmadi: {locator}")
            raise ElementNotClickableError(
                message="Element bosilmaydigan holatda",
                locator=locator,
                original_error=e
            )
        except Exception as e:
            self.logger.warning(f"{page_name}: Element bosilishi da kutilmagan xato: {str(e)}")
            raise ElementInteractionError(
                message="Kutilmagan xatolik - Clickable",
                locator=locator,
                original_error=e
            )

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
        self.logger.debug(f"{page_name}: Click started: {locator}")

        attempt = 0
        while attempt < retries:
            try:
                self._wait_for_all_loaders(log_text='Click')

                element_dom = self._wait_for_presence(locator)
                self._scroll_to_element(element_dom, locator)
                self._wait_for_visibility(locator)
                element_clickable = self._wait_for_clickable(locator)

                if self._click(element_clickable, locator):
                    return True

                self.logger.warning(f"{page_name}: Click ishlamadi, Retry Click urinilmoqda...")
                time.sleep(retry_delay)

                element_clickable = self._wait_for_clickable(locator)
                if element_clickable:
                    if self._click(element_clickable, locator, retry=True):
                        return True

                self.logger.info(f"{page_name}: Click va Retry Click ishlamadi, majburiy JS Click qilinmoqda...")
                time.sleep(retry_delay)

                element_dom = self._wait_for_presence(locator)
                if element_dom:
                    if self._click_js(element_dom, locator):
                        return True

                raise ElementNotClickableError(
                    "Element barcha usullar bilan bosilmadi",
                    locator=locator
                )
            except (ElementStaleError, ScrollError, ElementVisibilityError, ElementNotClickableError, ElementNotFoundError) as e:
                if attempt == retries - 1:
                    self.logger.error(f"{page_name}: {e.message}")
                    self.take_screenshot(f"{page_name.lower()}_click_error")
                    raise

                self.logger.warning(f"{page_name}: {e.message}, qayta urinish ({attempt + 1}/{retries})")
                time.sleep(retry_delay)
                attempt += 1
                continue

            except LoaderTimeoutError as e:
                self.logger.error(f"{page_name}: {e.message}")
                self.take_screenshot(f"{page_name.lower()}_click_error")
                raise

        raise ElementInteractionError(
            f"Element bosilmadi ({attempt} urinish): {locator}",
            locator=locator
        )

    # Wait -------------------------------------------------------------------------------------------------------------

    def wait_for_element_visible(self, locator, timeout=None, retries=3, retry_delay=0.5):
        """Elementni ko'rinishini kutish funksiyasi"""
        page_name = self.__class__.__name__
        self.logger.debug(f"{page_name}: Visible started: {locator}")

        timeout = timeout or self.default_timeout
        attempt = 0

        while attempt < retries:
            try:
                self._wait_for_all_loaders(log_text='Visible')

                element_dom = self._wait_for_presence(locator)
                self._scroll_to_element(element_dom, locator)
                element = self._wait_for_visibility(locator, timeout)

                if element:
                    self.logger.info(f"⏺ {page_name}: Element topildi: {locator}")
                    return element

                raise ElementInteractionError(
                    message="Element ko'rinmadi",
                    locator=locator
                )

            except (ElementStaleError, ScrollError, ElementNotFoundError, ElementVisibilityError) as e:
                if attempt == retries - 1:
                    self.logger.error(f"{page_name}: {e.message}")
                    self.take_screenshot(f"{page_name.lower()}_visibility_error")
                    raise

                self.logger.warning(f"{page_name}: {e.message}, qayta urinish ({attempt + 1}/{retries})")
                time.sleep(retry_delay)
                attempt += 1
                continue

            except LoaderTimeoutError as e:
                self.logger.error(f"{page_name}: {e.message}")
                self.take_screenshot(f"{page_name.lower()}_visibility_error")
                raise

            except Exception as e:
                self.logger.error(f"{page_name}: Kutilmagan xato: {str(e)}")
                self.take_screenshot(f"{page_name.lower()}_visibility_error")
                raise ElementInteractionError(
                    message=f"Kutilmagan xato: {str(e)}",
                    locator=locator,
                    original_error=e
                )

        raise ElementInteractionError(
            f"Element topilmadi ({attempt} urinish): {locator}",
            locator=locator
        )

    # ------------------------------------------------------------------------------------------------------------------
    def _wait_for_presence_all(self, locator, timeout=None):
        """Elementlar ro'yxatini kutish funksiyasi."""
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        try:
            elements = WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))
            return elements

        except StaleElementReferenceException as e:
            self.logger.warning(f"{page_name}: Elementlar ro'yhati DOM da yangilandi: {locator}")
            raise ElementStaleError(
                message="Elementlar ro'yhati DOM da yangilandi",
                locator=locator,
                original_error=e
            )

        except TimeoutException as e:
            self.logger.error(f"{page_name}: Elementlar ro'yhati topilmadi: {locator}")
            raise ElementNotFoundError(
                message="Elementlar ro'yhati topilmadi",
                locator=locator,
                original_error=e
            )

        except Exception as e:
            self.logger.error(f"{page_name}: Elementlarni ro'yhatini qidirishda kutilmagan xato: {e}")
            raise ElementInteractionError(
                message=f"Elementlarni ro'yhatini qidirishda kutilmagan xato: {str(e)}",
                locator=locator,
                original_error=e
            )

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
            result = WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            if result:
                return True

            if error_message:
                self.logger.warning(f"{page_name}: Element hali ham ko'rinmoqda: {locator}")
            return False

        except StaleElementReferenceException as e:
            if error_message:
                self.logger.warning(f"{page_name}: Element DOM da yangilandi: {locator}")
            raise ElementStaleError(
                message="Element DOM da yangilandi",
                locator=locator,
                original_error=e
            )

        except TimeoutException as e:
            if error_message:
                self.logger.error(f"{page_name}: Element ko'rinmas bo'lmadi: {locator}")
            raise ElementVisibilityError(
                message="Element ko'rinmas bo'lmadi",
                locator=locator,
                original_error=e
            )

        except Exception as e:
            if error_message:
                self.logger.error(f"{page_name}: Element kutishda kutilmagan xato: {e}")
            raise ElementInteractionError(
                message=f"Kutilmagan xato: {str(e)}",
                locator=locator,
                original_error=e
            )

    # ------------------------------------------------------------------------------------------------------------------

    def input_text(self, locator, text, retries=3, retry_delay=1):
        """Element topib, matn kiritish funksiyasi"""
        page_name = self.__class__.__name__
        self.logger.debug(f"{page_name}: Matn kiritilmoqda: {locator}")

        attempt = 0

        while attempt < retries:
            try:
                self._wait_for_all_loaders(log_text='input_text')

                element_dom = self._wait_for_presence(locator)
                self._scroll_to_element(element_dom, locator)
                element_clickable = self._wait_for_clickable(locator)

                # Matn kiritish
                element_clickable.clear()
                element_clickable.send_keys(text)
                self.logger.info(f"⏺ {page_name}: Input: {locator} -> {text}")
                return True

            except ElementStaleError:
                self.logger.warning(
                    f"{page_name}: '{text}' elementi yangilandi, qayta urinish ({attempt + 1})...")
                attempt += 1
                time.sleep(retry_delay)
                continue

            except (ElementNotFoundError, ScrollError, ElementNotClickableError, LoaderTimeoutError) as e:
                self.logger.error(f"{page_name}: {e.message}")
                self.take_screenshot(f"{page_name.lower()}_input_error")
                raise

            except Exception as e:
                self.logger.error(f"{page_name}: Matn kiritishda kutilmagan xatolik: {str(e)}")
                self.take_screenshot(f"{page_name.lower()}_input_error")
                raise ElementInteractionError(
                    message=f"Matn kiritishda xatolik: {str(e)}",
                    locator=locator,
                    original_error=e
                )

    # ------------------------------------------------------------------------------------------------------------------

    def clear_element(self, locator):
        element = self._wait_for_clickable(locator)
        try:
            element.clear()
        except Exception:
            self.logger.error("clear_element: not clear.")

    # ------------------------------------------------------------------------------------------------------------------
    def get_text(self, locator):
        """Elementning matnini olish."""
        try:
            element_dom = self._wait_for_presence(locator)
            if not element_dom:
                return None

            self._scroll_to_element(element_dom, locator)
            element_visibility = self._wait_for_visibility(locator)

            return element_visibility.text if element_visibility else None

        except Exception as e:
            self.logger.error(f"Element matnini olishda xato: {str(e)}")
            return None

    # ------------------------------------------------------------------------------------------------------------------

    def get_numeric_value(self, locator):
        """Elementdan raqamli qiymatni ajratib olish va float formatiga o'tkazish."""
        text = self.get_text(locator)
        if text is None:
            self.logger.error(f"get_numeric_value: Element topilmadi - {locator}")
            return None

        text = text.strip()
        numeric_value = re.sub(r'[^0-9.]', '', text)

        if numeric_value.count('.') > 1:
            self.logger.error(f"get_numeric_value: Noto'g'ri format - {text}")
            return None

        try:
            return float(numeric_value) if numeric_value else 0
        except ValueError as e:
            self.logger.error(f"get_numeric_value: Float ga o'tkazishda xato - {str(e)}")
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
            raise
        except Exception as e:
            self.logger.error(f"Yangi oyna ochishda xato: {str(e)}", exc_info=True)
            self.take_screenshot("open_new_window_error")
            raise WebDriverException(f"Yangi oyna ochishda xato: {str(e)}")

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
                if self._wait_for_all_loaders(timeout=60, log_text='switch_to_previous_window'):
                    self.logger.info("Avvalgi oynaga qaytildi")
                    return True
            else:
                self.logger.error("Avvalgi oyna topilmadi")
                return False
        except LoaderTimeoutError:
            raise
        except Exception as e:
            self.logger.error(f"Avvalgi oynaga qaytishda xato: {str(e)}", exc_info=True)
            self.take_screenshot("switch_to_previous_window_error")
            return False

    # ------------------------------------------------------------------------------------------------------------------
    def refresh_page(self) -> bool:
        """Joriy sahifani yangilash."""
        try:
            self.driver.refresh()

            try:
                self._wait_for_all_loaders(timeout=60, log_text='refresh_page')
                self.logger.info("Sahifa muvaffaqiyatli yangilandi")
                return True
            except LoaderTimeoutError:
                self.logger.error("Sahifa yangilangandan so'ng to'liq yuklanmadi")
                raise

        except Exception as e:
            self.logger.error(f"Sahifani yangilashda xato: {str(e)}", exc_info=True)
            self.take_screenshot("refresh_page_error")
            return False

    # ------------------------------------------------------------------------------------------------------------------

    def current_date(self, add_days=0):
        """Joriy vaqtni qaytaruvchi funksiya."""

        current_date = datetime.now()
        future_date = current_date + timedelta(days=add_days)
        formatted_date = future_date.strftime("%d.%m.%Y %H:%M:%S")
        return formatted_date

    # ------------------------------------------------------------------------------------------------------------------
    def click_options(self, input_locator, options_locator, element, scroll=30):
        """
        Dropdown bilan ishlash uchun funksiya.

        Args:
            input_locator: Dropdown ochish uchun bosiladigan element lokatori
            options_locator: Dropdown ichidagi variantlar lokatori
            element: Tanlanishi kerak bo'lgan element matni
            scroll: Scroll qilish uchun maksimal urinishlar soni (default: 10)

        Returns:
            bool: Muvaffaqiyatli bajarilganda True, aks holda False

        Raises:
            ElementNotFoundError: Element topilmaganda
            ElementNotClickableError: Element bosilmaydigan holatda bo'lganda
            ScrollError: Elementga scroll qilib bo'lmaganda
            ElementVisibilityError: Element ko'rinmas bo'lmaganda
        """
        page_name = self.__class__.__name__
        self.logger.debug(f"{page_name}: Dropdown bilan ishlanmoqda: {input_locator}")

        try:
            # 1. Dropdown ochish
            if not self.click(input_locator):
                raise ElementNotClickableError(
                    message="Dropdown ochib bo'lmadi",
                    locator=input_locator
                )

            # 2. Optionlarni yuklanishini kutish
            options = self._wait_for_presence_all(options_locator)
            if not options:
                raise ElementNotFoundError(
                    message="Dropdown variantlari yuklanmadi",
                    locator=options_locator
                )

            # 3. Element topish va bosish funksiyasi
            def find_and_click_option(options_list):
                element_str = str(element).strip()
                for option in options_list:
                    if option.text.strip() == element_str:
                        try:
                            option.click()
                            self.logger.info(f"⏺ {page_name}: Element '{element}' bosildi")
                            return True
                        except Exception as e:
                            raise ElementNotClickableError(
                                message=f"Elementni bosib bo'lmadi: {str(e)}",
                                locator=options_locator
                            )
                return False

            # 4. Elementni qidirish
            if find_and_click_option(options):
                return self._check_dropdown_closed(options_locator)

            # 5. Scroll qilib qidirish
            self.logger.info(f"{page_name}: Element '{element}' topilmadi. Scroll qilinmoqda...")
            dropdown_container = self._find_visible_container(options_locator)
            if not dropdown_container:
                raise ElementNotFoundError(
                    message="Dropdown konteyner topilmadi",
                    locator=options_locator
                )

            # 6. Scroll bilan qidirish
            last_height = 0
            for attempt in range(scroll):
                try:
                    self.driver.execute_script("arguments[0].scrollBy(0, 300);", dropdown_container)
                    time.sleep(0.5)

                    options = self._wait_for_presence_all(options_locator)
                    if options and find_and_click_option(options):
                        return self._check_dropdown_closed(options_locator)

                    new_height = self.driver.execute_script("return arguments[0].scrollHeight", dropdown_container)
                    if new_height == last_height:
                        raise ElementNotFoundError(
                            message=f"Element '{element}' scroll tugagandan keyin ham topilmadi",
                            locator=options_locator
                        )
                    last_height = new_height

                except ElementStaleError:
                    if attempt == scroll - 1:
                        raise
                    continue

            raise ElementNotFoundError(
                message=f"Element '{element}' {scroll} marta scroll qilingandan keyin ham topilmadi",
                locator=options_locator
            )

        except (ElementNotFoundError, ElementNotClickableError, ScrollError) as e:
            self.logger.error(f"{page_name}: {e.message}")
            self.take_screenshot(f"{page_name.lower()}_click_options_error")
            raise

        except Exception as e:
            self.logger.error(f"{page_name}: Kutilmagan xato: {str(e)}")
            self.take_screenshot(f"{page_name.lower()}_click_options_error")
            raise ElementInteractionError(
                message=f"Kutilmagan xato: {str(e)}",
                locator=options_locator,
                original_error=e
            )

    def _check_dropdown_closed(self, options_locator):
        """Dropdown yopilganligini tekshirish."""

        page_name = self.__class__.__name__
        try:
            # Turli yopish usullarini sinash
            self.driver.execute_script("document.body.click();")
            time.sleep(0.1)
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            time.sleep(0.1)

            if not self._wait_for_invisibility_of_locator(options_locator):
                raise ElementVisibilityError(
                    message="Dropdown yopilmadi",
                    locator=options_locator
                )
            return True

        except ElementVisibilityError as e:
            self.logger.error(f"{page_name}: {e.message}")
            self.take_screenshot(f"{page_name.lower()}_dropdown_close_error")
            raise

        except Exception as e:
            self.logger.error(f"{page_name}: Dropdown yopishda kutilmagan xato: {str(e)}")
            self.take_screenshot(f"{page_name.lower()}_dropdown_close_error")
            raise ElementInteractionError(
                message=f"Dropdown yopishda kutilmagan xato: {str(e)}",
                locator=options_locator,
                original_error=e
            )

    def _find_visible_container(self, options_locator):
        """Dropdown uchun ko'rinadigan konteynerni topish."""

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
                containers = self.driver.find_elements(By.XPATH, selector)
                for container in containers:
                    if container.is_displayed():
                        return container

            raise ElementNotFoundError(
                message="Ko'rinadigan dropdown konteyner topilmadi",
                locator=(By.XPATH, " | ".join(possible_container_selectors))
            )

        except ElementNotFoundError as e:
            self.logger.error(f"{page_name}: {e.message}")
            raise

        except Exception as e:
            self.logger.error(f"{page_name}: Konteyner qidirishda kutilmagan xato: {str(e)}")
            raise ElementInteractionError(
                message=f"Konteyner qidirishda kutilmagan xato: {str(e)}",
                locator=options_locator,
                original_error=e
            )

    # ------------------------------------------------------------------------------------------------------------------

    def find_row_and_click(self, element_name, timeout=5, xpath_pattern=None, checkbox=False):
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

        while attempt < 3:
            try:
                self._wait_for_all_loaders(log_text='find_and_click_row')
                try:
                    elements = self._wait_for_presence_all(row_locator, timeout)
                except ElementNotFoundError:
                    if not limit_raised:
                        self.logger.info(f"{page_name}: '{element_name}' topilmadi, jadval limiti oshirilmoqda...")
                        limit_change_button = self._wait_for_clickable(limit_change_button)
                        limit_option = self._wait_for_clickable(limit_option)
                        if self._click(limit_change_button, limit_change_button) and \
                                self._click(limit_option, limit_option):
                            self.logger.info("Limit oshirildi -> ro'yhatda 1000 ta elemet bor")
                        limit_raised = True
                        continue
                    elif not search_used:
                        self.logger.warning(
                            f"{page_name}: Limit oshirilganidan keyin ham '{element_name}' topilmadi. Qidiruvga berilmoqda...")
                        if element := self._wait_for_clickable(search_input):
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
                element = self._wait_for_clickable(row_locator)
                if not self._click(element, row_locator):
                    self.logger.warning("Element -> JS click orqali bosiladi")
                    elements = self._wait_for_presence_all(row_locator, timeout)
                    target_element = elements[0]
                    self._click_js(target_element, row_locator)

                if checkbox:
                    element_dom = self._wait_for_presence(checkbox_locator)
                    self._click_js(element_dom)
                return True

            except ElementStaleError:
                self.logger.warning(
                    f"{page_name}: '{element_name}' element yangilandi, qayta urinish ({attempt + 1}/3)")
                attempt += 1
                continue

            except LoaderTimeoutError:
                raise

            except Exception as e:
                self.logger.error(f"{page_name}: Kutilmagan xatolik yuz berdi: {str(e)}")
                self.take_screenshot(f"{page_name.lower()}_find_row_error")
                raise

    # ------------------------------------------------------------------------------------------------------------------
