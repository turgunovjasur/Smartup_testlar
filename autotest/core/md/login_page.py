from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    login_header = (By.XPATH, '//div[@class="loginbox__logo"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.login_header)
    # ------------------------------------------------------------------------------------------------------------------
    email_input = (By.XPATH, '//input[@id="login"]')
    password_input = (By.XPATH, '//input[@id="password"]')

    def fill_form(self, email, password):
        self.input_text(self.email_input, email)
        self.input_text(self.password_input, password)
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
        self.logger.info("Login Out: closed successfully")
    # ------------------------------------------------------------------------------------------------------------------
