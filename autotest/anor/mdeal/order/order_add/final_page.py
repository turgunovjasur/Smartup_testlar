from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

from autotest.core.md.base_page import BasePage


class FinalPage(BasePage):
    def fill_form(self, payment_type, status, payment_type_input_xpath, payment_elem_xpath, status_input_xpath, status_elem_xpath):
        self.new_input((By.XPATH, payment_type_input_xpath), payment_type, (By.XPATH, payment_elem_xpath))
        try:
            self.choice((By.XPATH, status_input_xpath), (By.XPATH, status_elem_xpath))
        except TimeoutException:
            print("An error occurred while selecting status")
            self.take_screenshot("status_selection_error")

    def click_save_button(self, save_button_xpath, yes_button_xpath):
        self.click_element((By.XPATH, save_button_xpath))
        self.click_element((By.XPATH, yes_button_xpath))


