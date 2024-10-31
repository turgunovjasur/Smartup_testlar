import os
import time
import re
import allure
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.default_timeout = 20
        self.wait = WebDriverWait(self.driver, self.default_timeout)
        self.logger = logging.getLogger(__name__)
    # ------------------------------------------------------------------------------------------------------------------

    def is_element_visible(self, locator, timeout=20):
        element = WebDriverWait(self.driver, timeout=timeout).until(EC.visibility_of_element_located(locator))
        return bool(element)
    # ------------------------------------------------------------------------------------------------------------------

    def wait_for_element_clickable(self, locator, timeout=None, poll_frequency=0.5):
        timeout = timeout or self.default_timeout
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # Sahifaning yuklanishini tekshirish
                page_state = self.driver.execute_script('return document.readyState')
                if page_state != 'complete':
                    self.logger.debug("Page is still loading, waiting...")
                    time.sleep(poll_frequency)
                    continue

                # Element bosilishi mumkinligini tekshirish
                element = WebDriverWait(self.driver, poll_frequency).until(
                    EC.element_to_be_clickable(locator)
                )
                return element
            except StaleElementReferenceException:
                self.logger.debug(f"Stale element, retrying: {locator}")
            except TimeoutException:
                self.logger.debug(f"Element not clickable, retrying: {locator}")
            except Exception as e:
                self.logger.error(f"Unexpected error while waiting for element: {e}")

        self.logger.error(f"Element not clickable or page not loaded within {timeout} seconds: {locator}")
        # self.take_screenshot("page_load_or_element_not_clickable_error")
        return None
    # ------------------------------------------------------------------------------------------------------------------

    def wait_for_element_visible(self, locator, timeout=None, poll_frequency=0.5):
        timeout = timeout or self.default_timeout
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # Sahifaning yuklanishini tekshirish
                page_state = self.driver.execute_script('return document.readyState')
                if page_state != 'complete':
                    self.logger.debug("Page is still loading, waiting...")
                    time.sleep(poll_frequency)
                    continue

                # Elementning ko'rinishini tekshirish
                element = WebDriverWait(self.driver, poll_frequency).until(
                    EC.visibility_of_element_located(locator)
                )
                return element
            except StaleElementReferenceException:
                self.logger.debug(f"Stale element, retrying: {locator}")
            except TimeoutException:
                self.logger.debug(f"Element not visible, retrying: {locator}")
            except Exception as e:
                self.logger.error(f"Unexpected error while waiting for element: {e}")

        self.logger.error(f"Element not visible or page not loaded within {timeout} seconds: {locator}")
        # self.take_screenshot("page_load_or_element_not_visible_error")
        return None
    # ------------------------------------------------------------------------------------------------------------------

    def click(self, locator, timeout=None):
        element = self.wait_for_element_clickable(locator, timeout=timeout)
        if element:
            element.click()
        else:
            raise Exception("Submit button not clickable or page not loaded")
    # ------------------------------------------------------------------------------------------------------------------

    def click_js(self, locator, timeout=None):
        element = self.wait_for_element_clickable(locator, timeout=timeout)
        self.driver.execute_script("arguments[0].click();", element)
    # ------------------------------------------------------------------------------------------------------------------

    def click_circle(self, locator, max_attempts=None):
        if max_attempts is None:
            max_attempts = 3

        for attempt in range(1, max_attempts + 1):
            try:
                element = self.wait_for_element_clickable(locator)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                element.click()
                break
            except StaleElementReferenceException:
                print(f"Attempt {attempt}: Trying to click again...")
    # ------------------------------------------------------------------------------------------------------------------

    def input_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    # ------------------------------------------------------------------------------------------------------------------

    def input_text_elem(self, locator, elem_locator, timeout=None):
        self.click(locator, timeout=timeout)
        self.click(elem_locator, timeout=timeout)
    # ------------------------------------------------------------------------------------------------------------------

    def find_element(self, locator, timeout=None):
        return self.wait_for_element_visible(locator, timeout=timeout)
    # ------------------------------------------------------------------------------------------------------------------

    def get_element(self, locator):
        return self.wait_for_element_visible(locator)
    # ------------------------------------------------------------------------------------------------------------------

    def get_text(self, locator):
        return self.get_element(locator).text
    # ------------------------------------------------------------------------------------------------------------------

    def get_numeric_value(self, locator):
        text = self.get_text(locator)
        # print(f'get_text: {text}')
        if text is None:
            print("Element topilmadi yoki ko'rinmayapti.")
            return None
        text = text.strip()
        numeric_value = re.sub(r'[^0-9.]', '', text)
        if numeric_value.count('.') <= 1:
            return float(numeric_value) if numeric_value else 0
        return None
    # ------------------------------------------------------------------------------------------------------------------

    def click_multiple_time(self, locator, click_count=2, delay=1):
        for _ in range(click_count):
            self.click(locator)
            time.sleep(delay)
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
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        time.sleep(duration / 1000)
    # ------------------------------------------------------------------------------------------------------------------

    def check_count(self, locator):
        try:
            element = self.wait_for_element_visible(locator, timeout=5)
            if element:
                count_text = element.text.strip()
                if count_text:
                    count = ''.join(filter(str.isdigit, count_text))
                    return int(count) if count else 0
                else:
                    print("Warn: the count element is empty")
                    return 0
            else:
                print("Warn: count element not found")
                return 0
        except Exception as e:
            print(f"Check_count_error: {str(e)}")
            self.take_screenshot("check_count_error")
            return 0
    # ------------------------------------------------------------------------------------------------------------------

    def get_current_url(self):
        return self.driver.current_url

    # ------------------------------------------------------------------------------------------------------------------
    def cut_url(self):
        current_url = self.get_current_url()
        keywords = ["anor/", "trade/", "core/"]
        positions = [current_url.find(keyword) for keyword in keywords if current_url.find(keyword) != -1]

        if positions:
            min_position = min(positions)
            cut_url = current_url[:min_position]
        else:
            cut_url = current_url

        return cut_url
    # ------------------------------------------------------------------------------------------------------------------

