from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class FinishPage(BasePage):
    ##############################################################################
    finish_page_header = "//div[@id='anor133-wizard_step-main']"

    def element_visible(self, finish_page_header):
        self.wait_for_element_visible((By.XPATH, finish_page_header))

    ##############################################################################
    status_input = "//div[@id='anor133-uiselect-status']//span"
    status_input_elem = "//div[@id='anor133-uiselect-status']//div//span[contains(text(), 'Черновик')]"

    text_area_input = "//div[@id='anor133-input-textarea-note']/textarea"
    text_area_text = "TEST"

    def fill_form(self, status_input, status_input_elem):
        self.input_text_elem((By.XPATH, status_input), (By.XPATH, status_input_elem))
        # self.input_text((By.XPATH, text_area_input), text_area_text)

    ##############################################################################
    next_button_xpath = "//button[@id='anor133-button-finish']"
    save_button_xpath = "//div/button[contains(text(), 'да')]"

    def click_button(self, next_button_xpath, save_button_xpath):
        self.click((By.XPATH, next_button_xpath))
        self.click((By.XPATH, save_button_xpath))

    ##############################################################################