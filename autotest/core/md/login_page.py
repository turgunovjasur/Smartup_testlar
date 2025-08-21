from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    login_header = (By.XPATH, '//div[@class="loginbox__logo"]')

    def element_visible(self):
        self.wait_for_element_visible(self.login_header)
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
    error_message = (By.XPATH, "//span[@id='error']")

    def check_error_message_absence(self):
        element = self.wait_for_element(self.error_message, wait_type="presence", error_message=False)
        text = element.get_attribute("textContent").strip().replace("\xa0", "").replace("\n", "")
        if text:
            self.logger.error(f"Error text identified: '{text}'")
            self.take_screenshot(f"login_page_error_message")
            raise AssertionError("An unexpected error came out on the login page.")
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
    # unauthenticated_session_details
    # ------------------------------------------------------------------------------------------------------------------
    retry_button = (By.XPATH, '//button[@id="retry"]')

    def element_visible_retry_button(self):
        self.wait_for_element_visible(self.retry_button)
    # ------------------------------------------------------------------------------------------------------------------

    def click_retry_button(self):
        self.click(self.retry_button)
    # ------------------------------------------------------------------------------------------------------------------
    back_button = (By.XPATH, '//button[@id="retry"]/following-sibling::a[@id="back"]')

    def click_back_button(self):
        self.click(self.back_button)
    # ------------------------------------------------------------------------------------------------------------------
