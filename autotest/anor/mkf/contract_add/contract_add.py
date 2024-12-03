from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ContractAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//input[@ng-model="d.contract_number"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    contract_number_input = (By.XPATH, '//input[@ng-model="d.contract_number"]')

    def input_contract_number(self, contract_number):
        self.input_text(self.contract_number_input, contract_number)
    # ------------------------------------------------------------------------------------------------------------------
    contract_name_input = (By.XPATH, '//form[@name="form"]//input[@ng-model="d.name"]')

    def input_contract_name(self, contract_name):
        self.click(self.contract_name_input)
        self.clear_element(self.contract_name_input)
        self.input_text(self.contract_name_input, contract_name)
    # ------------------------------------------------------------------------------------------------------------------
    radio_button = (By.XPATH, '//label[@class="radio"][2]/input[@name="person_kind"]/following-sibling::span')

    def click_radio_button(self):
        self.click(self.radio_button)
    # ------------------------------------------------------------------------------------------------------------------
    person_name_input = (By.XPATH, '//form[@name="form"]//b-input[@name="persons"]//input[@ng-model="d.person_name"]')
    options_person_name = (By.XPATH, '//form[@name="form"]//b-input[@name="persons"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_person_name(self, person_name):
        self.click_options(self.person_name_input, self.options_person_name, person_name)
    # ------------------------------------------------------------------------------------------------------------------
    currency_name_input = (By.XPATH, '//form[@name="form"]//b-input[@name="currencies"]//input')
    options_currency_name = (By.XPATH, '//form[@name="form"]//b-input[@name="currencies"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div[1]')

    def input_currency_name(self, currency_name):
        self.click_options(self.currency_name_input, self.options_currency_name, currency_name)
    # ------------------------------------------------------------------------------------------------------------------
    initial_amount_input = (By.XPATH, '//form[@name="form"]//input[@ng-model="d.initial_amount"]')

    def input_initial_amount(self, initial_amount):
        self.input_text(self.initial_amount_input, initial_amount)
    # ------------------------------------------------------------------------------------------------------------------
    checkbox_button = (By.XPATH, '(//form[@name="form"]//label[@class="switch"]/span)[1]')

    def click_checkbox_button(self):
        self.click(self.checkbox_button)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
