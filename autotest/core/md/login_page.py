import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from autotest.core.md.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def fill_registration_form(self, email, password, login_xpath, password_xpath):
        self.input_text((By.XPATH, login_xpath), email)
        self.input_text((By.XPATH, password_xpath), password)

    def click_sign_up_button(self, signup_xpath):
        self.click_element((By.XPATH, signup_xpath))

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
        self.fill_registration_form(email, password, login_xpath, password_xpath)
        self.click_sign_up_button(signup_xpath)
        time.sleep(5)

    def is_dashboard_visible(self, dashboard_header_xpath):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, dashboard_header_xpath))
            )
            return True
        except TimeoutException:
            print("Sahifa topilmadi")
            self.take_screenshot("Page_not_found")
            return False

    def take_error_screenshot(self):
        self.take_screenshot(f"login_error_{int(time.time())}")
