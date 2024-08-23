import random
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class FinishPage(BasePage):
    ##############################################################################
    finish_page_header = "//div/descendant::div/h3/t[contains(text(), 'Основное')]"

    def element_visible(self, finish_page_header):
        self.wait_for_element_visible((By.XPATH, finish_page_header))

    ##############################################################################
    status_input = "//div[@id='anor289-uiselect-status']/div/div/div/span"
    status_element = "//li[@id='ui-select-choices-5' and @class='ui-select-choices-group']/div[4]/span"

    def fill_form(self, status_input, status_element):
        self.input_text_elem((By.XPATH, status_input), (By.XPATH, status_element))

    ##############################################################################
    purchase_number_input = "//div[@id='anor289-input-text-purchasenumber']/input"

    def random_number(self, purchase_number_input):
        number = random.randint(1, 9999)
        self.input_text((By.XPATH, purchase_number_input), number)
        return number

    ##############################################################################
    finish_page_save_button = "//button[@id= 'anor289-button-save']"
    finish_page_yes_button = "//div[@id= 'biruniConfirm']/descendant::button[contains(text(), 'да')]"

    def click_button(self, finish_page_save_button, finish_page_yes_button):
        self.click((By.XPATH, finish_page_save_button))
        self.click((By.XPATH, finish_page_yes_button))

    ##############################################################################