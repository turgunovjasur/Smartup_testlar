import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


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

    def take_screenshot(self, filename):
        screenshot_dir = "screenshot_dir"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        screenshot_path = os.path.join(screenshot_dir, f"{filename}.png")
        self.driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved at {screenshot_path}")

    def extra_click_after_selection(self, locator):
        try:
            element = self.wait_for_element_clickable((By.XPATH, locator))
            if element:
                element.click()
            else:
                print(f"Element not clickable: {locator}")
        except Exception as e:
            print(f"Error clicking element after selection: {e}")

    def get_element(self, locator):
        return WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(locator))

    def long_press(self, locator, duration=1000):
        element = self.get_element(locator)
        self.driver.execute_script("""
            const element = arguments[0];
            const duration = arguments[1];
            const mouseDownEvent = new MouseEvent('mousedown', { bubbles: true });
            element.dispatchEvent(mouseDownEvent);
            setTimeout(() => {
                const mouseUpEvent = new MouseEvent('mouseup', { bubbles: true });
                element.dispatchEvent(mouseUpEvent);
            }, duration);
        """, element, duration)

    def hover_and_hold(self, locator, duration=2000):
        element = self.get_element(locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        time.sleep(duration / 1000)

    def extract_count(self, xpath):
        element = self.wait_for_element_visible((By.XPATH, xpath), timeout=20)
        if element and element.text.strip():
            count = ''.join(filter(str.isdigit, element.text.strip()))
            return int(count) if count else 0
        else:
            print(f"Ogohlantirish: {xpath} uchun element bo'sh yoki topilmadi")
            return 0

    def check_counts(self, *xpaths):
        try:
            return [self.extract_count(xpath) for xpath in xpaths]
        except Exception as e:
            print(f"Check counts error: {str(e)}")
            self.take_screenshot("check_counts_error")
            return [0] * len(xpaths)

    def check_calculations(self, expected_values, actual_xpaths, labels):
        try:
            actual_values = self.check_counts(*actual_xpaths)
            results = []
            for expected, actual, label in zip(expected_values, actual_values, labels):
                result = "True" if expected == actual else "False"
                results.append(f"Hisoblangan {label}: {expected}, Tekshirilgan qiymat: {actual}, {label} {result}")
            return results
        except Exception as e:
            print(f"Error: {str(e)}")
            self.take_screenshot("calculations_error")
            return []
