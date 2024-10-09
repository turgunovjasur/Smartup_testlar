from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class FinishPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    finish_page_header = "//div[@id='anor133-wizard_step-main']"

    def element_visible(self, finish_page_header):
        self.wait_for_element_visible((By.XPATH, finish_page_header))
    # ------------------------------------------------------------------------------------------------------------------
    status_input = "//div[@id='anor133-uiselect-status']//span"
    status_elem = "//div[@id='anor133-uiselect-status']//div//span[contains(text(), 'Черновик')]"
    text_area_input = "//div[@id='anor133-input-textarea-note']/textarea"

    def fill_form(self, status_input, status_elem,
                  text_area_input, text_area_text):
        self.input_text_elem((By.XPATH, status_input), (By.XPATH, status_elem))
        self.input_text((By.XPATH, text_area_input), text_area_text)
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = "//button[@id='anor133-button-finish']"
    yes_button = "//div/button[contains(text(), 'да')]"

    def click_button(self, next_step_button, yes_button):
        self.click((By.XPATH, next_step_button))
        self.click((By.XPATH, yes_button))
    # ------------------------------------------------------------------------------------------------------------------
