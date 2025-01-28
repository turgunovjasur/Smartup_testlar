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
        self.logger.setLevel(logging.DEBUG)

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
            InvalidElementStateException: "⚠️ Element holati o‘zgartirilmasligi mumkin.",
            NoSuchWindowException: "❌ Ko‘rsatilgan oyna mavjud emas.",
            NoSuchFrameException: "❌ Ko‘rsatilgan frame mavjud emas.",
            ElementNotSelectableException: "⚠️ Element tanlanishi mumkin emas.",
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

    # Halper function --------------------------------------------------------------------------------------------------

    def _wait_for_page_load(self, timeout=None):
        """Sahifa to'liq yuklanganligini kutish."""

        timeout = timeout or self.default_timeout
        try:
            result = WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete")
            return bool(result)

        except TimeoutException:
            self.logger.error(f"Sahifa {timeout}s ichida yuklanmadi.")
            return False

    def _wait_for_async_operations(self, timeout=None):
        """Sahifadagi async operatsiyalar (AJAX, fetch) tugashini kutish."""

        timeout = timeout or self.default_timeout
        try:
            result = WebDriverWait(self.driver, timeout).until(lambda driver:
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
            return bool(result)

        except TimeoutException:
            self.logger.error(f"Async operatsiyalar {timeout}s o'tgandan keyin ham tugamadi.")
            return False

    def _wait_for_overlay_absence(self, timeout=None):
        """Bloklovchi element yo‘q bo‘lishini kutadi."""

        timeout = timeout or self.default_timeout
        try:
            result = WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "block-ui-overlay")))
            return bool(result)

        except TimeoutException:
            self.logger.error(f"Bloklovchi element {timeout}s ichida yo'qolmadi.")
            return False

    def _check_spinner_absence(self, timeout=None):
        """Yuklash indikatorlarining mavjud emasligini tekshirish."""

        timeout = timeout or self.default_timeout
        locator = (By.XPATH,
                   "//div[contains(@class, 'block-ui-overlay') or contains(@class, 'block-ui-message-container')]")
        try:
            result = WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator))
            return bool(result)

        except TimeoutException:
            self.logger.error(f"Yuklash indikatori {timeout}s o'tgandan keyin ham mavjud.")
            return False

    def _wait_for_all_loaders(self, timeout=None):
        """Sahifaning to'liq yuklanganligi va foydalanishga tayyor holatini kutish."""

        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        try:
            # Sahifaning asosiy HTML dokumenti yuklanishini kutish
            if not self._wait_for_page_load(timeout):
                return False

            # Barcha asinxron so'rovlar tugashini kutish
            if not self._wait_for_async_operations(timeout):
                return False

            # Bloklovchi elementlar yo'qolishini kutish
            if not self._wait_for_overlay_absence(timeout):
                return False

            # Yuklash indikatorlari yo'qolishini kutish
            if not self._check_spinner_absence(timeout):
                return False
            return True

        except TimeoutException:
            self.logger.error(f"{page_name}: Sahifa testlash uchun to'liq yuklanmadi", exc_info=True)
            return False

    # ------------------------------------------------------------------------------------------------------------------

    def _click(self, element, locator=None, retry=False, error_massage=True):
        """Oddiy click urinishi"""

        page_name = self.__class__.__name__
        try:
            element.click()
            self.logger.info(f"⏺{page_name}: {'Retry ' if retry else ''}Click: {locator}")
            return True
        except WebDriverException:
            if error_massage:
                self.logger.warning(f"❗{page_name}: {'Retry ' if retry else ''}Click ishlamadi: {locator}")
            return False

    def _click_js(self, element, locator=None, retry=False):
        """JavaScript orqali majburiy bosish."""

        try:
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info(f"⏺{'Retry ' if retry else ''}JS-Click: {locator}")
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

    def _wait_for_presence(self, locator, timeout=None, error_message=True):
        """Element DOM da mavjud ekanligini tekshirish."""

        timeout = timeout or self.default_timeout
        page_name = self.__class__.__name__

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator))
            return element

        except TimeoutException:
            if error_message:
                self.logger.error(f"{page_name}: Element DOM da topilmadi / {timeout}s: {locator}")
            return False

    def _scroll_to_element(self, element, locator):
        """Elementga scroll qilish."""

        page_name = self.__class__.__name__

        if element.is_displayed():
            return element

        try:
            location = element.location_once_scrolled_into_view
            self.driver.execute_script(
                f"window.scrollTo({location['x']}, {location['y'] - 100});")

            if element.is_displayed():
                return element

        except Exception:
            self.logger.error(f"{page_name}: Scroll qilishda xatolik. {locator}")
            return False
        return False

    def _wait_for_visibility(self, locator, timeout=None, error_message=True):
        """Element sahifada ko'rinishini tekshirish."""

        timeout = timeout or self.default_timeout
        page_name = self.__class__.__name__
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator))
            return element

        except TimeoutException:
            if error_message:
                self.logger.error(
                    f"{page_name}: Element sahifada ko'rinmadi / {timeout}s: {locator}")
            return None

    def _wait_for_clickable(self, locator, timeout=None, error_message=True):
        """Element bosish uchun tayyor ekanligini tekshirish."""

        timeout = timeout or self.default_timeout
        page_name = self.__class__.__name__

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator))
            return element

        except TimeoutException:
            if error_message:
                self.logger.error(
                    f"{page_name}: Element bosish uchun tayyor emas / {timeout}s: {locator}")
            return None

    # ------------------------------------------------------------------------------------------------------------------

    def _wait_for_presence_all(self, locator, timeout=None, error_massage=True):
        """Elementlar ro'yxatini kutish."""

        timeout = timeout or self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            if error_massage:
                self.logger.error(f"Elementlar ro'yhati topilmadi: {locator}")
            return []

    def _wait_for_invisibility_of_element(self, element, timeout=None, error_massage=None):
        """Element ni ko'rinmas bo'lishini kutish."""

        timeout = timeout or self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element(element))
        except TimeoutException as e:
            if error_massage:
                self.logger.error(f"Element interfeys dan yo'qolmadi: {e}")
            return False

    def _wait_for_invisibility_of_locator(self, locator, timeout=None, error_massage=None):
        """Locator ni ko'rinmas bo'lishini kutish."""

        timeout = timeout or self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
        except TimeoutException as e:
            if error_massage:
                self.logger.error(f"Locator interfeys dan yo'qolmadi: {e}")
            return False

    # Click ------------------------------------------------------------------------------------------------------------
    def click(self, locator, retries=3, retry_delay=1):
        """Elementni bosish funksiyasi"""

        page_name = self.__class__.__name__
        attempt = 0
        while attempt < retries:
            try:
                # Sahifa yuklanishini tekshirish
                if not self._wait_for_all_loaders():
                    return False

                # Element DOM da mavjudligini tekshirish va elementni olish
                element_dom = self._wait_for_presence(locator)
                if not element_dom:
                    return False

                # Elementga scroll qilish
                element_scroll = self._scroll_to_element(element_dom, locator)
                if not element_scroll:
                    return False

                element_clickable = self._wait_for_clickable(locator)
                if not element_clickable:
                    return False

                # 1-urinish: Oddiy click
                if self._click(element_clickable, locator, error_massage=False):
                    return True

                # 2-urinish: Qayta oddiy click
                time.sleep(retry_delay)
                if self._click(element_clickable, locator, retry=True, error_massage=False):
                    return True

                # 3-urinish: JavaScript click
                time.sleep(retry_delay)
                element_dom = self._wait_for_presence(locator)
                if self._click_js(element_dom, locator):
                    return True

            except StaleElementReferenceException:
                self.logger.warning(f"{page_name} Element yangilandi. Click {attempt + 1}/{retries}. {locator}")
            except TimeoutException:
                self.logger.error(f"{page_name} Elementni kutish vaqti tugadi. {locator}")
            except Exception as e:
                self.logger.warning(f"{page_name} Kutilmagan xatolik: {e}. Click {attempt + 1}/{retries}")

            attempt += 1
            time.sleep(retry_delay)

        self.logger.error(f'❌{page_name} Click muvaffaqiyatsiz yakunlandi')
        self.take_screenshot(f"{page_name.lower()}_click_error")
        return False

    # Wait -------------------------------------------------------------------------------------------------------------

    def wait_for_element_visiblee(self, locator, timeout=None, retries=3, retry_delay=1):
        """Elementni ko'rinishini kutish funksiyasi"""
        page_name = self.__class__.__name__
        self.logger.debug(f"{page_name} sahifasida element qidirilmoqda: {locator}")

        timeout = timeout or self.default_timeout
        attempt = 0

        while attempt < retries:
            try:
                # Sahifa yuklanishini tekshirish
                if not self._wait_for_all_loaders():
                    return False

                # Element DOM da mavjudligini tekshirish va elementni olish
                element_dom = self._wait_for_presence(locator)
                if not element_dom:
                    return False

                element_visibility = self._wait_for_visibility(locator)
                if not element_visibility:
                    # Elementga scroll qilish
                    element_scroll = self._scroll_to_element(element_dom, locator)
                    if not element_scroll:
                        return False

                if element_visibility:
                    self.logger.info(f"⏺ {page_name} element topildi: {locator}")
                    return element_visibility

            except StaleElementReferenceException:
                self.logger.warning(f"{page_name} element yangilandi: (Urinish {attempt + 1})")

            except TimeoutException:
                self.logger.error(f"{page_name} Elementni kutish vaqti tugadi: (Urinish {attempt + 1}")

            except Exception as e:
                self.logger.warning(f"{page_name} Kutilmagan xato: {str(e)} (Urinish {attempt + 1})")

            attempt += 1
            if attempt < retries:
                self.logger.warning(f"{page_name} Element topilmadi. {retry_delay} soniyadan keyin qayta urinish...")
                time.sleep(retry_delay)

        # Barcha urinishlar tugadi
        self.logger.error(f"❌ {page_name} Elementni topish muvaffaqiyatsiz yakunlandi")
        self.take_screenshot(f"{page_name.lower()}_element_not_found")
        return False

    def wait_for_element_visible(self, locator, timeout=None, retries=3, retry_delay=1):
        """Elementni ko'rinishini kutish funksiyasi"""
        page_name = self.__class__.__name__
        self.logger.debug(f"{page_name} sahifasida element qidirilmoqda: {locator}")

        timeout = timeout or self.default_timeout
        attempt = 0

        while attempt < retries:
            try:
                # Sahifa yuklanishini tekshirish
                if not self._wait_for_all_loaders():
                    attempt += 1
                    if attempt < retries:
                        self.logger.warning(
                            f"{page_name} Sahifa yuklanmadi. {retry_delay} soniyadan keyin qayta urinish...")
                        time.sleep(retry_delay)
                        continue
                    return False

                # Element DOM da mavjudligini tekshirish va elementni olish
                element_dom = self._wait_for_presence(locator)
                if not element_dom:
                    attempt += 1
                    if attempt < retries:
                        self.logger.warning(
                            f"{page_name} Element DOM da topilmadi. {retry_delay} soniyadan keyin qayta urinish...")
                        time.sleep(retry_delay)
                        continue
                    return False

                element_visibility = self._wait_for_visibility(locator)
                if not element_visibility:
                    # Elementga scroll qilish
                    element_scroll = self._scroll_to_element(element_dom, locator)
                    if not element_scroll:
                        attempt += 1
                        if attempt < retries:
                            self.logger.warning(
                                f"{page_name} Elementga scroll qilib bo'lmadi. {retry_delay} soniyadan keyin qayta urinish...")
                            time.sleep(retry_delay)
                            continue
                        return False

                if element_visibility:
                    self.logger.info(f"⏺ {page_name} element topildi: {locator}")
                    return element_visibility

            except StaleElementReferenceException:
                self.logger.warning(f"{page_name} element yangilandi: (Urinish {attempt + 1})")
                attempt += 1
                if attempt < retries:
                    time.sleep(retry_delay)
                    continue

            except TimeoutException:
                self.logger.error(f"{page_name} Elementni kutish vaqti tugadi: (Urinish {attempt + 1})")
                attempt += 1
                if attempt < retries:
                    time.sleep(retry_delay)
                    continue

            except Exception as e:
                self.logger.warning(f"{page_name} Kutilmagan xato: {str(e)} (Urinish {attempt + 1})")
                attempt += 1
                if attempt < retries:
                    time.sleep(retry_delay)
                    continue

        # Barcha urinishlar tugadi
        self.logger.error(f"❌ {page_name} Elementni topish muvaffaqiyatsiz yakunlandi")
        self.take_screenshot(f"{page_name.lower()}_element_not_found")
        return False

    # ------------------------------------------------------------------------------------------------------------------

    def input_text(self, locator, text):
        try:
            if element := self._wait_for_clickable(locator):
                element.clear()
                element.send_keys(text)
                return True

        except Exception:
            self.logger.warning("input_text: not working!: %s", locator)
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

    def get_text(self, locator):
        element = self.wait_for_element_visible(locator)
        return element.text

    # ------------------------------------------------------------------------------------------------------------------

    def clear_element(self, locator):
        element = self._wait_for_clickable(locator)
        try:
            element.clear()
        except Exception:
            self.logger.error("clear_element: not clear.")

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
    def click_options(self, input_locator, options_locator, element, scroll=10):
        """
        Dropdown bilan ishlash uchun funksiya: elementni topib, uni bosish va dropdownni yopish.
        options_locator = (By.XPATH, '//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')
        """

        try:
            # 1. Dropdown ochish
            if not self.click(input_locator):
                self.logger.error("Dropdownni ochib bo'lmadi!")
                return False

            # 2. Optionlarni yuklanishini kutish
            options = self._wait_for_presence_all(options_locator, error_massage=False)
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
                self.logger.info(f"Element '{element}' topilmadi. Scroll boshlanmoqda.")
                dropdown_container = self._find_visible_container(options_locator)
                if not dropdown_container:
                    self.logger.error("Dropdown konteyner topilmadi.")
                    return False

                last_height = 0
                for _ in range(scroll):  # Maksimal 10 marta scroll qilishga ruxsat
                    self.driver.execute_script("arguments[0].scrollBy(0, 300);", dropdown_container)
                    time.sleep(1)

                    options = self._wait_for_presence_all(options_locator)
                    if options and find_and_click_option():
                        self.logger.info(f"Element '{element}' scroll orqali topildi va bosildi.")
                        break
                    new_height = self.driver.execute_script("return arguments[0].scrollHeight", dropdown_container)
                    if new_height == last_height:
                        self.logger.warning(f"Scroll tugadi, lekin {element} topilmadi.")
                        return False
                    last_height = new_height

            # 4. Dropdown yopilishini tekshirish
            if not self._check_dropdown(options_locator):
                return False
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

    def _check_dropdown(self, options_locator):
        """Dropdown yopilishini tekshirish."""

        try:
            # Turli yopish usullarini sinash
            self.driver.execute_script("document.body.click();")
            time.sleep(0.1)
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            time.sleep(0.1)

            return self._wait_for_invisibility_of_locator(options_locator)
        except Exception as e:
            self.logger.error(f"Dropdownni yopishda xatolik: {str(e)}")
            return False

    # ------------------------------------------------------------------------------------------------------------------

    def find_row_and_click(self, element_name, xpath_pattern=None, timeout=None,
                           expand=False, checkbox=False, limit=3):
        """Jadvaldagi qatorni topish va ustiga bosish."""

        xpath_pattern = xpath_pattern or ("//div[contains(@class, 'tbl')]//div[contains(@class, 'tbl-row')]"
                                          "//div[contains(@class, 'tbl-cell') and normalize-space(text())='{}']")
        row_locator = (By.XPATH, xpath_pattern.format(element_name))
        limit_button = (By.XPATH, '//button[@class="btn btn-default rounded-0 ng-binding"]')

        timeout = timeout or self.default_timeout

        def click_limit_button(limit):
            self.click(limit_button)
            item_button = (
                By.XPATH, f'//button[@class="btn btn-default rounded-0 ng-binding"]/following-sibling::div/a[{limit}]')
            self.click(item_button)

        if expand:
            click_limit_button(limit=2)

        def process_element():
            try:
                # Sahifa yuklanishini kutish
                if not self._wait_for_page_load():
                    return False

                # Jadval qatorini izlash
                elements = self._wait_for_presence_all(row_locator, timeout, error_massage=False)
                if not elements:
                    if limit:
                        self.logger.info(f"'{element_name}' topilmadi. Limit 500 qilib belgilanadi")
                        click_limit_button(limit)
                        time.sleep(1)
                        # Qayta qidirish
                        elements = self._wait_for_presence_all(row_locator, error_massage=False)
                        if not elements:
                            self.logger.error(f"'{element_name}' limit o'zgartirilgandan keyin ham topilmadi.")
                            return False
                    else:
                        self.logger.error(f"'{element_name}' qatori topilmadi.")
                        return False

                target_element = elements[0]

                # Scroll qilish
                self._scroll_to_element(target_element, row_locator)

                # Elementni ko'rinishi
                if not self._wait_for_visibility(row_locator):
                    return False

                if not self.click(row_locator):
                    return False

                # Checkboxni bosish
                if checkbox:
                    checkbox_locator = (
                        By.XPATH, f"//div[contains(@class, 'tbl-row') and .//div[text()='{element_name}']]//span")
                    element = self._wait_for_presence(checkbox_locator)
                    if not element:
                        self.logger.error(f"Checkbox DOM da topilmadi: {checkbox_locator}")
                        return False
                    if not self._click_js(element, checkbox_locator):
                        self.logger.error(f"Checkbox bosib bo'lmadi: {checkbox_locator}")
                        return False

                return True

            except Exception as e:
                self.logger.error(f"find_row_and_click xatolik: {str(e)}")
                self.take_screenshot(f"find_row_and_click_{element_name}_error")
                return False

        return process_element()

    # ------------------------------------------------------------------------------------------------------------------

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
