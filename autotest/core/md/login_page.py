from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By

from utils.exception import ElementNotFoundError, ElementInteractionError


class LoginPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    login_header = (By.XPATH, '//div[@class="loginbox__logo"]')

    def element_visible(self):
        try:
            self._wait_for_visibility(self.login_header)
            self.logger.info("Login sahifada 'logo' elementi tasdiqlandi")
        except ElementNotFoundError:
            self.logger.warning("Login sahifada 'logo' elementi ko'rinmadi")
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    email_input = (By.XPATH, '//input[@id="login"]')
    password_input = (By.XPATH, '//input[@id="password"]')

    def fill_form(self, email, password):
        try:
            email_success = self.input_text(self.email_input, email)
            password_success = self.input_text(self.password_input, password)
            if email_success and password_success:
                self.logger.info("Login formasi muvaffaqiyatli to'ldirildi")
        except ElementInteractionError:
            self.logger.error(f"Noto'g'ri ma'lumot: email={email} yoki password={password}")
            raise
    # ------------------------------------------------------------------------------------------------------------------
    signup_button = (By.XPATH, '//button[@id="sign_in"]')

    def click_button(self):
        self.click(self.signup_button)
    # ------------------------------------------------------------------------------------------------------------------
    error_massage = (By.XPATH, "//span[@id='error']")

    def get_error_text(self, timeout=2):
        self.wait_for_element_visible(self.error_massage, timeout=timeout)
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
