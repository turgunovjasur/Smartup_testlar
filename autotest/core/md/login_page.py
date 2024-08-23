from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    ##############################################################################
    email_xpath = "//div/input[@placeholder='Логин@компания']"
    password_xpath = "//div/input[@placeholder='Пароль']"

    def fill_form(self, email, password, email_xpath, password_xpath):
        self.input_text((By.XPATH, email_xpath), email)
        self.input_text((By.XPATH, password_xpath), password)

    ##############################################################################
    signup_xpath = "//div/button[contains(text(), 'Войти')]"

    def click_button(self, signup_xpath):
        self.click((By.XPATH, signup_xpath))

    ##############################################################################