from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By

from utils.exception import ElementInteractionError, ElementVisibilityError


class LoginPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    login_header = (By.XPATH, '//div[@class="loginbox__logo"]')

    def element_visible(self):
        try:
            self._wait_for_visibility(self.login_header)
            self.logger.info("Login Page: The 'logo' element is verified")
        except ElementVisibilityError:
            self.logger.warning("Login Page: The 'logo' element is not visible")
            pass
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    email_input = (By.XPATH, '//input[@id="login"]')
    password_input = (By.XPATH, '//input[@id="password"]')

    def fill_form(self, email, password):
        try:
            email_success = self.input_text(self.email_input, email)
            password_success = self.input_text(self.password_input, password)
            if email_success and password_success:
                self.logger.info("Login Page: Data entered successfully")
        except ElementInteractionError:
            self.logger.error(f"Login Page: Incorrect data -> email={email} or password={password}")
            raise
    # ------------------------------------------------------------------------------------------------------------------
    signup_button = (By.XPATH, '//button[@id="sign_in"]')

    def click_button(self):
        self.click(self.signup_button)
    # ------------------------------------------------------------------------------------------------------------------
    error_massage = (By.XPATH, "//span[@id='error']")

    def get_error_text(self):
        self.wait_for_element_visible(self.error_massage)
    # ------------------------------------------------------------------------------------------------------------------
    # Logout
    # ------------------------------------------------------------------------------------------------------------------
    navbar_button = (By.XPATH, '(//div[@class="topbar-item"])[5]/div/span')

    def click_navbar_button(self):
        self.click(self.navbar_button)
    # ------------------------------------------------------------------------------------------------------------------
    logout_button = (By.XPATH, '//a[@ng-click="a.logout()"]/div')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_logout_button(self):
        self.click(self.logout_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
