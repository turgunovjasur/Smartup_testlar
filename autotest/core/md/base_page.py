import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.default_timeout = 20

    # ------------------------------------------------------------------------------------------------------------------
    def click(self, locator, timeout=None):
        self.wait_for_element_clickable(locator, timeout).click()

    # ------------------------------------------------------------------------------------------------------------------
    def click_js(self, locator, timeout=None):
        element = self.wait_for_element_clickable(locator, timeout)
        self.driver.execute_script("arguments[0].click();", element)

    # ------------------------------------------------------------------------------------------------------------------

    def clear_and_send_keys(self, locator, text):
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)
    # ------------------------------------------------------------------------------------------------------------------

    def wait_for_element_clickable(self, locator, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            print(f"Element not clickable within: {timeout} seconds: {locator}")
            return None
    # ------------------------------------------------------------------------------------------------------------------

    def wait_for_element_visible(self, locator, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            print(f"Element not visible within: {timeout} seconds: {locator}")
            return None
    # ------------------------------------------------------------------------------------------------------------------

    def input_text(self, locator, text):
        self.clear_and_send_keys(locator, text)
        self.click(locator)
    # ------------------------------------------------------------------------------------------------------------------

    def input_text_elem(self, locator, elem_locator):
        self.click(locator)
        self.click(elem_locator)
    # ------------------------------------------------------------------------------------------------------------------

    def input_text_elem_js(self, locator, elem_locator):
        self.click_js(locator)
        self.click_js(elem_locator)
    # ------------------------------------------------------------------------------------------------------------------

    def take_screenshot(self, filename):
        filename = str(filename)
        screenshot_dir = "screenshot_dir"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        screenshot_path = os.path.join(screenshot_dir, f"{filename}.png")
        self.driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved at {screenshot_path}")
    # ------------------------------------------------------------------------------------------------------------------

    def click_multiple_time(self, locator, click_count=2, delay=1, timeout=None):
        for _ in range(click_count):
            self.click(locator, timeout)
            time.sleep(delay)
    # ------------------------------------------------------------------------------------------------------------------

    def get_element(self, locator):
        return WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(locator))
    # ------------------------------------------------------------------------------------------------------------------

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
    # ------------------------------------------------------------------------------------------------------------------

    def hover_and_hold(self, locator, duration=2000):
        element = self.get_element(locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        time.sleep(duration / 1000)
    # ------------------------------------------------------------------------------------------------------------------

    def get_element_value(self, xpath, as_int=False):
        try:
            element = self.wait_for_element_visible((By.XPATH, xpath), timeout=20)
            if element:
                text = element.text.strip()
                if as_int:
                    return int(''.join(filter(str.isdigit, text))) if text else 0
                else:
                    return text
            else:
                print(f"Warning: {xpath} not found")
                return 0 if as_int else ""
        except ValueError:
            print(f"Warning: {xpath} could not convert text to number")
            return 0
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            self.take_screenshot("get_element_value_error")
            return 0 if as_int else ""
    # ------------------------------------------------------------------------------------------------------------------

    def elements_equal(self, xpath1, xpath2, as_int=False):

        try:
            value1 = self.get_element_value(xpath1, as_int=True)
            value2 = self.get_element_value(xpath2, as_int=True)

            is_equal = value1 == value2
            result = "equal" if is_equal else "not equal"

            print(f"Result: {result}")

            return is_equal
        except Exception as e:
            print(f"Error comparing values: {str(e)}")
            self.take_screenshot("compare_elements_error")
            return False
    # ------------------------------------------------------------------------------------------------------------------

    def check_count(self, count_xpath):
        try:
            element = self.wait_for_element_visible((By.XPATH, count_xpath), timeout=20)
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
