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

    def check_counts(self, *xpaths):
        try:
            return [self.get_element_value(xpath, as_int=True) for xpath in xpaths]
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
                results.append(f"Calculated {label}: {expected}, Checked value: {actual}, {label} {result}")
            return results
        except Exception as e:
            print(f"Error: {str(e)}")
            self.take_screenshot("calculations_error")
            return []

    def get_element_value(self, xpath, as_int=False):
        """
        Berilgan XPath orqali elementning matnini qaytaradi yoki integer qiymat sifatida qaytaradi.
        :param xpath: elementning XPath'i
        :param as_int: True bo'lsa, matnni integer qiymatga aylantirib qaytaradi
        :return: element matni yoki integer qiymati
        """
        try:
            element = self.wait_for_element_visible((By.XPATH, xpath), timeout=20)
            if element:
                text = element.text.strip()
                if as_int:
                    return int(''.join(filter(str.isdigit, text))) if text else 0
                else:
                    return text
            else:
                print(f"Ogohlantirish: {xpath} uchun element topilmadi")
                return 0 if as_int else ""
        except ValueError:
            print(f"Ogohlantirish: {xpath} uchun element matni integerga aylantirib bo'lmadi")
            return 0
        except Exception as e:
            print(f"Xatolik yuz berdi: {str(e)}")
            self.take_screenshot("get_element_value_error")
            return 0 if as_int else ""

    def elements_equal(self, xpath1, xpath2, as_int=False):
        """
        Ikki elementning qiymatlarini solishtiradi va ularning tengligini tekshiradi.
        :param xpath1: birinchi elementning XPath'i
        :param xpath2: ikkinchi elementning XPath'i
        :param as_int: True bo'lsa, qiymatlarni integer sifatida solishtiradi
        :return: True agar qiymatlar teng bo'lsa, aks holda False
        """
        try:
            value1 = self.get_element_value(xpath1, as_int)
            value2 = self.get_element_value(xpath2, as_int)

            is_equal = value1 == value2
            result = "teng" if is_equal else "teng emas"

            print(f"Qiymat 1 ({xpath1}): {value1}")
            print(f"Qiymat 2 ({xpath2}): {value2}")
            print(f"Natija: Qiymatlar {result}")

            return is_equal
        except Exception as e:
            print(f"Qiymatlarni solishtirishda xatolik yuz berdi: {str(e)}")
            self.take_screenshot("compare_elements_error")
            return False
