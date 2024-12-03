from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    email_input = (By.XPATH, "//div/input[@placeholder='Логин@компания']")
    password_input = (By.XPATH, "//div/input[@placeholder='Пароль']")

    def fill_form(self, email, password):
        self.input_text(self.email_input, email)
        self.input_text(self.password_input, password)
    # ------------------------------------------------------------------------------------------------------------------
    signup_button = (By.XPATH, "//div/button[contains(text(), 'Войти')]")

    def click_button(self):
        self.click(self.signup_button)
    # ------------------------------------------------------------------------------------------------------------------
