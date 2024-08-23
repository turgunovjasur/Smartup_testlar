from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class FinishPage(BasePage):
    ##############################################################################
    finish_page_header = "//div[@id='anor113-wizard_wrapper-main']"

    def element_visible(self, finish_page_header):
        self.wait_for_element_visible((By.XPATH, finish_page_header))

    ##############################################################################
    status_input = "//div[@id='anor113-ui_select-status_name']/div/div/span"
    status = "(//div[@id='anor113-ui_select-status_name']//div[@class='ui-select-choices-row ng-scope']/span)[1]"

    def fill_form(self, status_input, status):
        self.input_text_elem((By.XPATH, status_input), (By.XPATH, status))

    ##############################################################################
    next_button = "//button[@id='anor113-button-finish-nextstep']"
    save_button = "//div[@class='modal-footer']/button[contains(text(), 'да')]"

    def click_button(self, next_button, save_button):
        self.click((By.XPATH, next_button))
        self.click((By.XPATH, save_button))

    ##############################################################################