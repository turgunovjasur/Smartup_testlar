import re
import time
import inspect

from colorama import init

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from utils.error_handler import handle_selenium_error, handle_with_retry, WebDriverError
from utils.logger import LoggerConfig, log_action

init(autoreset=True)


def _get_test_name():
    """Test nomini avtomatik aniqlash"""
    stack = inspect.stack()
    for frame in stack:
        if frame.function.startswith("test_"):
            return frame.function
    return "unknown_test"


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = LoggerConfig().get_logger()
        self.default_timeout = 5
        self.actions = ActionChains(driver)

    def take_screenshot(self, filename=None):
        """Screenshot olish va saqlash"""
        return LoggerConfig().take_screenshot(self.driver, filename)

    # ------------------------------------------------------------------------------------------------------------------
    # Helper functions yordamchi metodlar
    @handle_selenium_error(take_screenshot=False)
    def _wait_for_page_load(self, timeout=None):
        """Sahifa to'liq yuklanganligini kutish"""
        return WebDriverWait(self.driver, timeout or self.default_timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete")

    @handle_selenium_error(take_screenshot=False)
    def _wait_for_async_operations(self, timeout=None):
        """Sahifadagi async operatsiyalar tugashini kutish"""
        return WebDriverWait(self.driver, timeout or self.default_timeout).until(
            lambda driver: driver.execute_script("""
                return (document.readyState === 'complete') &&
                    (typeof jQuery === 'undefined' || jQuery.active === 0) &&
                    (window.performance.getEntriesByType('resource')
                        .filter(r => !r.responseEnd && 
                            (r.initiatorType === 'fetch' || 
                             r.initiatorType === 'xmlhttprequest')
                        ).length === 0);
            """))

    @handle_selenium_error(take_screenshot=False)
    def _wait_for_overlay_absence(self, timeout=None):
        """Bloklovchi element yo'q bo'lishini kutish"""
        return WebDriverWait(self.driver, timeout or self.default_timeout).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "block-ui-overlay")))

    @handle_selenium_error(take_screenshot=False)
    def _check_spinner_absence(self, timeout=None):
        """Yuklash indikatorlarini tekshirish"""
        locator = (
            By.XPATH, "//div[contains(@class, 'block-ui-overlay') or contains(@class, 'block-ui-message-container')]")
        return WebDriverWait(self.driver, timeout or self.default_timeout).until(
            EC.invisibility_of_element_located(locator))

    @handle_selenium_error(take_screenshot=False)
    def _wait_for_all_loaders(self, timeout=None):
        """Barcha yuklanish indikatorlarini kutish"""
        self._wait_for_page_load(timeout)
        self._wait_for_async_operations(timeout)
        self._wait_for_overlay_absence(timeout)
        self._check_spinner_absence(timeout)
        return True

    # ------------------------------------------------------------------------------------------------------------------
    # Element bilan ishlash metodlari
    @handle_selenium_error(take_screenshot=False)
    def _wait_for_presence(self, locator, timeout=None):
        """Element DOMda mavjudligini kutish"""
        return WebDriverWait(self.driver, timeout or self.default_timeout).until(
            EC.presence_of_element_located(locator))

    @handle_selenium_error(take_screenshot=False)
    def _wait_for_clickable(self, locator, timeout=None):
        """Element bosilishi mumkinligini kutish"""
        return WebDriverWait(self.driver, timeout or self.default_timeout).until(
            EC.element_to_be_clickable(locator))

    @handle_selenium_error(take_screenshot=False)
    def _scroll_to_element(self, element, locator):
        """Elementga scroll qilish"""
        if element.is_displayed():
            return element

        location = element.location_once_scrolled_into_view
        self.driver.execute_script(
            f"window.scrollTo({location['x']}, {location['y'] - 100});")
        return element

    @handle_selenium_error(take_screenshot=False)
    def _perform_click(self, element, locator=None, is_js=False):
        """Click amalga oshirish"""
        page_name = self.__class__.__name__
        if is_js:
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info(f"⏺ {page_name}: JS-Click: {locator}")
        else:
            element.click()
            self.logger.info(f"⏺ {page_name}: Click: {locator}")
        return True

    # ------------------------------------------------------------------------------------------------------------------
    # Asosiy public metodlar
    @handle_with_retry(max_attempts=3, delay=1)
    @handle_selenium_error()
    def click(self, locator):
        """Elementni bosish asosiy funksiyasi"""
        self._wait_for_all_loaders()
        element_dom = self._wait_for_presence(locator)
        self._scroll_to_element(element_dom, locator)
        element_clickable = self._wait_for_clickable(locator)

        try:
            if self._perform_click(element_clickable, locator):
                return True
        except Exception:
            return self._perform_click(element_dom, locator, is_js=True)

    # ------------------------------------------------------------------------------------------------------------------

    @log_action()
    @handle_with_retry()
    def wait_for_element_visible(self, locator, timeout=None):
        """Elementni ko'rinishini kutish"""
        page_name = self.__class__.__name__
        self._wait_for_all_loaders()
        element = self._wait_for_presence(locator)
        self._scroll_to_element(element, locator)
        element = WebDriverWait(self.driver, timeout or self.default_timeout).until(
            EC.visibility_of_element_located(locator))
        if element:
            self.logger.info(f"⏺ {page_name}: Visible: {locator}")
        return element

    # ------------------------------------------------------------------------------------------------------------------

    @handle_with_retry()
    def input_text(self, locator, text):
        """Matn kiritish"""
        element = self._wait_for_clickable(locator)
        element.clear()
        element.send_keys(text)
        return True

    @handle_selenium_error()
    def _wait_for_presence_all(self, locator, timeout=None):
        """Elementlar ro'yxatini kutish"""
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator))

    @handle_selenium_error()
    def _wait_for_visibility(self, locator, timeout=None):
        """Element ko'rinishini kutish"""
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator))

    @handle_selenium_error()
    def _wait_for_invisibility_of_element(self, element, timeout=None):
        """Element ko'rinmasligini kutish"""
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element(element))

    @handle_selenium_error()
    def _wait_for_invisibility_of_locator(self, locator, timeout=None):
        """Locator ko'rinmasligini kutish"""
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator))

    @handle_selenium_error()
    def get_text(self, locator):
        """Element textini olish"""
        element = self.wait_for_element_visible(locator)
        return element.text

    @handle_selenium_error()
    def clear_element(self, locator):
        """Elementni tozalash"""
        element = self._wait_for_clickable(locator)
        element.clear()
        return True

    @handle_selenium_error()
    def get_numeric_value(self, locator):
        """Element ichidan raqamli qiymatni olish"""
        text = self.get_text(locator)
        if text is None:
            return None
        numeric_value = re.sub(r'[^0-9.]', '', text.strip())
        return float(numeric_value) if numeric_value and numeric_value.count('.') <= 1 else None

    @handle_selenium_error(take_screenshot=False)
    def get_current_url(self):
        """Joriy URL ni olish"""
        return self.driver.current_url

    @handle_selenium_error(take_screenshot=False)
    def cut_url(self):
        """URL ni formatlash"""
        current_url = self.get_current_url()
        try:
            base_path = current_url.split('#')[0]
            after_hash = current_url.split('#')[1]
            user_id = after_hash.split('/!')[1].split('/')[0]
            return f"{base_path}#/!{user_id}/"
        except Exception as e:
            self.logger.warning(f"URL ni kesishda xatolik: {str(e)}")
            return current_url

    @handle_with_retry()
    def click_options(self, input_locator, options_locator, element, scroll=10):
        """Dropdown bilan ishlash"""
        # Dropdown ochish
        self.click(input_locator)

        # Optionlarni kutish
        options = self._wait_for_presence_all(options_locator)
        if not options:
            raise WebDriverError("Dropdown variantlari yuklanmadi")

        def find_and_click_option():
            element_str = str(element).strip()
            for option in options:
                if option.text.strip() == element_str:
                    self._perform_click(option)
                    return True
            return False

        if find_and_click_option():
            # Dropdown yopilganini tekshirish
            if self._check_dropdown(options_locator):
                return True
            return False

        # Scroll bilan qidirish
        dropdown_container = self._find_visible_container(options_locator)
        if not dropdown_container:
            raise WebDriverError("Dropdown konteyner topilmadi")

        last_height = 0
        for _ in range(scroll):
            self.driver.execute_script("arguments[0].scrollBy(0, 300);", dropdown_container)
            time.sleep(1)

            options = self._wait_for_presence_all(options_locator)
            if options and find_and_click_option():
                return True

            new_height = self.driver.execute_script("return arguments[0].scrollHeight", dropdown_container)
            if new_height == last_height:
                raise WebDriverError(f"Element '{element}' topilmadi")
            last_height = new_height

        return self._check_dropdown(options_locator)

    @handle_selenium_error(take_screenshot=False)
    def _check_dropdown(self, options_locator):
        """Dropdown ESC bilan yopish va yopilganini tekshirish"""
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
        time.sleep(0.1)
        return self._wait_for_invisibility_of_locator(options_locator)

    @handle_selenium_error()
    def _find_visible_container(self, options_locator):
        """Dropdown konteynerni topish"""
        container_selectors = [
            "//div[contains(@class, 'hint-body')]",
            "//div[contains(@class, 'dropdown-menu')]",
            "//div[contains(@class, 'select-dropdown')]",
            f"{options_locator[1]}/ancestor::div[contains(@class, 'hint')]",
            f"{options_locator[1]}/ancestor::div[contains(@class, 'dropdown')]",
        ]

        for selector in container_selectors:
            containers = self.driver.find_elements(By.XPATH, selector)
            for container in containers:
                if container.is_displayed():
                    return container
        return None

    @handle_with_retry(max_attempts=3)
    def find_row_and_click(self, element_name, xpath_pattern=None, timeout=None,
                           expand=False, checkbox=False, limit=3):
        """Jadval qatorini topish va bosish"""
        xpath_pattern = xpath_pattern or (
            "//div[contains(@class, 'tbl')]//div[contains(@class, 'tbl-row')]"
            "//div[contains(@class, 'tbl-cell') and normalize-space(text())='{}']"
        )
        row_locator = (By.XPATH, xpath_pattern.format(element_name))

        if expand:
            self._expand_table_limit(limit)

        # Qatorni topish
        elements = self._wait_for_presence_all(row_locator, timeout)
        if not elements and limit:
            self._expand_table_limit(limit)
            elements = self._wait_for_presence_all(row_locator, timeout)
            if not elements:
                raise WebDriverError(f"'{element_name}' qatori topilmadi")

        target_element = elements[0]
        self._scroll_to_element(target_element, row_locator)

        # Click
        self.click(row_locator)

        # Checkbox bilan ishlash
        if checkbox:
            checkbox_locator = (
                By.XPATH,
                f"//div[contains(@class, 'tbl-row') and .//div[text()='{element_name}']]//span"
            )
            checkbox_element = self._wait_for_presence(checkbox_locator)
            return self._perform_click(checkbox_element, checkbox_locator, is_js=True)

        return True

    @handle_selenium_error()
    def _expand_table_limit(self, limit):
        """Jadval limitini kengaytirish"""
        limit_button = (By.XPATH, '//button[@class="btn btn-default rounded-0 ng-binding"]')
        self.click(limit_button)
        item_button = (
            By.XPATH,
            f'//button[@class="btn btn-default rounded-0 ng-binding"]/following-sibling::div/a[{limit}]'
        )
        self.click(item_button)
        time.sleep(1)  # UI yangilanishini kutish

    @handle_selenium_error()
    def _check_main_content_loaded(self, timeout=None):
        """Asosiy kontentni tekshirish"""
        timeout = timeout or self.default_timeout
        for selector in ["//html", "//body"]:
            elements = self._wait_for_presence_all((By.XPATH, selector), timeout)
            if any(e.is_displayed() and len(e.text.strip()) > 0 for e in elements):
                return True
        return False
