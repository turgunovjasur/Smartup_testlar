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

from utils.exception import (
    ElementInteractionError,
    ElementNotFoundError,
    ElementStaleError,
    ElementNotClickableError,
    ScrollError,
    LoaderTimeoutError, ElementVisibilityError
)
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

    def _wait_for_async_operations(self, timeout=None):
        """Sahifadagi asinxron operatsiyalar tugashini kutish."""

        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

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
        try:
            WebDriverWait(self.driver, timeout).until(lambda driver: driver.execute_script(async_check_script))
            return True

        except TimeoutException:
            error_message = f"Asinxron operatsiyalar {timeout}s ichida tugallanmadi"
            self.logger.error(f"{page_name}: {error_message}")
            raise LoaderTimeoutError(error_message)
        except Exception as e:
            error_message = f"Asinxron operatsiyalar tekshirishda kutilmagan xato: {str(e)}"
            self.logger.error(f"{page_name}: {error_message}")
            raise LoaderTimeoutError(error_message)

    def _wait_for_block_ui_absence(self, timeout=None):
        """
            Block UI yo'qolishini kutish.
            JavaScript orqali Block UI holatini tekshiradi.
            blockUI va blockUIConfig obyektlarining mavjudligi va holatini tekshiradi.
            Faqat JavaScript darajasida ishlaydi.
        """
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        block_ui_script = """
            return (
                (typeof blockUI === 'undefined' || !blockUI.state() || !blockUI.state().blocking) &&
                (typeof blockUIConfig === 'undefined' || blockUIConfig.autoBlock !== false)
            );
        """

        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script(block_ui_script)
            )
            return True

        except TimeoutException:
            error_message = f"Block UI {timeout}s ichida yo'qolmadi"
            self.logger.error(f"{page_name}: {error_message}")
            raise LoaderTimeoutError(error_message)
        except Exception as e:
            error_message = f"Block UI tekshirishda kutilmagan xato: {str(e)}"
            self.logger.error(f"{page_name}: {error_message}")
            raise LoaderTimeoutError(error_message)

    def _check_spinner_absence(self, timeout=None):
        """
            Spinner yo'qolishini kutish.
            DOM elementlarini tekshiradi (4 ta CSS selector orqali)
            Angular scope holatini tekshiradi.
            Ham DOM, ham JavaScript darajasida ishlaydi.
        """
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        # Block UI container va uning ichki elementlari uchun locatorlar
        block_ui_locators = [
            (By.CSS_SELECTOR, "div.block-ui-container"),
            (By.CSS_SELECTOR, "div.block-ui-overlay"),
            (By.CSS_SELECTOR, "div.block-ui-message-container"),
            (By.CSS_SELECTOR, "img[src='assets/img/loading.svg']")
        ]

        try:
            for locator in block_ui_locators:
                WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))

            # Angular scope holatini tekshirish
            angular_scope_script = """
                return (typeof angular === 'undefined') || 
                       !document.querySelector('.block-ui-container.ng-scope') ||
                       angular.element(document.querySelector('.block-ui-container')).scope().state.blocking === false;
            """

            WebDriverWait(self.driver, timeout).until(lambda driver: driver.execute_script(angular_scope_script))
            return True

        except TimeoutException:
            error_message = f"Block UI spinneri {timeout}s ichida yo'qolmadi"
            self.logger.error(f"{page_name}: {error_message}")
            raise LoaderTimeoutError(error_message)
        except Exception as e:
            error_message = f"Block UI spinnerini tekshirishda kutilmagan xato: {str(e)}"
            self.logger.error(f"{page_name}: {error_message}")
            raise LoaderTimeoutError(error_message)

    def _wait_for_all_loaders(self, timeout=None, log_text=None):
        """Sahifaning to'liq barqaror holatga kelishini kutish."""

        page_name = self.__class__.__name__

        status_text = f"{log_text}: ->" if log_text else ""
        self.logger.debug(f"{page_name}: {status_text} Sahifa yuklanishini kutish boshlandi")

        try:
            self._wait_for_async_operations(timeout)
            self._wait_for_block_ui_absence(timeout)
            self._check_spinner_absence(timeout)
            self.logger.debug(f"{page_name}: {status_text} Sahifa yuklandi")
            return True

        except LoaderTimeoutError as e:
            self.logger.error(f"{page_name}: {status_text} Sahifa yuklanishida xato: {str(e)}")
            raise

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

    def _wait_for_presence(self, locator, timeout=None, error_message=True):
        """Element DOMda mavjud ekanligini tekshirish"""
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        try:
            # # Sahifa yuklanishini tekshirish
            # try:
            #     self._wait_for_all_loaders(log_text='DOM')
            # except LoaderTimeoutError:
            #     raise

            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return element

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
                self.logger.error(f"{page_name}: Element DOM da topilmadi: {locator}")
            raise ElementNotFoundError(
                message="Element topilmadi",
                locator=locator,
                original_error=e
            )

        except Exception as e:
            if error_message:
                self.logger.error(f"{page_name}: Element qidirishda kutilmagan xato: {e}")
            raise ElementInteractionError(
                message=f"Kutilmagan xato: {str(e)}",
                locator=locator,
                original_error=e
            )

    def _scroll_to_element(self, element, locator):
        """Element ga scroll qilish"""
        page_name = self.__class__.__name__

        if element.is_displayed():
            # self.logger.debug(f"{page_name}: Element scroll kerak emas!: {locator}")
            return element

        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(0.5)

            if not element.is_displayed():
                self.logger.warning(f"{page_name}: Element scroll qilingandan keyin ham ko'rinmadi: {locator}")
                raise ScrollError(
                    message="Element scroll qilingandan keyin ham ko'rinmadi",
                    locator=locator
                )
            return element

        except StaleElementReferenceException as e:
            raise ElementStaleError(
                message="Scroll paytida element yangilandi",
                locator=locator,
                original_error=e
            )
        except Exception as e:
            raise ScrollError(
                message=f"Element scroll qilib bo'lmadi",
                locator=locator,
                original_error=e
            )

    def _wait_for_visibility(self, locator, timeout=None, error_message=True):
        """Element ko'rinishini kutish"""
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        try:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return element

        except StaleElementReferenceException as e:
            if error_message:
                self.logger.warning(f"{page_name}: Element DOM da yangilandi: {locator}")
            raise ElementStaleError(
                message="Element ko'rinishini kutishda yangilandi",
                locator=locator,
                original_error=e
            )

        except TimeoutException as e:
            if error_message:
                self.logger.error(f"{page_name}: Element ko'rinmadi: {locator}")
            raise ElementNotFoundError(
                message="Element ko'rinmadi",
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

    def _wait_for_clickable(self, locator, timeout=None, error_message=True):
        """Element bosiladigan holatda ekanligini tekshirish"""
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            return element

        except StaleElementReferenceException as e:
            if error_message:
                self.logger.warning(f"{page_name}: Element DOM da yangilandi: {locator}")
            raise ElementStaleError(
                message="Element bosiladigan holatga kelishda yangilandi",
                locator=locator,
                original_error=e
            )

        except TimeoutException as e:
            if error_message:
                self.logger.error(f"{page_name}: Element bosilmaydigan holatda: {locator}")
            raise ElementNotClickableError(
                message="Element bosilmaydigan holatda",
                locator=locator,
                original_error=e
            )

        except Exception as e:
            if error_message:
                self.logger.error(f"{page_name}: Element tekshirishda kutilmagan xato: {e}")
            raise ElementInteractionError(
                message=f"Kutilmagan xato: {str(e)}",
                locator=locator,
                original_error=e
            )

    # Click ------------------------------------------------------------------------------------------------------------

    def is_displayed_block_ui(self, timeout=None):
        """Block UI elementining ko'rinishini tekshiradi.

        Returns:
            bool: True agar loading ko'rinsa, False agar ko'rinmasa
        """
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout
        block_ui_locator = (By.CSS_SELECTOR, "img[src='assets/img/loading.svg']")

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(block_ui_locator)
            )
            self.logger.info(f"@ {page_name}: block_ui DOM da topildi")

            is_visible = element.is_displayed()
            if is_visible:
                self.logger.info(f"@ {page_name}: block_ui ko'rindi")
                return True
            else:
                self.logger.info(f"@ {page_name}: block_ui ko'rinmadi")
                return False

        except TimeoutException:
            self.logger.info(f"@ {page_name}: block_ui topilmadi")
            return False
        except WebDriverException as e:
            self.logger.error(f"@ {page_name}: block_ui tekshirishda xatolik: {str(e)}")
            raise

    def click(self, locator, retries=3, retry_delay=1):
        """Elementni bosish funksiyasi"""
        page_name = self.__class__.__name__
        self.logger.debug(f"{page_name}: Element bosilmoqda: {locator}")

        attempt = 0
        while attempt < retries:
            try:
                # Sahifa yuklanishini tekshirish
                try:
                    self._wait_for_all_loaders(log_text='Click')
                except LoaderTimeoutError:
                    raise

                # Element bilan ishlash
                element_dom = self._wait_for_presence(locator)
                self._scroll_to_element(element_dom, locator)
                self._wait_for_visibility(locator)
                element_clickable = self._wait_for_clickable(locator)

                # Click urinishlari
                if self._click(element_clickable, locator):
                    return True

                time.sleep(retry_delay)
                if self._click(element_clickable, locator, retry=True):
                    return True

                time.sleep(retry_delay)
                if self._click_js(element_dom, locator):
                    return True

                # Sahifa yuklanishini tekshirish
                try:
                    self._wait_for_all_loaders()
                except LoaderTimeoutError as e:
                    self.logger.error(f"{page_name}: Click: -> 2)Sahifa yuklanish xatosi: {str(e)}")
                    raise

                # Barcha click urinishlari muvaffaqiyatsiz bo'lsa
                raise ElementNotClickableError(
                    "Element barcha usullar bilan bosilmadi",
                    locator=locator
                )

            except (ElementStaleError, ElementNotClickableError, ScrollError) as e:
                # Elementning yangilanishi yoki bosilmasligi bilan bog'liq xatoliklar
                if attempt == retries - 1:
                    self.logger.error(f"{page_name}: {e.message}")
                    self.take_screenshot(f"{page_name.lower()}_click_error")
                    raise

                self.logger.warning(f"{page_name}: {e.message}, qayta urinish ({attempt + 1}/{retries})")
                time.sleep(retry_delay)
                attempt += 1
                continue

            except ElementNotFoundError as e:
                # Bu xatoliklar uchun qayta urinish mantiqsiz
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
        self.logger.debug(f"{page_name}: Element qidirilmoqda: {locator}")

        timeout = timeout or self.default_timeout
        attempt = 0

        while attempt < retries:
            try:
                # Sahifa yuklanishini tekshirish
                try:
                    self._wait_for_all_loaders(log_text='Visible')
                except LoaderTimeoutError:
                    raise

                # Element bilan ishlash
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

            except (ElementStaleError, ScrollError) as e:
                # Element yangilanishi bilan bog'liq xatoliklar
                if attempt == retries - 1:
                    self.logger.error(f"{page_name}: {e.message}")
                    self.take_screenshot(f"{page_name.lower()}_visibility_error")
                    raise

                self.logger.warning(f"{page_name}: {e.message}, qayta urinish ({attempt + 1}/{retries})")
                time.sleep(retry_delay)
                attempt += 1
                continue

            except (ElementNotFoundError) as e:
                # Bu xatoliklar uchun qayta urinish mantiqsiz
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
    def _wait_for_presence_all(self, locator, timeout=None, error_message=True):
        """Elementlar ro'yxatini kutish funksiyasi."""
        page_name = self.__class__.__name__
        timeout = timeout or self.default_timeout

        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            if not elements:
                self.logger.warning(f"{page_name}: Elementlar topilmadi: {locator}")
            return elements

        except StaleElementReferenceException as e:
            if error_message:
                self.logger.warning(f"{page_name}: Elementlar DOM da yangilandi: {locator}")
            raise ElementStaleError(
                message="Elementlar DOM da yangilandi",
                locator=locator,
                original_error=e
            )

        except TimeoutException as e:
            if error_message:
                self.logger.error(f"{page_name}: Elementlar topilmadi: {locator}")
            raise ElementNotFoundError(
                message="Elementlar topilmadi",
                locator=locator,
                original_error=e
            )

        except Exception as e:
            if error_message:
                self.logger.error(f"{page_name}: Elementlarni qidirishda kutilmagan xato: {e}")
            raise ElementInteractionError(
                message=f"Kutilmagan xato: {str(e)}",
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

    def input_text(self, locator, text):
        """Element topib, matn kiritish funksiyasi"""
        page_name = self.__class__.__name__
        self.logger.debug(f"{page_name}: Matn kiritilmoqda: {locator}")

        try:
            # Sahifa yuklanishini alohida tekshirish
            try:
                self._wait_for_all_loaders(log_text='input_text')
            except LoaderTimeoutError:
                self.take_screenshot(f"{page_name.lower()}_loader_error")
                raise

            # Element bilan ishlash
            element_dom = self._wait_for_presence(locator)
            self._scroll_to_element(element_dom, locator)
            element_clickable = self._wait_for_clickable(locator)

            # Matn kiritish
            element_clickable.clear()
            element_clickable.send_keys(text)
            self.logger.info(f"⏺ {page_name}: Input: {locator} -> {text}")
            return True

        except (ElementNotFoundError, ElementStaleError, ScrollError, ElementNotClickableError) as e:
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

    def find_row_and_click(self, element_name, xpath_pattern=None, timeout=None,
                           expand=False, checkbox=False, limit=3):
        """Jadvaldagi qatorni topish va ustiga bosish funksiyasi."""

        page_name = self.__class__.__name__
        self.logger.debug(f"{page_name}: Jadval qatori qidirilmoqda: {element_name}")

        if not xpath_pattern:
            xpath_pattern = ("//div[contains(@class, 'tbl')]//div[contains(@class, 'tbl-row')]"
                             "//div[contains(@class, 'tbl-cell') and normalize-space(text())='{}']")

        row_locator = (By.XPATH, xpath_pattern.format(element_name))
        limit_button = (By.XPATH, '//button[@class="btn btn-default rounded-0 ng-binding"]')

        timeout = timeout or self.default_timeout

        def change_limit(new_limit):
            """Jadval sahifasidagi elementlar sonini o'zgartirish."""
            try:
                # Limit tugmasini bosish
                if not self.click(limit_button):
                    raise ElementNotClickableError(
                        message="Limit tugmasini bosib bo'lmadi",
                        locator=limit_button
                    )

                # Kerakli limitni tanlash
                limit_option = (By.XPATH,
                                f'//button[@class="btn btn-default rounded-0 ng-binding"]'
                                f'/following-sibling::div/a[{new_limit}]'
                                )
                if not self.click(limit_option):
                    raise ElementNotClickableError(
                        message=f"Limit {new_limit} ni tanlab bo'lmadi",
                        locator=limit_option
                    )

                # Loader tugashini kutish
                self._wait_for_all_loaders()
                return True

            except (ElementNotClickableError, LoaderTimeoutError) as e:
                self.logger.error(f"{page_name}: Limit o'zgartirishda xatolik: {e.message}")
                raise

        def click_checkbox_for_row():
            """Qator uchun checkbox ni bosish."""
            try:
                checkbox_locator = (
                    By.XPATH,
                    f"//div[contains(@class, 'tbl-row') and .//div[text()='{element_name}']]//span"
                )
                checkbox_element = self._wait_for_presence(checkbox_locator)

                if not self._click_js(checkbox_element, checkbox_locator):
                    raise ElementNotClickableError(
                        message="Checkbox ni bosib bo'lmadi",
                        locator=checkbox_locator
                    )
                return True

            except ElementNotFoundError as e:
                self.logger.error(f"{page_name}: Checkbox topilmadi: {e.message}")
                raise

            except ElementNotClickableError as e:
                self.logger.error(f"{page_name}: Checkbox bosilmadi: {e.message}")
                raise

        def find_and_click_row():
            """Qatorni topish va bosish."""
            try:
                # Sahifa yuklanishini alohida tekshirish
                try:
                    self._wait_for_all_loaders(log_text='find_and_click_row')
                except LoaderTimeoutError:
                    self.take_screenshot(f"{page_name.lower()}_loader_error")
                    raise

                # Qatorni qidirish
                elements = self._wait_for_presence_all(row_locator, timeout)
                if not elements:
                    # Agar limit o'rnatilgan bo'lsa, limitni oshirib qayta qidirish
                    if limit:
                        self.logger.info(f"{page_name}: '{element_name}' topilmadi. "
                                         f"Limit {limit} ga o'zgartiriladi")
                        change_limit(limit)
                        elements = self._wait_for_presence_all(row_locator)
                        if not elements:
                            raise ElementNotFoundError(
                                message=f"Qator '{element_name}' limit o'zgartirilgandan "
                                        f"keyin ham topilmadi",
                                locator=row_locator
                            )
                    else:
                        raise ElementNotFoundError(
                            message=f"Qator '{element_name}' topilmadi",
                            locator=row_locator
                        )

                target_element = elements[0]

                self._scroll_to_element(target_element, row_locator)
                self._wait_for_visibility(row_locator)

                # Qatorni bosish
                if not self.click(row_locator):
                    raise ElementNotClickableError(
                        message=f"Qator '{element_name}' ni bosib bo'lmadi",
                        locator=row_locator
                    )

                # Agar checkbox belgilangan bo'lsa
                if checkbox:
                    click_checkbox_for_row()
                return True

            except (ElementNotFoundError, ElementNotClickableError, ElementStaleError) as e:
                self.logger.error(f"{page_name}: {e.message}")
                self.take_screenshot(f"{page_name.lower()}_find_row_error")
                raise

            except Exception as e:
                self.logger.error(f"{page_name}: Kutilmagan xatolik: {str(e)}")
                self.take_screenshot(f"{page_name.lower()}_find_row_error")
                raise ElementInteractionError(
                    message=f"Kutilmagan xatolik: {str(e)}",
                    locator=row_locator,
                    original_error=e
                )

        try:
            # Jadval hajmini kengaytirish
            if expand:
                change_limit(4)

            # Qatorni topish va bosish
            return find_and_click_row()

        except Exception as e:
            self.logger.error(f"{page_name}: {str(e)}")
            self.take_screenshot(f"{page_name.lower()}_find_row_error")
            return False

    # ------------------------------------------------------------------------------------------------------------------
