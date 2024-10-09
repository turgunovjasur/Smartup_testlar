import os
import time
import re
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.default_timeout = 20
        self.wait = WebDriverWait(self.driver, self.default_timeout)

    # ------------------------------------------------------------------------------------------------------------------
    def wait_for_element_clickable(self, locator, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.element_to_be_clickable(locator))

        except TimeoutException:
            print(f"Element not clickable within: {timeout} seconds: {locator}")
            # self.take_screenshot("element_not_clickable_error")
            return None
    # ------------------------------------------------------------------------------------------------------------------

    def wait_for_element_visible(self, locator, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            print(f"Element not visible within: {timeout} seconds: {locator}")
            # self.take_screenshot("element_not_visible_error")
            return None
    # ------------------------------------------------------------------------------------------------------------------

    def wait_for_all_elements_visible(self, locator, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.visibility_of_all_elements_located(locator))
        except TimeoutException:
            print(f"Elements not visible within: {timeout} seconds: {locator}")
            # self.take_screenshot("elements_not_visible_error")
            return None
    # ------------------------------------------------------------------------------------------------------------------

    def click(self, locator, timeout=None):
        element = self.wait_for_element_clickable(locator, timeout=timeout)
        if element:
            element.click()
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
        return self.wait_for_element_clickable(locator, timeout=timeout)
    # ------------------------------------------------------------------------------------------------------------------

    def find_elements(self, locator):
        return self.wait_for_all_elements_visible(locator)
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
