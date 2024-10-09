from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class FinishPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    finish_page_header = (By.XPATH, "//div[@id='anor113-wizard_wrapper-main']")

    def element_visible(self):
        self.wait_for_element_visible(self.finish_page_header)
    # ------------------------------------------------------------------------------------------------------------------
    status_input = (By.XPATH, "//div[@id='anor113-ui_select-status_name']/div/div/span")
    status = (By.XPATH, "(//div[@id='anor113-ui_select-status_name']//div[@class='ui-select-choices-row ng-scope']/span)[1]")

    def fill_form(self):
        self.input_text_elem(self.status_input, self.status)
    # ------------------------------------------------------------------------------------------------------------------
    next_button = (By.XPATH, "//button[@id='anor113-button-finish-nextstep']")
    save_button = (By.XPATH, "//div[@class='modal-footer']/button[contains(text(), 'да')]")

    def click_button(self):
        self.click(self.next_button)
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
