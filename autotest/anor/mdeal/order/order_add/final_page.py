from selenium.webdriver.common.by import By

from autotest.core.md.base_page import BasePage


class FinalPage(BasePage):
    def fill_form(self, payment_type_input_xpath, payment_elem_xpath,
                  status_input_xpath, status_elem_xpath):
        self.input_text_elem((By.XPATH, payment_type_input_xpath), (By.XPATH, payment_elem_xpath))
        self.input_text_elem((By.XPATH, status_input_xpath), (By.XPATH, status_elem_xpath))

    def click_save_button(self, save_button_xpath, yes_button_xpath):
        self.wait_and_click((By.XPATH, save_button_xpath))
        self.wait_and_click((By.XPATH, yes_button_xpath))