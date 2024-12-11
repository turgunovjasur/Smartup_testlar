import os
import time
import re
import logging
import allure
from time import time as current_time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, \
    ElementClickInterceptedException, ElementNotInteractableException, WebDriverException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.default_timeout = 20
        self.wait = WebDriverWait(driver, self.default_timeout)
        self.actions = ActionChains(driver)

    # ------------------------------------------------------------------------------------------------------------------

    def _get_wait(self, timeout=None):
        """
        Timeout ga qarab WebDriverWait obyektini qaytaradi
        """
        if timeout is not None and timeout != self.default_timeout:
            return WebDriverWait(self.driver, timeout)
        return self.wait

    # ------------------------------------------------------------------------------------------------------------------

    def click(self, locator, timeout=None, retries=3, retry_delay=1):
        wait = self._get_wait(timeout)
        attempt = 0
        last_exception = None

        while attempt < retries:
            try:
                wait.until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete")

                element = wait.until(
                    EC.presence_of_element_located(locator))

                element = wait.until(
                    EC.visibility_of_element_located(locator))

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});",
                    element)
                time.sleep(0.5)

                element = wait.until(
                    EC.element_to_be_clickable(locator))

                try:
                    element.click()
                except (ElementClickInterceptedException, ElementNotInteractableException):
                    try:
                        self.driver.execute_script("arguments[0].click();", element)
                    except WebDriverException:
                        try:
                            self.actions.move_to_element(element).click().perform()
                        except WebDriverException:
                            location = element.location
                            size = element.size
                            x = location['x'] + size['width'] // 2
                            y = location['y'] + size['height'] // 2
                            self.actions.move_by_offset(x, y).click().perform()

                return True

            except StaleElementReferenceException:
                attempt += 1
                if attempt == retries:
                    last_exception = "Element yangilandi va topilmadi"
                time.sleep(retry_delay)

            except TimeoutException:
                attempt += 1
                if attempt == retries:
                    last_exception = "Element kutish vaqti tugadi"
                time.sleep(retry_delay)

            except Exception as e:
                attempt += 1
                if attempt == retries:
                    last_exception = str(e)
                time.sleep(retry_delay)

        error_message = f"Click muvaffaqiyatsiz yakunlandi: {last_exception}"
        self.take_screenshot("click_error")
        raise AssertionError(error_message)

    # ------------------------------------------------------------------------------------------------------------------

    def wait_for_element_visible(self, locator, timeout=None, retries=3, retry_delay=1):
        """
            Elementni ko'rinishini kutish uchun kuchaytirilgan funksiya.
            Har bir xatolik turi uchun alohida qayta ishlash mexanizmi.
        """
        wait = self._get_wait(timeout)

        def try_with_retries(action, stage_name):
            attempt = 0
            while attempt < retries:
                try:
                    return action()

                except StaleElementReferenceException:
                    attempt += 1
                    if attempt == retries:
                        error_msg = f"{stage_name}: Element yangilandi va topilmadi"
                        logging.error(error_msg)
                        self.take_screenshot(f"stale_element_{stage_name}")
                        raise WebDriverException(error_msg)
                    logging.warning(f"{stage_name}: Element yangilandi. Qayta urinish {attempt}/{retries}")
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
                    if attempt == retries:
                        error_msg = f"{stage_name}: Kutilmagan xatolik: {str(e)}"
                        logging.error(error_msg)
                        self.take_screenshot(f"unexpected_{stage_name}")
                        raise WebDriverException(error_msg)
                    logging.warning(f"{stage_name}: Kutilmagan xatolik. Qayta urinish {attempt}/{retries}")
                    time.sleep(retry_delay)

        # 1. Sahifa to'liq yuklanganligi tekshirish
        try_with_retries(
            lambda: wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            ),
            "Sahifa yuklash"
        )

        # 2. Element mavjudligi tekshirish
        element = try_with_retries(
            lambda: wait.until(EC.presence_of_element_located(locator)),
            "Element mavjudligi"
        )

        # 3. Element ko'rinishi tekshirish
        element = try_with_retries(
            lambda: wait.until(EC.visibility_of_element_located(locator)),
            "Element ko'rinishi"
        )

        # 4. Elementni ko'rinadigan qismga scroll qilish
        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});",
                element
            )
            time.sleep(0.5)
        except Exception as e:
            logging.warning(f"Elementga scroll qilishda xatolik: {str(e)}")

        # 5. Element haqiqatdan ko'rinishi va faolligini tekshirish
        element = try_with_retries(
            lambda: wait.until(
                lambda x: (
                                  element.is_displayed() and
                                  element.is_enabled() and
                                  element.rect['height'] > 0 and
                                  element.rect['width'] > 0
                          ) and element
            ),
            "Element faolligi"
        )

        return element

    # ------------------------------------------------------------------------------------------------------------------

    def input_text(self, locator, text):
        try:
            element = self.wait_for_element_visible(locator)
            element = self.wait.until(EC.element_to_be_clickable(element))
            element.clear()
            element.send_keys(text)
            return True

        except Exception as e:
            print(f"input_text_error: {str(e)}")
            self.take_screenshot("input_text_error")
            return False

    # ------------------------------------------------------------------------------------------------------------------

    def input_text_elem(self, locator, elem_locator, timeout=None):
        try:
            if self.click(locator, timeout=timeout) and self.click(elem_locator, timeout=timeout):
                return True
            return False

        except Exception as e:
            print(f"input_text_elem: {str(e)}")
            self.take_screenshot("input_text_elem")
            return False

    # ------------------------------------------------------------------------------------------------------------------

    def get_element(self, locator):
        return self.wait_for_element_visible(locator)

    # ------------------------------------------------------------------------------------------------------------------

    def get_text(self, locator):
        element = self.wait_for_element_visible(locator)
        return element.text

    # ------------------------------------------------------------------------------------------------------------------

    def clear_element(self, locator):
        element = self.wait_for_element_visible(locator)
        element.clear()
        time.sleep(0.5)

    # ------------------------------------------------------------------------------------------------------------------

    def get_numeric_value(self, locator):
        text = self.get_text(locator)
        if text is None:
            print("Element topilmadi.")
            return None
        text = text.strip()
        numeric_value = re.sub(r'[^0-9.]', '', text)
        if numeric_value.count('.') <= 1:
            return float(numeric_value) if numeric_value else 0
        return None

    # ------------------------------------------------------------------------------------------------------------------

    def take_screenshot(self, filename):
        filename = str(filename)
        screenshot_dir = "screenshot_dir"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        screenshot_path = os.path.join(screenshot_dir, f"{filename}.png")
        self.driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved at {screenshot_path}")
        allure.attach.file(screenshot_path, name="Error Screenshot", attachment_type=allure.attachment_type.PNG)

    # ------------------------------------------------------------------------------------------------------------------

    def hover_and_hold(self, locator, duration=2000):
        element = self.get_element(locator)
        self.actions.move_to_element(element).perform()
        time.sleep(duration / 1000)

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

        except Exception as e:
            print(f"URL ni kesishda xatolik: {str(e)}")
            return current_url

    # ------------------------------------------------------------------------------------------------------------------
    def click_options(self, input_locator, options_locator, element, timeout=None, scroll_enabled=False):
        """
        Select/dropdown elementlar bilan ishlash uchun funksiya.

        Args:
            input_locator: Dropdown ni ochish uchun bosiladigan element lokatori
            options_locator: Dropdown ichidagi variantlar lokatori
            element: Tanlanishi kerak bo'lgan qiymat
            timeout: Kutish vaqti (default: None)
            scroll_enabled: Dropdown ro'yxatini pasga surish funksiyasi (default: False)

            options_locator = (By.XPATH, '//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

        """
        wait = self._get_wait(timeout)

        try:
            self.click(input_locator)
            time.sleep(0.5)

            if element:
                def find_and_click_option(options):
                    element_str = str(element).strip()
                    for option in options:
                        option_text = option.text.strip()

                        if option_text == element_str:
                            wait.until(EC.element_to_be_clickable(option)).click()
                            time.sleep(0.5)

                            action = ActionChains(self.driver)
                            action.move_by_offset(0, 0).click().perform()

                            try:
                                wait.until_not(EC.visibility_of_element_located(options_locator))
                            except TimeoutException:
                                print("dropdown yopilmadi!")
                                self.driver.execute_script("document.body.click()")

                            return True
                    return False

                # Birinchi urinish
                options = wait.until(EC.presence_of_all_elements_located(options_locator))
                if not options:
                    raise Exception("Ro'yxat bo'sh!")

                if find_and_click_option(options):
                    return True

                # Agar element topilmagan va scroll_enabled=True bo'lsa
                if scroll_enabled:
                    print(f"'{element}' topilmadi. Ro'yxatni pasga surish...")

                    try:
                        # Dropdown containerini topishning turli usullari
                        possible_container_selectors = [
                            "//div[contains(@class, 'hint-body')]",
                            "//div[contains(@class, 'dropdown-menu')]",
                            "//div[contains(@class, 'select-dropdown')]",
                            "//div[contains(@class, 'hint')]",
                            # element turgan hint containerini topish
                            f"{options_locator[1]}/ancestor::div[contains(@class, 'hint')]",
                            f"{options_locator[1]}/ancestor::div[contains(@class, 'dropdown')]",
                        ]

                        dropdown_container = None
                        for selector in possible_container_selectors:
                            try:
                                containers = self.driver.find_elements(By.XPATH, selector)
                                for container in containers:
                                    if container.is_displayed():
                                        dropdown_container = container
                                        break
                                if dropdown_container:
                                    break
                            except:
                                continue

                        if not dropdown_container:
                            print("Dropdown container topilmadi")
                            return False

                        # Ro'yxatni pasga surish
                        last_height = self.driver.execute_script("return arguments[0].scrollHeight", dropdown_container)
                        scroll_attempt = 0
                        max_scroll_attempts = 5  # Maksimal scroll urinishlar soni

                        while scroll_attempt < max_scroll_attempts:
                            # Scroll to bottom
                            self.driver.execute_script("arguments[0].scrollBy(0, 300)", dropdown_container)
                            time.sleep(1)

                            # Yangi elementlarni kutish
                            options = wait.until(EC.presence_of_all_elements_located(options_locator))

                            # Elementni izlash
                            if find_and_click_option(options):
                                return True

                            # Scroll height ni tekshirish
                            new_height = self.driver.execute_script("return arguments[0].scrollHeight",
                                                                    dropdown_container)
                            if new_height == last_height:
                                scroll_attempt += 1
                            else:
                                scroll_attempt = 0
                            last_height = new_height

                    except Exception as e:
                        print(f"Scroll qilishda xatolik: {str(e)}")

                print(f"'{element}' option topilmadi!")
                return False

        except TimeoutException:
            print("Ro'yxat yuklanmadi!")
            self.take_screenshot("options_timeout")
            return False

        except Exception as e:
            print(f"Option tanlashda xatolik: {str(e)}")
            self.take_screenshot("option_error")
            return False

    # ------------------------------------------------------------------------------------------------------------------

    # def click_options(self, input_locator, options_locator, element, timeout=None):
    #     """
    #     options_locator = (By.XPATH, '//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')
    #
    #     """
    #     wait = self._get_wait(timeout)
    #
    #     try:
    #         self.click(input_locator)
    #         time.sleep(0.5)
    #
    #         if element:
    #             options = wait.until(EC.presence_of_all_elements_located(options_locator))
    #
    #             if not options:
    #                 raise Exception("Ro'yxati bo'sh!")
    #
    #             element_str = str(element).strip()
    #             for option in options:
    #                 option_text = option.text.strip()
    #
    #                 if option_text == element_str:
    #                     wait.until(EC.element_to_be_clickable(option)).click()
    #
    #                     time.sleep(0.5)
    #
    #                     action = ActionChains(self.driver)
    #                     action.move_by_offset(0, 0).click().perform()
    #
    #                     try:
    #                         wait.until_not(EC.visibility_of_element_located(options_locator))
    #                     except TimeoutException:
    #                         print("dropdown yopilmadi!")
    #                         self.driver.execute_script("document.body.click()")
    #
    #                     return True
    #             print(f"'{element_str}' option topilmadi!")
    #             return False
    #
    #     except TimeoutException:
    #         print("Ro'yxat yuklanmadi!")
    #         self.take_screenshot("options_timeout")
    #         return False
    #
    #     except Exception as e:
    #         print(f"Option tanlashda xatolik: {str(e)}")
    #         self.take_screenshot("option_error")
    #         return False
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def find_row_and_click(self, element_name, xpath_pattern=None, checkbox=False, timeout=None):
        wait = self._get_wait(timeout)

        if not xpath_pattern:
            xpath_pattern = ("//div[contains(@class, 'tbl')]//div[contains(@class, 'tbl-row')]"
                             "//div[contains(@class, 'tbl-cell') and normalize-space(text())='{}']")

        find_elems_name_xpath = xpath_pattern.format(element_name)
        start_time = current_time()

        timeout = timeout if timeout is not None else self.default_timeout
        while current_time() - start_time < timeout:
            try:
                wait.until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete")

                elements = wait.until(
                    lambda driver: driver.find_elements(By.XPATH, find_elems_name_xpath))

                if elements:
                    target_element = elements[0]

                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});",
                        target_element)

                    time.sleep(0.5)

                    wait.until(EC.visibility_of(target_element))
                    target_element.click()

                    if checkbox:
                        try:
                            checkbox_elem = wait.until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, ".tbl-cell span")))
                            checkbox_elem.click()
                        except Exception as e:
                            print(f"Checkbox bosishda xatolik: {str(e)}")
                            return False

                    return True

                print(f"'{element_name}' elementi topilmadi, qayta urinish...")

            except StaleElementReferenceException:
                print("")

            except Exception as e:
                print(f"Xatolik yuz berdi: {str(e)}")

        print(f"'{element_name}' elementi {timeout} sekund ichida topilmadi")
        self.take_screenshot(f"find_row_{element_name}_error")
        return False

    # ------------------------------------------------------------------------------------------------------------------
    def wait_for_page_load(self, timeout=None):
        timeout = timeout if timeout else self.default_timeout
        wait = self._get_wait(timeout)
        start_time = current_time()

        try:
            # 1. Async operatsiyalarni kutish - shart bajarilishi bilan darhol qaytadi
            try:
                wait.until(lambda driver:
                           driver.execute_script("return document.readyState") == "complete" and
                           driver.execute_script(
                               "return typeof jQuery !== 'undefined' ? jQuery.active === 0 : true;") and
                           driver.execute_script("""
                        return window.performance
                            .getEntriesByType('resource')
                            .filter(r => !r.responseEnd && 
                                (r.initiatorType === 'fetch' || 
                                r.initiatorType === 'xmlhttprequest')
                            ).length === 0;
                    """)
                           )
            except TimeoutException:
                logging.warning("Async operatsiyalar kutish vaqti tugadi")
                return False

            # 2. Loading indikatorlarni tekshirish - darhol
            loading_indicators = [
                ".loading", ".loader", "#loading",
                "[class*='loading']", "[class*='spinner']",
                "[id*='loading']", ".preloader", "#spinner"
            ]

            elements = []
            for indicator in loading_indicators:
                try:
                    # Darhol tekshirish
                    elements.extend(self.driver.find_elements(By.CSS_SELECTOR, indicator))
                except Exception as e:
                    logging.debug(f"Loading indikatorni tekshirishda xatolik: {str(e)}")
                    continue

            # Agar ko'rinadigan loading indikatorlar topilsa, ularning yo'qolishini kutamiz
            visible_loaders = [e for e in elements if e.is_displayed()]
            if visible_loaders:
                try:
                    # Faqat ko'rinadigan loading indikatorlar yo'qolishini kutish
                    wait.until(lambda driver:
                               not any(loader.is_displayed() for loader in visible_loaders
                                       if self._is_element_still_attached(loader))
                               )
                except TimeoutException:
                    logging.warning("Loading indikatorlar yo'qolmadi")
                    return False

            # 3. Asosiy kontentni tekshirish
            main_selectors = [
                "main", "#main", "#content", ".main-content",
                "article", ".content", "#app", "#root", "body"
            ]

            # Avval mavjud elementlarni tezkor tekshirish
            for selector in main_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if any(e.is_displayed() and len(e.text.strip()) > 0 for e in elements):
                        elapsed_time = current_time() - start_time
                        logging.info(f"Sahifa {elapsed_time:.1f} sekund ichida yuklandi")
                        return True
                except Exception:
                    continue

            # Agar tezkor tekshiruvda topilmasa, kutish rejimiga o'tish
            for selector in main_selectors:
                try:
                    wait.until(lambda driver:
                               any(e.is_displayed() and len(e.text.strip()) > 0
                                   for e in driver.find_elements(By.CSS_SELECTOR, selector))
                               )
                    elapsed_time = current_time() - start_time
                    logging.info(f"Sahifa {elapsed_time:.1f} sekund ichida yuklandi")
                    return True
                except Exception as e:
                    logging.debug(f"Kontentni tekshirishda xatolik: {str(e)}")
                    continue

            logging.warning("Asosiy kontent topilmadi")
            return False

        except TimeoutException:
            elapsed_time = current_time() - start_time
            logging.error(f"Sahifa {elapsed_time:.1f} sekund kutildi, lekin yuklanmadi")
            self.take_screenshot("page_load_timeout")
            return False
        except Exception as e:
            elapsed_time = current_time() - start_time
            logging.error(f"Sahifani tekshirishda xatolik ({elapsed_time:.1f}s): {str(e)}")
            self.take_screenshot("page_load_error")
            return False

    def _is_element_still_attached(self, element):
        """Elementning hali ham DOMda mavjudligini tekshirish"""
        try:
            element.is_enabled()
            return True
        except Exception:
            return False
    # ------------------------------------------------------------------------------------------------------------------

    # def wait_for_page_load_2(self, timeout=None):
    #     timeout = timeout if timeout else self.default_timeout
    #     wait = self._get_wait(timeout)
    #     start_time = current_time()
    #
    #     try:
    #         # 1. Async operatsiyalarni tekshirish
    #         is_ready = wait.until(lambda driver:
    #                               driver.execute_script("return document.readyState") == "complete"
    #                               and driver.execute_script(
    #                                   "return typeof jQuery !== 'undefined' ? jQuery.active === 0 : true;"
    #                               )
    #                               and driver.execute_script("""
    #                 return window.performance
    #                     .getEntriesByType('resource')
    #                     .filter(r => !r.responseEnd &&
    #                         (r.initiatorType === 'fetch' ||
    #                          r.initiatorType === 'xmlhttprequest')
    #                     ).length === 0;
    #             """)
    #                               )
    #
    #         if not is_ready:
    #             logging.warning("Sahifa async operatsiyalari tugamadi")
    #             return False
    #
    #         # 2. Loading indikatorlarni tekshirish
    #         loading_indicators = [
    #             ".loading", ".loader", "#loading",
    #             "[class*='loading']", "[class*='spinner']",
    #             "[id*='loading']", ".preloader", "#spinner"
    #         ]
    #
    #         for indicator in loading_indicators:
    #             # Har bir loading indikator uchun tez tekshirish (0.5 sekund)
    #             try:
    #                 elements = self.driver.find_elements(By.CSS_SELECTOR, indicator)
    #                 if any(element.is_displayed() for element in elements):
    #                     logging.warning(f"Loading indikator topildi: {indicator}")
    #                     return False
    #             except Exception as e:
    #                 logging.debug(f"Loading indikatorni tekshirishda xatolik: {str(e)}")
    #                 continue
    #
    #         # 3. Asosiy kontentni tekshirish
    #         main_selectors = [
    #             "main", "#main", "#content", ".main-content",
    #             "article", ".content", "#app", "#root", "body"
    #         ]
    #
    #         for selector in main_selectors:
    #             try:
    #                 elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
    #                 if elements and any(len(e.text.strip()) > 0 for e in elements):
    #                     elapsed_time = current_time() - start_time
    #                     logging.info(f"Sahifa {elapsed_time:.1f} sekund ichida yuklandi")
    #                     return True
    #             except Exception as e:
    #                 logging.debug(f"Kontentni tekshirishda xatolik: {str(e)}")
    #                 continue
    #
    #         logging.warning("Sahifada asosiy kontent topilmadi")
    #         return False
    #
    #     except TimeoutException:
    #         elapsed_time = current_time() - start_time
    #         logging.error(f"Sahifa {elapsed_time:.1f} sekund kutildi, lekin yuklanmadi")
    #         self.take_screenshot("page_load_timeout")
    #         return False
    #
    #     except Exception as e:
    #         elapsed_time = current_time() - start_time
    #         logging.error(f"Sahifani tekshirishda xatolik ({elapsed_time:.1f}s): {str(e)}")
    #         self.take_screenshot("page_load_error")
    #         return False
