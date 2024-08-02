import time

from autotest.core.md.base_page import BasePage

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def fill_form(self, email, password, email_xpath, password_xpath):
        self.input_text((By.XPATH, email_xpath), email)
        self.input_text((By.XPATH, password_xpath), password)

    def click_button(self, signup_xpath):
        self.click((By.XPATH, signup_xpath))

    def is_error_message_displayed(self, error_message_xpath):
        return self.is_element_visible((By.XPATH, error_message_xpath))

    def is_element_visible(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def login(self, email, password, login_xpath, password_xpath, signup_xpath):
        self.fill_form(email, password, login_xpath, password_xpath)
        self.click_button(signup_xpath)
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.XPATH, signup_xpath)))

    def is_dashboard_visible(self, dashboard_header_xpath):
        try:
            return self.wait_for_element_visible((By.XPATH, dashboard_header_xpath), timeout=20)
        except TimeoutException:
            print(f"Page not found: {dashboard_header_xpath}")
            self.take_screenshot("Page_not_found")
            return False

    def take_error_screenshot(self):
        self.take_screenshot(f"login_error_{int(time.time())}")