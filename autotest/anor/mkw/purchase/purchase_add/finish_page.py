import random
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class FinishPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    finish_page_header = (By.XPATH, "//div/descendant::div/h3/t[contains(text(), 'Основное')]")

    def element_visible(self):
        self.wait_for_element_visible(self.finish_page_header)
    # ------------------------------------------------------------------------------------------------------------------
    status_input = (By.XPATH, "//div[@id='anor289-uiselect-status']/div/div/div/span")
    status_element = (By.XPATH, "//li[@id='ui-select-choices-5' and @class='ui-select-choices-group']/div[4]/span")

    def fill_form(self):
        self.input_text_elem(self.status_input, self.status_element)
    # ------------------------------------------------------------------------------------------------------------------
    purchase_number_input = (By.XPATH, "//div[@id='anor289-input-text-purchasenumber']/input")

    def random_number(self):
        number = random.randint(1, 9999)
        self.input_text(self.purchase_number_input, number)
        return number
    # ------------------------------------------------------------------------------------------------------------------
    finish_page_save_button = (By.XPATH, "//button[@id= 'anor289-button-save']")
    finish_page_yes_button = (By.XPATH, "//div[@id= 'biruniConfirm']/descendant::button[contains(text(), 'да')]")

    def click_button(self):
        self.click(self.finish_page_save_button)
        self.click(self.finish_page_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
