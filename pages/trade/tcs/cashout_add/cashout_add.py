from selenium.webdriver.common.by import By
from pages.core.md.base_page import BasePage


class CashoutAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="savePost()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
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
    cashout_number_input = (By.XPATH, '//input[@ng-model="d.cashout_number"]')

    def input_cashout_number(self, cashout_number):
        self.input_text(self.cashout_number_input, cashout_number)
    # ------------------------------------------------------------------------------------------------------------------
    cashout_time_input = (By.XPATH, '//input[@ng-model="d.cashout_time"]')

    def get_input_cashout_time(self):
        return self.input_text(self.cashout_time_input, get_value=True)
    # ------------------------------------------------------------------------------------------------------------------
    currencies_input = (By.XPATH, '//b-input[@name="currencies"]//input')

    def get_input_currencies(self):
        return self.input_text(self.currencies_input, get_value=True)
    # ------------------------------------------------------------------------------------------------------------------
    balance_input = (By.XPATH, '//t[contains(text(),"Баланс")]/../../span[contains(@class,"form-view")]')

    def get_balance(self):
        return self.get_text(self.balance_input, clean=True)
    # ------------------------------------------------------------------------------------------------------------------
    amount_input = (By.XPATH, '//input[@ng-model="d.amount"]')

    def input_amount(self, amount):
        self.input_text(self.amount_input, amount)
    # ------------------------------------------------------------------------------------------------------------------
    suppliers_input = (By.XPATH, '//b-input[@name="suppliers"]//input')
    options_supplier = (By.XPATH, '//b-input[@name="suppliers"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_suppliers(self, supplier_name):
        self.click_options(self.suppliers_input, self.options_supplier, supplier_name)
    # ------------------------------------------------------------------------------------------------------------------
    payment_types_input = (By.XPATH, '//b-input[@name="payment_types"]//input')
    options_payment_type = (By.XPATH, '//b-input[@name="payment_types"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_payment_types(self, payment_type):
        self.click_options(self.payment_types_input, self.options_payment_type, payment_type)
    # ------------------------------------------------------------------------------------------------------------------
    cashboxes_input = (By.XPATH, '//b-input[@name="cashboxes"]//input')
    options_cashbox = (By.XPATH, '//b-input[@name="cashboxes"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_cashboxes(self, cashbox_name):
        self.click_options(self.cashboxes_input, self.options_cashbox, cashbox_name)
    # ------------------------------------------------------------------------------------------------------------------

    def check_cashout_row(self, cashout_number):
        locator = (By.XPATH, f'//b-pg-grid[@name="cashouts"]//div[contains(@class,"tbl-row")]/div[contains(text(),"{cashout_number}")]')
        self.wait_for_element_visible(locator)
    # ------------------------------------------------------------------------------------------------------------------
