from pages.core.md.base_page import BasePage
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
    options_currency_name = (By.XPATH, '//form[@name="form"]//b-input[@name="currencies"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div[2]')

    def input_currency_name(self, currency_name):
        self.click_options(self.currency_name_input, self.options_currency_name, currency_name)
    # ------------------------------------------------------------------------------------------------------------------
    initial_amount_input = (By.XPATH, '//form[@name="form"]//input[@ng-model="d.initial_amount"]')

    def input_initial_amount(self, initial_amount):
        self.input_text(self.initial_amount_input, initial_amount)
    # ------------------------------------------------------------------------------------------------------------------
    sub_filial_input = (By.XPATH, '//b-input[@name="subfilials"]//input')
    options_sub_filial = (By.XPATH, '//b-input[@name="subfilials"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_sub_filial(self, sub_filial_name):
        self.click_options(self.sub_filial_input, self.options_sub_filial, sub_filial_name)
    # ------------------------------------------------------------------------------------------------------------------
    is_main_checkbox = (By.XPATH, '//input[@ng-model="d.is_main"]')

    def click_is_main_checkbox(self, state):
        self.click_checkbox(self.is_main_checkbox, state=state)
    # ------------------------------------------------------------------------------------------------------------------
    allow_auto_consignment_checkbox = (By.XPATH, '//input[@ng-model="d.allow_auto_consignment"]/following-sibling::span')

    def click_allow_auto_consignment_checkbox(self):
        self.click(self.allow_auto_consignment_checkbox)
    # ------------------------------------------------------------------------------------------------------------------
    check_status_checkbox = (By.XPATH, '//input[@ng-model="d.state"]/following-sibling::span')

    def click_check_status_checkbox(self):
        self.click(self.check_status_checkbox)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
