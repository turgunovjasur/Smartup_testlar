from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class CashinAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="save()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    cashin_number_input = (By.XPATH, '//input[@ng-model="d.cashin_number"]')

    def input_cashin_number(self, cashin_number):
        self.input_text(self.cashin_number_input, cashin_number)
    # ------------------------------------------------------------------------------------------------------------------
    clients_input = (By.XPATH, '//b-input[@name="clients"]//input[@ng-model="d.client_name"]')
    options_clients = (By.XPATH, '//b-input[@name="clients"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def input_clients(self, client_name):
        self.click_options(self.clients_input, self.options_clients, client_name)
    # ------------------------------------------------------------------------------------------------------------------
    amount_get = (By.XPATH, '//label/t[normalize-space(text())="Баланс"]/ancestor::label/following-sibling::span[@class="form-view ng-binding"]')

    def get_amount(self):
        return self.get_numeric_value(self.amount_get)
    # ------------------------------------------------------------------------------------------------------------------
    amount_input = (By.XPATH, '//input[@ng-model="d.amount"]')

    def input_amount(self, amount_cashin):
        self.input_text(self.amount_input, amount_cashin)
    # ------------------------------------------------------------------------------------------------------------------
    payment_types_input = (By.XPATH, '//b-input[@name="payment_types"]//input')
    options_payment_types = (By.XPATH, '//b-input[@name="payment_types"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_payment_types(self, payment_type):
        self.click_options(self.payment_types_input, self.options_payment_types, payment_type)
    # ------------------------------------------------------------------------------------------------------------------
    cashbox_input = (By.XPATH, '//b-input[@name="cashboxes"]//input')
    options_cashbox = (By.XPATH, '//b-input[@name="cashboxes"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_cashbox(self, cashbox_name):
        self.click_options(self.cashbox_input, self.options_cashbox, cashbox_name)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
