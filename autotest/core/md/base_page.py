import os
import re
import time
import allure
import logging
import inspect
from datetime import datetime, timedelta
from selenium.webdriver import Keys
from colorama import Fore, Style, init
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, \
    ElementClickInterceptedException, ElementNotInteractableException, WebDriverException, \
    StaleElementReferenceException

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    InvalidSelectorException,
    WebDriverException,
    NoAlertPresentException,
    UnexpectedAlertPresentException,
    InvalidElementStateException,
    NoSuchWindowException,
    NoSuchFrameException,
    ElementNotSelectableException,
    ImeActivationFailedException,
    ImeNotAvailableException,
    InsecureCertificateException,
    InvalidCookieDomainException,
    UnableToSetCookieException,
    UnexpectedTagNameException,
    InvalidSessionIdException,
    SessionNotCreatedException,
)

init(autoreset=True)  # Ranglarni avtomatik reset qilish


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.test_name = self._get_test_name()
        self._configure_logging()
        self.default_timeout = 5
        self.actions = ActionChains(driver)

    def _get_test_name(self):
        """Test nomini avtomatik aniqlash: funksiyaning yoki sinfning nomini topish."""

        stack = inspect.stack()
        for frame in stack:
            # Test funksiyasi "test_" bilan boshlanadi
            if frame.function.startswith("test"):
                return frame.function
        return "unknown_test"

    def _configure_logging(self):
        """
        Logging konfiguratsiyasi: loglarni yagona faylga yozish
        va test nomi bilan ajratib ko‘rsatish.
        """
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Log faylining yagona nomi
        log_file_name = f"{log_dir}/{self.test_name}_{datetime.now().strftime('%Y_%m_%d')}.log"

        # Logger yaratish
        self.logger = logging.getLogger(self.test_name)
        self.logger.setLevel(logging.INFO)

        # Eski handlerlarni tozalash
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # Log format: test nomini kiritish
        log_format = f"%(asctime)s - [%(levelname)s] - {self.test_name} - %(message)s"

        # Rangli konsol handler
        class ColorFormatter(logging.Formatter):
            def format(self, record):
                log_message = super().format(record)
                if record.levelno == logging.INFO:
                    return f"{Fore.GREEN}{log_message}{Style.RESET_ALL}"
                elif record.levelno == logging.WARNING:
                    return f"{Fore.YELLOW}{log_message}{Style.RESET_ALL}"
                elif record.levelno == logging.ERROR:
                    return f"{Fore.RED}{log_message}{Style.RESET_ALL}"
                elif record.levelno == logging.DEBUG:
                    return f"{Fore.CYAN}{log_message}{Style.RESET_ALL}"
                return log_message

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = ColorFormatter(log_format)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File handler
        file_handler = logging.FileHandler(log_file_name, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(log_format)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Avoid propagating logs to the root logger
        self.logger.propagate = False

    # Errors -----------------------------------------------------------------------------------------------------------

    def errors(self, exception, error_description=""):
        """Selenium xatoliklarini boshqarish uchun yordamchi funksiya."""

        exception_map = {
            TimeoutException: "❌ Elementni topish yoki yuklash uchun vaqt tugadi.",
            NoSuchElementException: "❌ Element mavjud emas.",
            StaleElementReferenceException: "⚠️ DOM yangilangani sababli element mavjud emas.",
            ElementClickInterceptedException: "⚠️ Element bloklangan yoki ustida boshqa element bor.",
            ElementNotInteractableException: "❌ Element foydalanuvchi bilan ishlashga tayyor emas.",
            InvalidSelectorException: "❌ Lokator noto‘g‘ri yoki sintaksisda xatolik mavjud.",
            WebDriverException: "🚨 Selenium WebDriver xatoligi.",
            NoAlertPresentException: "❌ Kutilgan alert dialog topilmadi.",
            UnexpectedAlertPresentException: "⚠️ Kutilmagan alert paydo bo‘ldi.",
            InvalidElementStateException: "⚠️ Element holati o‘zgartirilmasligi mumkin.",
            NoSuchWindowException: "❌ Ko‘rsatilgan oyna mavjud emas.",
            NoSuchFrameException: "❌ Ko‘rsatilgan frame mavjud emas.",
            ElementNotSelectableException: "⚠️ Element tanlanishi mumkin emas.",
            ImeActivationFailedException: "❌ IME faollashtirilmadi.",
            ImeNotAvailableException: "❌ IME tizimda mavjud emas.",
            InsecureCertificateException: "⚠️ Xavfsiz bo‘lmagan sertifikat topildi.",
            InvalidCookieDomainException: "❌ Cookie noto‘g‘ri domen uchun o‘rnatilgan.",
            UnableToSetCookieException: "❌ Cookie o‘rnatib bo‘lmadi.",
            UnexpectedTagNameException: "⚠️ Elementning tegi kutilmagan turda.",
            InvalidSessionIdException: "❌ Sessiya identifikatori noto‘g‘ri yoki muddati o‘tgan.",
            SessionNotCreatedException: "🚨 Selenium sessiyasi yaratilmagan.",
        }

        error_message = exception_map.get(type(exception), "❓ Noma’lum xatolik yuz berdi.")
        if error_description:
            error_message += f" Amal: {error_description}"
        self.logger.error(error_message)
        return error_message

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

    # Retry ------------------------------------------------------------------------------------------------------------

    def retry_with_delay(self, func, retries=3, retry_delay=1, *args, **kwargs):
        """Retry mexanizmi: Funksiyani qayta urinish bilan bajarish."""

        last_exception = None
        for attempt in range(retries):
            self.logger.debug(f"Funksiya {func.__name__} chaqirildi, urinish {attempt + 1}")
            try:
                result = func(*args, **kwargs)
                if result:
                    self.logger.debug(f"{func.__name__} natijasi: {result}")
                    return result  # Muvaffaqiyatli natija
            except Exception as e:
                last_exception = e
                self.logger.warning(
                    f"[Urinish {attempt + 1}] {func.__name__} bajarilmadi, {retry_delay} soniyadan keyin qayta urinish..."
                )
            time.sleep(retry_delay)
        self.logger.error(
            f"Funksiya {func.__name__} barcha {retries} urinishdan so‘ng muvaffaqiyatsiz tugadi: {last_exception}"
        )
        return False

    # Halper function --------------------------------------------------------------------------------------------------

    def _wait_for_page_load(self, timeout=None):
        """Sahifa to'liq yuklanganligini kutish."""

        timeout = timeout or self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete")
        except TimeoutException:
            self.logger.error(f"Sahifa to'liq yuklanmadi. Kutish vaqti tugadi: {timeout}s")
            return False

    def _wait_for_overlay_absence(self, timeout=None):
        """Bloklovchi element yo‘q bo‘lishini kutadi."""

        timeout = timeout or self.default_timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "block-ui-overlay")))
        except TimeoutException:
            self.logger.error(f"Blocklovchi element yo'qolmadi.")
            return False

    def _check_spinner_absence(self, timeout=None):
        """Yuklash indikatorlarining mavjud emasligini tekshirish."""

        timeout = timeout or self.default_timeout
        locator = (
            By.XPATH, "//div[contains(@class, 'block-ui-overlay') or contains(@class, 'block-ui-message-container')]")
        start_time = time.time()
        try:
            # Spinner yo'qligini yoki ko'rinmasligini kutish
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
            # elapsed_time = time.time() - start_time
            # self.logger.info(f"Yuklash indikatori {elapsed_time:.2f}s ichida muvaffaqiyatli yo'qoldi: {locator}.")
            return True
        except TimeoutException:
            elapsed_time = time.time() - start_time
            self.logger.warning(f"Yuklash indikatori hali ham mavjud yoki ko'rinmoqda ({elapsed_time:.2f}s o'tdi): {locator}.")
            return False

    def _wait_for_all_loaders(self, timeout=None):
        """Sahifadagi barcha yuklovchi elementlarni kuzatish"""

        timeout = timeout or self.default_timeout
        return self._wait_for_page_load(timeout) and \
            self._wait_for_overlay_absence(timeout) and \
            self._check_spinner_absence(timeout)

    # ------------------------------------------------------------------------------------------------------------------

    def _click_js(self, element, locator=None):
        """JavaScript orqali majburiy bosish."""

        try:
            self.driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as e:
            self.logger.error(f"JavaScript orqali bosishda xatolik: {locator} \n{e}")
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
    def _is_element_covered(self, element):
        """Element boshqa element tomonidan qoplanganligini aniqlash."""

        rect = self.driver.execute_script(
            "var rect = arguments[0].getBoundingClientRect();"
            "return {top: rect.top, left: rect.left, bottom: rect.bottom, right: rect.right};", element)
        x = (rect['left'] + rect['right']) // 2
        y = (rect['top'] + rect['bottom']) // 2

        # O‘rta nuqtani tekshirish
        covered_element = self.driver.execute_script(
            "return document.elementFromPoint(arguments[0], arguments[1]);", x, y)
        return covered_element != element

    def _get_covering_element(self, element):
        """Element ustini qoplagan elementni aniqlash."""

        rect = self.driver.execute_script(
            "var rect = arguments[0].getBoundingClientRect();"
            "return {top: rect.top, left: rect.left, bottom: rect.bottom, right: rect.right};", element)
        x = (rect['left'] + rect['right']) // 2
        y = (rect['top'] + rect['bottom']) // 2

        # O‘rta nuqtani tekshirish
        covering_element = self.driver.execute_script(
            "return document.elementFromPoint(arguments[0], arguments[1]);", x, y)
        return covering_element

    def _hide_covering_element(self, covering_element):
        """Qoplovchi elementni vaqtinchalik yashirish."""

        self.driver.execute_script("arguments[0].style.display = 'none';", covering_element)
        self.logger.info("Qoplovchi element vaqtinchalik yashirildi.")

    # ------------------------------------------------------------------------------------------------------------------

    def _wait_for_presence(self, locator, timeout=None):
        """Locator DOMda mavjud ekanligini tekshirish."""

        timeout = timeout or self.default_timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException as e:
            self.logger.error(f"Locator DOM da topilmadi: {locator}. Xato: {e}")
            raise WebDriverException(f"Locator DOM da topilmadi: {locator}")

    def _scroll_to_element(self, element, locator):
        """Element ga scroll qilish."""

        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(0.5)
            return element

        except Exception:
            self.logger.warning(f"Scroll qilishda xatolik yuz berdi. Element yangilandi")
            try:
                element_dom = self._wait_for_presence(locator)
                self.logger.info(f"Qayta Scroll qilinadi.")
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element_dom)
                time.sleep(0.5)
                return element_dom
            except Exception as e:
                self.logger.error(f"Scroll: xatolik yuz berdi: {e}")
                raise WebDriverException(f"Scroll qilishda xatolik: {e}")

    def _wait_for_visibility(self, locator, timeout=None):
        """Locator ni interfeysda ko‘rinishini tekshirish."""

        timeout = timeout or self.default_timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return element
        except TimeoutException as e:
            self.logger.warning(f"Locator interfeysda ko‘rinmadi: {locator}. Xato: {e}")
            raise WebDriverException(f"Locator interfeysda ko‘rinmadi: {locator}")

    def _wait_for_clickable(self, locator, timeout=None):
        """Locatorni ni bosish uchun tayyor ekanligini tekshirish."""

        timeout = timeout or self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            self.logger.error(f"Locator bosishga tayyor emas")
            return None

    # ------------------------------------------------------------------------------------------------------------------

    def _is_element_visible(self, locator):
        """Element CSS orqali tekshirish"""
        try:
            element = self._wait_for_presence(locator)
            is_displayed = self.driver.execute_script(
                "return window.getComputedStyle(arguments[0]).getPropertyValue('display') !== 'none' && "
                "window.getComputedStyle(arguments[0]).getPropertyValue('visibility') !== 'hidden';", element)
            self.logger.info(f"Element CSS orqali tekshirildi: {is_displayed}")
            return is_displayed

        except Exception as e:
            self.logger.error(f"Element CSS orqali tekshirishda xatolik: {e}")
            return None

    def _wait_for_presence_all(self, locator, timeout=None):
        """Elementlar ro‘yxatini kutish."""

        timeout = timeout or self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            self.logger.warning(f"Elementlar topilmadi: {locator}")
            return []

    def _wait_for_invisibility_of_element(self, element, timeout=None):
        """Element ni ko'rinmas bo'lishini kutish."""

        timeout = timeout or self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element(element))
        except TimeoutException as e:
            self.logger.error(f"Element sahifadan yo'qolmadi: {e}")
            return False

    def _wait_for_invisibility_of_locator(self, locator, timeout=None):
        """Locator ni ko'rinmas bo'lishini kutish."""

        timeout = timeout or self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
        except TimeoutException as e:
            self.logger.error(f"Locator sahifadan yo'qolmadi")
            return False

    def _is_element_visible_and_interactable(self, element):
        """Elementning ko'rinishi va o'lchami tekshirish"""

        try:
            if element.is_displayed() and element.size['width'] > 0 and element.size['height'] > 0:
                return True

            self.logger.warning("Element ko'rinmayapti yoki hajmi nol.")
            return False

        except StaleElementReferenceException:
            self.logger.warning("Element eskirgan (stale)")
            return False
        except Exception as e:
            self.logger.warning(f"Elementning ko'rinishi va o'lchami tekshirishda xatolik: {e}")
            return False

    def _wait_for_element_with_size(self, locator, timeout=10):
        """Element o‘lchami nol emasligini kutadi."""
        element = WebDriverWait(self.driver, timeout).until(
            lambda driver: (
                    (el := driver.find_element(*locator)).size['width'] > 0 and
                    el.size['height'] > 0 and el
            )
        )
        return element

    def _wait_for_stable_dom(self, timeout=None, check_interval=0.5):
        """DOM ning barqarorligini tekshirish uchun. Sahifa o'zgarishlarini to'xtashini kutadi."""

        timeout = timeout or self.default_timeout
        start_time = time.time()
        prev_dom_snapshot = self.driver.page_source  # DOM snapshot olish

        while time.time() - start_time < timeout:
            time.sleep(check_interval)
            current_dom_snapshot = self.driver.page_source
            if current_dom_snapshot == prev_dom_snapshot:
                self.logger.info("DOM barqaror holatda.")
                return True
            prev_dom_snapshot = current_dom_snapshot

        self.logger.warning("DOM barqaror bo‘lishini kutish vaqti tugadi.")
        return False

    def _wait_for_dom_ready(self, timeout=None):
        """DOM ning tayyor ekanligini tekshirish (document.readyState va jQuery faol emasligini)."""

        timeout = timeout or self.default_timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script(
                    """
                    return document.readyState === 'complete' &&
                           (typeof jQuery === 'undefined' || jQuery.active === 0);
                    """
                )
            )
            self.logger.info("DOM barqaror holatga keldi (document.readyState = 'complete').")
            return True
        except TimeoutException:
            self.logger.warning("DOMni barqaror holatga kutish vaqti tugadi.")
            return False

    # Click ------------------------------------------------------------------------------------------------------------

    # def click(self, locator, timeout=None, retries=3, retry_delay=1):
    #     """Elementni bosish funksiyasi"""
    #
    #     timeout = timeout or self.default_timeout
    #     wait = WebDriverWait(self.driver, timeout)
    #     attempt = 0
    #     last_exception = None
    #
    #     while attempt < retries:
    #         try:
    #             self.logger.info(f"Click {attempt + 1}/{retries}: Sahifa yuklanganligini tekshirish...")
    #             wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    #
    #             self.logger.info(f"Click {attempt + 1}/{retries}: Sahifada loading indikatorini tekshirish...")
    #             self._check_spinner_absence(timeout=timeout)
    #
    #             self.logger.info(f"Click {attempt + 1}/{retries}: Element mavjudligini kutish... {locator}")
    #             element = wait.until(EC.presence_of_element_located(locator))
    #
    #             self.logger.info(f"Click {attempt + 1}/{retries}: Element ko‘rinishini kutish... {locator}")
    #             element = wait.until(EC.visibility_of_element_located(locator))
    #
    #             self.logger.info(f"Click {attempt + 1}/{retries}: Elementga scroll qilish... {locator}")
    #             self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    #             time.sleep(0.5)
    #
    #             self.logger.info(f"Click {attempt + 1}/{retries}: Element bosishga tayyorligini kutish... {locator}")
    #             element = wait.until(EC.element_to_be_clickable(locator))
    #
    #             self.logger.info(f"Click {attempt + 1}/{retries}: Elementni bosish... {locator}")
    #             try:
    #                 element.click()
    #                 self.logger.info(f"Element muvaffaqiyatli bosildi: {locator}")
    #             except (ElementClickInterceptedException, ElementNotInteractableException) as e:
    #                 self.logger.warning(f"Oddiy click ishlamadi: {e}. JavaScript orqali bosilmoqda...")
    #                 try:
    #                     self.driver.execute_script("arguments[0].click();", element)
    #                     self.logger.info(f"Element JavaScript yordamida muvaffaqiyatli bosildi: {locator}")
    #                 except WebDriverException as js_exc:
    #                     self.logger.warning(f"JavaScript click ishlamadi: {js_exc}. ActionChains orqali bosilmoqda...")
    #                     try:
    #                         self.actions.move_to_element(element).click().perform()
    #                         self.logger.info(f"Element ActionChains yordamida muvaffaqiyatli bosildi: {locator}")
    #                     except WebDriverException as ac_exc:
    #                         self.logger.warning(f"ActionChains click ishlamadi: {ac_exc}. Offset bilan bosilmoqda...")
    #                         location = element.location
    #                         size = element.size
    #                         x = location['x'] + size['width'] // 2
    #                         y = location['y'] + size['height'] // 2
    #                         self.actions.move_by_offset(x, y).click().perform()
    #                         self.logger.info(f"Element offset yordamida muvaffaqiyatli bosildi: {locator}")
    #
    #             return True
    #
    #         except StaleElementReferenceException:
    #             self.logger.warning(
    #                 f"StaleElementReferenceException: Element yangilandi va topilmadi. Click {attempt + 1}/{retries}")
    #             attempt += 1
    #             time.sleep(retry_delay)
    #
    #         except TimeoutException:
    #             self.logger.warning(f"TimeoutException: Elementni kutish vaqti tugadi. Click {attempt + 1}/{retries}")
    #             attempt += 1
    #             time.sleep(retry_delay)
    #
    #         except Exception as e:
    #             self.logger.error(f"Kutilmagan xatolik: {e}. Click {attempt + 1}/{retries}")
    #             attempt += 1
    #             time.sleep(retry_delay)
    #
    #     # Muvaffaqiyatsizlikdan keyin
    #     error_message = f"❌Click muvaffaqiyatsiz yakunlandi: {last_exception}"
    #     self.logger.error(error_message)
    #     self.take_screenshot("click_error")
    #     raise AssertionError(error_message)

    def click(self, locator, retries=3, retry_delay=1):
        """Elementni bosish funksiyasi"""

        attempt = 0
        last_exception = None

        while attempt < retries:
            try:
                self._wait_for_all_loaders()
                self._wait_for_async_operations()
                element_dom = self._wait_for_presence(locator)
                self._scroll_to_element(element=element_dom, locator=locator)
                element_visibility = self._wait_for_visibility(locator)
                element_clickable = self._wait_for_clickable(locator)

                # ------------------------------------------------------------------------------------------------------

                try:
                    element_clickable.click()
                    self.logger.info(f"✅Click: {locator}")
                except WebDriverException as a_exc:
                    last_exception = a_exc
                    self.logger.warning(f"❗️Click ishlamadi: {locator}")
                    # self.logger.warning(f"❌Error: {a_exc}")
                    try:
                        time.sleep(1)
                        element_clickable = self._wait_for_clickable(locator)
                        element_clickable.click()
                        self.logger.info(f"✅Retry Click: {locator}")
                    except WebDriverException as b_exc:
                        last_exception = b_exc
                        self.logger.warning(f"❗️Retry Click ishlamadi: {locator}")
                        # self.logger.warning(f"❌Error: {b_exc}")
                        try:
                            element_dom = self._wait_for_presence(locator)
                            self._click_js(element_dom)
                            self.logger.info(f"✅JavaSkript click: {locator}")
                        except WebDriverException as d_exc:
                            last_exception = d_exc
                            self.logger.warning(f"❗JavaSkript ishlamadi: {locator}")
                            # self.logger.warning(f"❌Error: {d_exc}")
                            try:
                                element_dom = self._wait_for_presence(locator)
                                self._click_js(element_dom)
                                self.logger.info(f"✅Retry JavaSkript click: {locator}")
                            except WebDriverException as e_exc:
                                last_exception = e_exc
                                self.logger.warning(f"❗Retry JavaSkript ishlamadi: {locator}")
                                self.logger.warning(f"❌Error: {e_exc}")
                return True

            except StaleElementReferenceException as e:
                last_exception = e
                self.logger.warning(
                    f"StaleElementReferenceException: Element yangilandi va topilmadi. Click {attempt + 1}/{retries}. {locator}")
                attempt += 1
                time.sleep(retry_delay)

            except TimeoutException as e:
                last_exception = e
                self.logger.warning(f"TimeoutException: Elementni kutish vaqti tugadi. Click {attempt + 1}/{retries}")
                attempt += 1
                time.sleep(retry_delay)

            except Exception as e:
                last_exception = e
                self.logger.warning(f"Kutilmagan xatolik: {e}. Click {attempt + 1}/{retries}")
                attempt += 1
                time.sleep(retry_delay)

        error_message = f"❌Click muvaffaqiyatsiz yakunlandi: {str(last_exception)}"
        self.logger.warning(error_message)
        self.take_screenshot("click_error")
        raise AssertionError(error_message)

    # Wait -------------------------------------------------------------------------------------------------------------

    def wait_for_element_visible(self, locator, timeout=None, retries=3, retry_delay=1):
        """Elementni ko'rinishini kutish uchun kuchaytirilgan funksiya."""

        timeout = timeout or self.default_timeout

        def try_with_retries(action, stage_name):
            attempt = 0
            while attempt < retries:
                try:
                    return action()

                except StaleElementReferenceException:
                    attempt += 1
                    logging.warning(f"{stage_name}: Element yangilandi. Qayta urinish {attempt}/{retries}")

                    if attempt == retries:
                        error_msg = f"{stage_name}: Element yangilandi va topilmadi"
                        logging.error(error_msg)
                        self.take_screenshot(f"stale_element_{stage_name}")
                        raise WebDriverException(error_msg)
                    time.sleep(retry_delay)

                except TimeoutException:
                    attempt += 1
                    if attempt == retries:
                        error_msg = (f"{stage_name}: Element {locator} "
                                     f"{timeout if timeout else self.default_timeout} "
                                     f"sekund ichida topilmadi")
                        logging.error(error_msg)
                        self.take_screenshot(f"timeout_{stage_name}")
                        raise WebDriverException(error_msg)
                    logging.warning(f"{stage_name}: Kutish vaqti tugadi. Qayta urinish {attempt}/{retries}")
                    time.sleep(retry_delay)

                except Exception as e:
                    attempt += 1
                    logging.warning(f"{stage_name}: Kutilmagan xatolik. Qayta urinish {attempt}/{retries}")

                    if attempt == retries:
                        error_msg = f"{stage_name}: Kutilmagan xatolik: {str(e)}"
                        logging.error(error_msg)
                        self.take_screenshot(f"unexpected_{stage_name}")
                        raise WebDriverException(error_msg)
                    time.sleep(retry_delay)

        # 1. Sahifa to'liq yuklanganligi tekshirish
        try_with_retries(lambda: self._wait_for_all_loaders(), "Sahifa yuklash")

        # 3. Element mavjudligi tekshirish
        element_dom = try_with_retries(lambda: self._wait_for_presence(locator), "Element DOM da mavjudligi")

        # 4. Elementni ko'rinadigan qismga scroll qilish
        try_with_retries(lambda: self._scroll_to_element(element=element_dom, locator=locator), "Element scroll qilish")

        # 5. Element ko'rinishi tekshirish
        element = try_with_retries(lambda: self._wait_for_visibility(locator), "Element interfeys da ko'rinishi")
        if not element:
            raise WebDriverException(f"Element ko‘rinadigan bo‘lmadi: {locator}")
        self.logger.info(f"✅Visible: {locator}")
        return element

    # ------------------------------------------------------------------------------------------------------------------

    def input_text(self, locator, text):
        try:
            element = self._wait_for_clickable(locator)

            if not element:
                self.logger.warning("input_text: not clickable: %s", locator)
                return False

            element.clear()
            element.send_keys(text)
            return True

        except Exception:
            self.logger.warning("input_text: not work: %s", locator)
            self.take_screenshot("input_text_error")
            return False

    # ------------------------------------------------------------------------------------------------------------------

    def input_text_elem(self, locator, elem_locator, timeout=None):
        try:
            if self.click(locator, timeout) and self.click(elem_locator, timeout):
                return True
            return False

        except Exception:
            self.logger.warning("input_text_elem: not clickable: %s", locator)
            self.take_screenshot("input_text_elem")
            return False

    # ------------------------------------------------------------------------------------------------------------------

    # def get_element(self, locator):
    #     return self.wait_for_element_visible(locator)

    # ------------------------------------------------------------------------------------------------------------------

    def get_text(self, locator):
        element = self.wait_for_element_visible(locator)
        return element.text

    # ------------------------------------------------------------------------------------------------------------------

    def clear_element(self, locator):
        element = self.wait_for_element_visible(locator)
        element.clear()
        time.sleep(0.1)

    # ------------------------------------------------------------------------------------------------------------------

    def get_numeric_value(self, locator):
        text = self.get_text(locator)
        if text is None:
            self.logger.warning("get_numeric_value: not work.")
            return None
        text = text.strip()
        numeric_value = re.sub(r'[^0-9.]', '', text)
        if numeric_value.count('.') <= 1:
            return float(numeric_value) if numeric_value else 0
        return None

    # ------------------------------------------------------------------------------------------------------------------

    def get_current_url(self):
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
            self.logger.warning("cut_url URL ni kesishda xatolik.")
            return current_url

    # ------------------------------------------------------------------------------------------------------------------

    def current_date(self, add_days=0):
        """Joriy vaqtni qaytaruvchi funksiya."""

        current_date = datetime.now()
        future_date = current_date + timedelta(days=add_days)
        formatted_date = future_date.strftime("%d.%m.%Y %H:%M:%S")
        return formatted_date

    # ------------------------------------------------------------------------------------------------------------------
    def click_options(self, input_locator, options_locator, element, timeout=None, scroll_enabled=True):
        """
        Dropdown bilan ishlash uchun funksiya: elementni topib, uni bosish va dropdownni yopish.
        options_locator = (By.XPATH, '//b-input[@name="contracts"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')
        """

        timeout = timeout or self.default_timeout
        try:
            # 1. Dropdown ochish
            if not self.click(input_locator):
                self.logger.warning("Dropdownni ochib bo'lmadi!")
                return False

            # 2. Optionlarni yuklanishini kutish
            options = self._wait_for_presence_all(options_locator, timeout=timeout)
            if not options:
                self.logger.warning("Dropdown variantlari yuklanmadi!")
                return False

            # 3. Elementni topish va bosish
            def find_and_click_option():
                element_str = str(element).strip()
                for option in options:
                    if option.text.strip() == element_str:
                        option.click()
                        return True
                return False

            if find_and_click_option():
                self.logger.info(f"Element '{element}' topildi va bosildi.")
            else:
                if scroll_enabled:
                    self.logger.info(f"Element '{element}' topilmadi. Scroll boshlanmoqda.")
                    dropdown_container = self._find_visible_container(options_locator)
                    if not dropdown_container:
                        self.logger.error("Dropdown konteyner topilmadi.")
                        return False

                    last_height = 0
                    for _ in range(5):  # Maksimal 5 marta scroll qilishga ruxsat
                        self.driver.execute_script("arguments[0].scrollBy(0, 300);", dropdown_container)
                        time.sleep(1)

                        options = self._wait_for_presence_all(options_locator, timeout=timeout)
                        if options and find_and_click_option():
                            self.logger.info(f"Element '{element}' scroll orqali topildi va bosildi.")
                            break
                        new_height = self.driver.execute_script("return arguments[0].scrollHeight", dropdown_container)
                        if new_height == last_height:
                            self.logger.warning("Scroll tugadi, lekin element topilmadi.")
                            return False
                        last_height = new_height
                else:
                    self.logger.warning(f"Element '{element}' topilmadi.")
                    return False

            # 4. Dropdown yopilishini tekshirish
            if not self.retry_with_delay(self._check_dropdown, retries=3, retry_delay=1,
                                         options_locator=options_locator, timeout=2):
                self.logger.error("Dropdown yopilmadi. Maksimal urinishlar amalga oshirildi.")
                return False

            self.logger.info("Dropdown muvaffaqiyatli yopildi.")
            return True

        except Exception as e:
            self.logger.error(f"Xatolik yuz berdi: {str(e)}")
            self.take_screenshot("click_options_error")
            return False

    def _find_visible_container(self, options_locator):
        """Dropdown uchun ko'rinadigan konteynerni topish."""

        possible_container_selectors = [
            "//div[contains(@class, 'hint-body')]",
            "//div[contains(@class, 'dropdown-menu')]",
            "//div[contains(@class, 'select-dropdown')]",
            f"{options_locator[1]}/ancestor::div[contains(@class, 'hint')]",
            f"{options_locator[1]}/ancestor::div[contains(@class, 'dropdown')]",
        ]

        for selector in possible_container_selectors:
            containers = self.driver.find_elements(By.XPATH, selector)
            for container in containers:
                if container.is_displayed():
                    return container

        self.logger.warning("Dropdown konteyner topilmadi.")
        return None

    def _check_dropdown(self, options_locator, timeout=None):
        """Dropdown yopilishini tekshirish va kerakli harakatlarni amalga oshirish."""

        try:
            # Turli yopish usullarini sinash
            self.driver.execute_script("document.body.click();")
            time.sleep(1)
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            time.sleep(1)

            # Dropdown yopilganligini tekshirish
            return self._wait_for_invisibility_of_element(options_locator, timeout=timeout)

        except Exception as e:
            self.logger.error(f"Dropdownni yopishda xatolik: {str(e)}")
            return False

    # ------------------------------------------------------------------------------------------------------------------

    def find_row_and_click(self, element_name, xpath_pattern=None, checkbox=False, timeout=None):
        """Jadvaldagi qatorni topish va ustiga bosish."""

        timeout = timeout or self.default_timeout
        xpath_pattern = xpath_pattern or ("//div[contains(@class, 'tbl')]//div[contains(@class, 'tbl-row')]"
                                          "//div[contains(@class, 'tbl-cell') and normalize-space(text())='{}']")

        row_locator = (By.XPATH, xpath_pattern.format(element_name))

        try:
            # Sahifa yuklanishini kutish
            if not self._wait_for_page_load(timeout=timeout):
                self.logger.warning("Sahifa to'liq yuklanmadi!")

            # Jadval qatorini izlash
            elements = self._wait_for_presence_all(row_locator, timeout=timeout)
            if not elements:
                self.logger.warning(f"'{element_name}' qatori topilmadi.")
                return False

            target_element = elements[0]

            # Scroll qilish
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", target_element)
            time.sleep(0.5)

            # Elementni ko'rinishi
            if not self._wait_for_visibility(row_locator, timeout=timeout):
                self.logger.warning("Element ko'rinmadi.")
                return False

            if not self.click(row_locator):
                self.logger.warning("Elementni bosib bo'lmadi.")
                return False

            # Checkboxni bosish
            if checkbox:
                checkbox_locator = (By.XPATH, f"//div[contains(@class, 'tbl-row') and .//div[text()='{element_name}']]//span")
                element = self._wait_for_presence(checkbox_locator)
                if not element:
                    self.logger.error(f"Checkbox topilmadi: {checkbox_locator}")
                    return False
                if not self._click_js(element):
                    self.logger.error(f"Checkbox bosib bo'lmadi: {checkbox_locator}")
                    return False
            return True

        except Exception as e:
            self.logger.error(f"find_row_and_click xatolik: {str(e)}")
            self.take_screenshot(f"find_row_and_click_{element_name}_error")
            return False

    # ------------------------------------------------------------------------------------------------------------------

    def _wait_for_async_operations(self, timeout=None):
        """Sahifadagi async operatsiyalar (AJAX, fetch) tugashini kutish."""

        timeout = timeout or self.default_timeout
        wait = WebDriverWait(self.driver, timeout)
        try:
            wait.until(lambda driver:
                       driver.execute_script(
                           "return document.readyState") == "complete" and
                       driver.execute_script(
                           "return typeof jQuery !== 'undefined' ? jQuery.active === 0 : true;") and
                       driver.execute_script("""
                        return window.performance
                            .getEntriesByType('resource')
                            .filter(r => !r.responseEnd &&
                                (r.initiatorType === 'fetch' ||
                                 r.initiatorType === 'xmlhttprequest')
                            ).length === 0;
                    """))
            # self.logger.info("Async operatsiyalar muvaffaqiyatli tugadi")
            return True
        except TimeoutException:
            self.logger.warning(f"Async operatsiyalar kutish vaqti tugadi: {timeout}s")
            return False

    # def _wait_for_async_operations(self, timeout=None):
    #     """Sahifadagi asinxron operatsiyalarni kutish."""
    #     timeout = timeout or self.default_timeout
    #     try:
    #         WebDriverWait(self.driver, timeout).until(lambda driver: driver.execute_script("""
    #             return (
    #                 document.readyState === 'complete' &&
    #                 (typeof jQuery === 'undefined' || jQuery.active === 0) &&
    #                 (typeof axios === 'undefined' || axios.defaults.transitional._pendingRequests === 0) &&
    #                 !document.querySelector('.loading-overlay, .spinner, .loader')
    #             );
    #         """))
    #         return True
    #     except TimeoutException:
    #         self.logger.warning("Asinxron operatsiyalar kutish vaqti tugadi")
    #         return False


    def _check_main_content_loaded(self, timeout=None):
        """Sahifada asosiy kontent yuklanganligini tekshirish."""

        timeout = timeout or self.default_timeout
        main_selectors = ["//html", "//body"]
        start_time = time.time()
        for selector in main_selectors:
            try:
                elements = self._wait_for_presence_all((By.CSS_SELECTOR, selector), timeout)
                if any(e.is_displayed() and len(e.text.strip()) > 0 for e in elements):
                    elapsed_time = time.time() - start_time
                    self.logger.info(f"Asosiy kontent {elapsed_time:.1f} sekund ichida yuklandi")
                    return True
            except Exception:
                continue
        self.logger.warning(f"Asosiy kontent {timeout:.1f} sekund ichida topilmadi")
        return False

    # ------------------------------------------------------------------------------------------------------------------
