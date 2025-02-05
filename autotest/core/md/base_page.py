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
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException
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

    def _wait_for_page_load(self, timeout=None):
        """Sahifa to'liq yuklanganligini kutish."""
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout
        try:
            result = WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete")
            return result
        except TimeoutException:
            self.logger.error(f"{page_name}: Sahifa {timeout}s ichida yuklanmadi.")
            return False

    def _wait_for_async_operations(self, timeout=None):
        """Sahifadagi async operatsiyalar (AJAX, fetch) tugashini kutish."""
        page_name = self.__class__.__name__
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
            return True
        except TimeoutException:
            self.logger.error(f"{page_name}: Async operatsiyalar {timeout}s ichida tugamadi.")
            return False

    def _wait_for_overlay_absence(self, timeout=None):
        """Bloklovchi element yo‘q bo‘lishini kutadi."""
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "block-ui-overlay")))
            return True
        except TimeoutException:
            self.logger.error(f"{page_name}: Bloklovchi element {timeout}s ichida yo'qolmadi.")
            return False

    def _check_spinner_absence(self, timeout=None):
        """Yuklash indikatorlarining mavjud emasligini tekshirish."""
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout
        locator = (By.XPATH,
                   "//div[contains(@class, 'block-ui-overlay') or contains(@class, 'block-ui-message-container')]")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            self.logger.error(f"{page_name}: Yuklash indikatori {timeout}s ichida yo'qolmadi.")
            return False

    def _wait_for_all_loaders(self, timeout=None):
        """Sahifadagi barcha yuklanish indikatorlarini kutish"""
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        try:
            # Sahifaning asosiy yuklanishi
            if not self._wait_for_page_load(timeout):
                raise TimeoutException("Sahifa HTML yuklashni tugatmadi")

            # Asinxron so'rovlarni kutish
            if not self._wait_for_async_operations(timeout):
                raise TimeoutException("Sahifadagi asinxron so'rovlar tugamadi")

            # Overlaylarni yo'qolishini kutish
            if not self._wait_for_overlay_absence(timeout):
                raise TimeoutException("Sahifadagi overley yo'qolmadi")

            # Spinnerlarni yo'qolishini kutish
            if not self._check_spinner_absence(timeout):
                raise TimeoutException("Sahifadagi yuklanish indikatori yo'qolmadi")

            return True
        except Exception as e:
            self.logger.error(f"{page_name}: Sahifa yuklanishida xatolik. {e}")
            return False

    # ------------------------------------------------------------------------------------------------------------------

    def _click(self, element, locator=None, retry=False, error_massage=True):
        """Oddiy click urinishi"""
        page_name = self.__class__.__name__
        try:
            element.click()
            self.logger.info(f"⏺ {page_name}: {'Retry ' if retry else ''}Click: {locator}")
            return True
        except WebDriverException:
            if error_massage:
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
            self.logger.error(f"❗{'Retry ' if retry else ''}JS-Click ishlamadi: {locator}")
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

    def _wait_for_presence(self, locator, timeout=None, error_massage=True):
        """Locator DOMda mavjud ekanligini tekshirish"""
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return element
        except StaleElementReferenceException:
            if error_massage:
                self.logger.warning(f"{page_name}: Element DOM da yangilandi: {locator}")
            raise
        except TimeoutException:
            if error_massage:
                self.logger.error(f"{page_name}: Element DOM da topilmadi: {locator}")
            return None
        except Exception as e:
            if error_massage:
                self.logger.error(f"{page_name}: Element qidirishda kutilmagan xato: {e}")
            return None

    def _scroll_to_element(self, element, locator, retries=3):
        """Element ga scroll qilish."""
        page_name = self.__class__.__name__

        if element.is_displayed():
            return element

        try:
            location = element.location_once_scrolled_into_view
            self.driver.execute_script(f"window.scrollTo({location['x']}, {location['y'] - 100});")
            return element
        except Exception:
            self.logger.warning(f"{page_name}: Scroll qilishda xatolik yuz berdi. Retry amalga oshiriladi.")

        for attempt in range(retries):
            try:
                location = element.location_once_scrolled_into_view
                self.driver.execute_script(f"window.scrollTo({location['x']}, {location['y'] - 100});")
                return element
            except Exception:
                time.sleep(1)

        self.logger.error(f"{page_name}: Scroll qilishda xatolik. Element locator: {locator}")
        return None

    def _wait_for_visibility(self, locator, timeout=None, error_massage=True):
        """Locatorni ko'rinishini tekshirish"""
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return element
        except StaleElementReferenceException:
            if error_massage:
                self.logger.warning(f"{page_name}: Elementni ko'rinishida: element DOM da yangilandi: {locator}")
            raise
        except TimeoutException:
            if error_massage:
                self.logger.error(f"{page_name}: Element sahifada ko'rinmadi: {locator}")
            return None
        except Exception as e:
            if error_massage:
                self.logger.error(f"{page_name}: Element ko'rinishini tekshirishda xatolik: {e}")
            return None

    def _wait_for_clickable(self, locator, timeout=None, error_massage=True):
        """Locatorni ni bosish uchun tayyor ekanligini tekshirish."""
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            return element
        except StaleElementReferenceException:
            if error_massage:
                self.logger.warning(f"{page_name}: Elementni bosishda: element DOM da yangilandi: {locator}")
            raise
        except TimeoutException:
            if error_massage:
                self.logger.warning(f"{page_name}: Element bosishga tayyor emas: {locator}")
            return None
        except Exception as e:
            if error_massage:
                self.logger.error(f"{page_name}: Element bosilishini tekshirishda xatolik: {e}")
            return None

    # Click ------------------------------------------------------------------------------------------------------------

    def click(self, locator, timeout=None, retries=3, retry_delay=0.5):
        """Elementni bosish funksiyasi"""
        page_name = self.__class__.__name__
        self.logger.debug(f"{page_name}: Element bosilmoqda: {locator}")

        timeout = timeout or self.default_timeout
        attempt = 0

        while attempt < retries:
            try:
                # 1. Sahifa yuklanishini tekshirish
                if not self._wait_for_all_loaders():
                    raise TimeoutException(f"{page_name}: sahifasi yuklanishi muvaffaqiyatsiz yakunlandi")

                # 2. Element DOM da borligini tekshirish
                element_dom = self._wait_for_presence(locator, error_massage=True)
                if not element_dom:
                    return False

                # 3. Elementga scroll
                if not self._scroll_to_element(element_dom, locator):
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
                element_dom = self._wait_for_presence(locator, error_massage=True)
                if not element_dom:
                    return False
                if self._click_js(element_dom, locator):
                    return True

                return False

            except StaleElementReferenceException:
                self.logger.warning(f"🔄 {page_name}: Element yangilandi, qayta urinish (Urinish {attempt + 1})")
                time.sleep(retry_delay)
            except TimeoutException:
                self.logger.warning(f"⛔️ {page_name}: Vaqt tugadi: {timeout}s (Urinish {attempt + 1})")
            except Exception:
                self.logger.warning(f"⁉️ {page_name}: Kutilmagan xato: (Urinish {attempt + 1})")

            attempt += 1
            if attempt < retries:
                self.logger.warning(f"⚠️ {page_name}: Element bosilmadi. (Urinish {attempt})")
                time.sleep(retry_delay)

        # Barcha urinishlar tugadi
        self.logger.error(f"❌ {page_name}: Element bosilmadi. (Urinish {attempt}): {locator}")
        self.take_screenshot(f"{page_name.lower()}_element_not_click")

        return False

    # Wait -------------------------------------------------------------------------------------------------------------

    def wait_for_element_visible(self, locator, timeout=None, retries=3, retry_delay=1):
        """Elementni ko'rinishini kutish funksiyasi"""
        page_name = self.__class__.__name__
        self.logger.debug(f"{page_name}: Element qidirilmoqda: {locator}")

        timeout = timeout or self.default_timeout
        attempt = 0

        while attempt < retries:
            try:
                # 1. Sahifa yuklanishini tekshirish
                if not self._wait_for_all_loaders():
                    raise TimeoutException(f"{page_name}: sahifasi yuklanishi muvaffaqiyatsiz yakunlandi")

                # 2. Element DOM da borligini tekshirish
                element_dom = self._wait_for_presence(locator, error_massage=True)
                if not element_dom:
                    return False

                # 3. Elementga scroll
                if not self._scroll_to_element(element_dom, locator):
                    return False

                # 4. Element ko'rinishini tekshirish
                if element := self._wait_for_visibility(locator, error_massage=True):
                    self.logger.info(f"⏺ {page_name} element topildi: {locator}")
                    return element

                return False

            except StaleElementReferenceException:
                self.logger.warning(f"🚫 {page_name}: Element yangilandi (Urinish {attempt + 1})")
                time.sleep(retry_delay)
            except TimeoutException:
                self.logger.warning(f"⛔️ {page_name}: Vaqt tugadi: {timeout}s (Urinish {attempt + 1})")
            except Exception:
                self.logger.warning(f"⁉️ {page_name}: Kutilmagan xato: (Urinish {attempt + 1})")

            attempt += 1
            if attempt < retries:
                self.logger.warning(f"⚠️ {page_name}: Element topilmadi. (Urinish {attempt}): {locator}")
                time.sleep(retry_delay)

        # Barcha urinishlar tugadi
        self.logger.error(f"❌ {page_name}: Element topilmadi. (Urinish {attempt}): {locator}")
        self.take_screenshot(f"{page_name.lower()}_element_not_found")

        return False

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

    # ------------------------------------------------------------------------------------------------------------------

    def input_text(self, locator, text):
        import inspect

        page_name = self.__class__.__name__
        # Chaqiruvchi funksiya nomini olish
        caller_frame = inspect.currentframe().f_back
        caller_name = caller_frame.f_code.co_name if caller_frame else None

        # Sahifa to'liq yuklangunicha kutish
        if not self._wait_for_all_loaders():
            self.logger.error(f"{page_name}: input yuklanmadi: {locator}")
            self.take_screenshot(f"{page_name.lower()}_input_not_loaded")
            return False

        # Element bosilishi mumkin bo'lguncha kutish
        element = self._wait_for_clickable(locator)
        if element is None:
            self.logger.error(f"{page_name}: Input topilmadi yoki bosilmadi: {locator}")
            self.take_screenshot(f"{page_name.lower()}_input_not_clickable")
            return False

        try:
            element.clear()
            element.send_keys(text)
            if caller_name:
                self.logger.info(f"{page_name}: {caller_name} -> {text}")
            return True
        except Exception as e:
            self.logger.error(f"{page_name}: Matn kiritishda xatolik: {locator}. Xato: {str(e)}")
            self.take_screenshot(f"{page_name.lower()}_input_text_error")
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
            options = self._wait_for_presence_all(options_locator, error_massage=True)
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
                    # print(f'container: {container}')
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
            click_limit_button(limit=4)

        def click_checkbox():
            checkbox_locator = (By.XPATH, f"//div[contains(@class, 'tbl-row') and .//div[text()='{element_name}']]//span")
            element = self._wait_for_presence(checkbox_locator, error_massage=False)
            if not element:
                self.logger.error(f"Checkbox DOM da topilmadi: {checkbox_locator}")
                return False
            if not self._click_js(element, checkbox_locator):
                self.logger.error(f"Checkbox bosib bo'lmadi: {checkbox_locator}")
                return False
            return True

        def process_element():
            try:
                # Sahifa yuklanishini kutish
                if not self._wait_for_all_loaders():
                    return False

                # Jadval qatorini izlash
                elements = self._wait_for_presence_all(row_locator, timeout, error_massage=True)
                if not elements:
                    if limit:
                        self.logger.info(f"'{element_name}' topilmadi. Limit 500 qilib belgilanadi")
                        click_limit_button(limit)
                        time.sleep(1)
                        # Qayta qidirish
                        elements = self._wait_for_presence_all(row_locator, error_massage=True)
                        if not elements:
                            self.logger.error(f"'{element_name}' limit o'zgartirilgandan keyin ham topilmadi.")
                            return False
                    else:
                        self.logger.error(f"'{element_name}' qatori topilmadi.")
                        return False

                target_element = elements[0]

                # Scroll qilish
                if not self._scroll_to_element(target_element, row_locator):
                    return False

                # Elementni ko'rinishi
                if not self._wait_for_visibility(row_locator):
                    return False

                if not self.click(row_locator):
                    return False

                # Checkboxni bosish
                if checkbox:
                    click_checkbox()

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
