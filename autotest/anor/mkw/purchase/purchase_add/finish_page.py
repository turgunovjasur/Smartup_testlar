from selenium.webdriver.common.by import By

from autotest.core.md.base_page import BasePage


class FinishPage(BasePage):
    ##############################################################################
    finish_page_header_xpath = "//div/descendant::div/h3/t[contains(text(), 'Основное')]"

    def element_visible(self, finish_page_header_xpath):
        self.wait_for_element_visible((By.XPATH, finish_page_header_xpath))

    ##############################################################################
    status = "//div[@id='anor289-uiselect-status']/div/div/div/span"
    status_elem = "//li[@id='ui-select-choices-5' and @class='ui-select-choices-group']/div[4]/span"

    def fill_form(self, status, status_elem):
        self.input_text_elem((By.XPATH, status), (By.XPATH, status_elem))

    ##############################################################################
    finish_page_save_button_xpath = "//button[@id= 'anor289-button-save']"
    finish_page_yes_button_xpath = "//div[@id= 'biruniConfirm']/descendant::button[contains(text(), 'да')]"

    def click_button(self, finish_page_save_button_xpath, finish_page_yes_button_xpath):
        self.wait_and_click((By.XPATH, finish_page_save_button_xpath))
        self.wait_and_click((By.XPATH, finish_page_yes_button_xpath))
    ##############################################################################
