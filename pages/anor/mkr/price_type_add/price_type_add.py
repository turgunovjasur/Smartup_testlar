from selenium.webdriver.common.by import By
from pages.core.md.base_page import BasePage


class PriceTypeAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//button[@id='anor183-button-save']")

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    code_input = (By.XPATH, "id('anor183-input-text-code')/input")

    def input_code(self, code):
        self.input_text(self.code_input, code)
    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, "//div[@id='anor183-input-text-name']/input")

    def input_name(self, price_type_name):
        self.input_text(self.name_input, price_type_name)
    # ------------------------------------------------------------------------------------------------------------------
    rooms_input = (By.XPATH, '//b-input[@name="rooms"]//input')
    rooms_options = (By.XPATH, '//b-input[@name="rooms"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_rooms(self, room_name):
        self.click_options(self.rooms_input, self.rooms_options, room_name)
    # ------------------------------------------------------------------------------------------------------------------
    currency_input = (By.XPATH, '//b-input[@name="currencies"]//input')
    currency_options = (By.XPATH, '//b-input[@name="currencies"]//div[contains(@class,"hint")]//div[contains(@class,"hint-item")]')

    def input_currency(self, currency_name):
        self.clear_element(self.currency_input)
        self.click_options(self.currency_input, self.currency_options, currency_name)
    # ------------------------------------------------------------------------------------------------------------------
    sub_filial_input = (By.XPATH, '//b-input[@name="subfilials"]//input')
    sub_filial_options = (By.XPATH, '//b-input[@name="subfilials"]//div[contains(@class,"hint")]//div[contains(@class,"hint-item")]')

    def input_sub_filial(self, sub_filial_name):
        self.click_options(self.sub_filial_input, self.sub_filial_options, sub_filial_name)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, "//button[@id='anor183-button-save']")

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
