import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def click(self, locator):
        self.wait_for_element_clickable(locator).click()

    def clear_and_send_keys(self, locator, text):
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)

    def wait_for_element_clickable(self, locator):
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            print(f"Element not clickable within: {self.timeout} seconds: {locator}")
            return None

    def wait_for_element_visible(self, locator, timeout=None):
        if timeout is None:
            timeout = self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            print(f"Element not visible within: {timeout} seconds: {locator}")
            return None

    def input_text(self, locator, text):
        self.clear_and_send_keys(locator, text)
        self.click(locator)

    def input_text_elem(self, locator, elem_locator):
        self.click(locator)
        self.wait_and_click(elem_locator)

    def wait_and_click(self, locator):
        self.click(locator)

    def take_screenshot(self, name, screenshot_dir="screenshot"):
        if not os.path.exists(screenshot_dir):
            os.makedirs("screenshot_dir")
        self.driver.save_screenshot(f"{screenshot_dir}/{name}.png")

    def extra_click_after_selection(self, locator):
        try:
            element = self.wait_for_element_clickable((By.XPATH, locator))
            if element:
                element.click()
            else:
                print(f"Element not clickable: {locator}")
        except Exception as e:
            print(f"Error clicking element after selection: {e}")