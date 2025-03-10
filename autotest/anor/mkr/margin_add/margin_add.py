from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class MarginAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="save()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    name_button = (By.XPATH, '//input[@ng-model="d.name"]')

    def click_name_button(self, margin_name):
        self.input_text(self.name_button, margin_name)
    # ------------------------------------------------------------------------------------------------------------------
    percent_button = (By.XPATH, '//input[@ng-model="d.percent"]')

    def click_percent_button(self, percent_margin):
        self.input_text(self.percent_button, percent_margin)
    # ------------------------------------------------------------------------------------------------------------------

    def click_percent_type_radio_button(self, percent_type):
        radio_button = (By.XPATH, f'(//input[@type="radio" and @ng-model="d.percent_type"])[{percent_type}]/following-sibling::span')
        self.click(radio_button)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
    error_header = (By.XPATH, '//div[contains(@class,"modal-header")]//h4[contains(@class,"modal-title") and contains(text(),"Ошибка")]')

    def check_error_header(self):
        self.wait_for_element_visible(self.error_header)
    # ------------------------------------------------------------------------------------------------------------------
