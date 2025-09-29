from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class LicenseList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    # balance
    # ------------------------------------------------------------------------------------------------------------------
    # header = (By.XPATH, '(//div[@class="card-header"]//div[@class="card-title"]//t[contains(text(),"Баланс")])[1]')

    def element_visible(self):
        self.assertions.assert_url_contains(expected_url_part="/biruni/kl/license_list")
    # ------------------------------------------------------------------------------------------------------------------

    def click_navbar_button(self, navbar_name):
        locator = (By.XPATH, f'//div[contains(@class,"navi-item")]//span/t[contains(text(),"{navbar_name}")]')
        self.click(locator)
    # ------------------------------------------------------------------------------------------------------------------

    def get_payer_balance(self, payer_name):
        locator = (By.XPATH, f'//b-pg-grid[@name="balances"]//div[contains(text(),"{payer_name}")]/..//p[@ng-class="getBalanceClass(item.balance)"]')
        get_payer_balance = self.get_numeric_value(locator)
        self.logger.info(f"get_payer_balance: {get_payer_balance}")
        return get_payer_balance
    # ------------------------------------------------------------------------------------------------------------------
    # licence and document
    # ------------------------------------------------------------------------------------------------------------------
    header_licence = (By.XPATH, '//div[@class="card-title"]//t[contains(text(),"Лицензии и документы")]')

    def licence_and_document_visible(self):
        self.assertions.assert_element_visible(self.header_licence, message="License: License and Purchase page")
    # ------------------------------------------------------------------------------------------------------------------

    def click_tbl_row_button(self, element_name, data):
        locator = f"//div[contains(@class, 'tbl-row')]//div[contains(@class, 'tbl-cell') and contains(.,'{element_name}')]/..//div[text()='{data}']"
        self.find_row_and_click(element_name, xpath_pattern=locator)
    # ------------------------------------------------------------------------------------------------------------------

    def click_attach_users_button(self, element_name, data):
        locator = (By.XPATH, f"//div[contains(@class, 'tbl-row')]//div[contains(@class, 'tbl-cell') and contains(.,'{element_name}')]/..//div[text()='{data}']/..//button")
        self.click(locator)
    # ------------------------------------------------------------------------------------------------------------------
    # purchase
    # ------------------------------------------------------------------------------------------------------------------
    buy_button = (By.XPATH, '//button[@ng-click="openPurchaseModal(\'Y\')"]')

    def visible_buy_button(self):
        self.assertions.assert_element_visible(self.buy_button, message="License: Purchase page")
    # ------------------------------------------------------------------------------------------------------------------
    payers_input = (By.XPATH, '//b-input[@name="payers"]//input')
    options_payer = (By.XPATH, '//b-input[@name="payers"]//div[contains(@class,"form-row")]')

    def input_payers(self, payer_name):
        self.click_options(self.payers_input, self.options_payer, payer_name)
    # ------------------------------------------------------------------------------------------------------------------
    contract_input = (By.XPATH, '//b-input[@name="contract"]//input')
    options_contract = (By.XPATH, '//b-input[@name="contract"]//div[contains(@class,"form-row")]/div')

    def input_contract(self, contract_name):
        self.click_options(self.contract_input, self.options_contract, contract_name)
    # ------------------------------------------------------------------------------------------------------------------
    begin_date_input = (By.XPATH, '//input[@ng-model="purchase.begin_date"]')

    def input_begin_date(self, begin_date):
        self.input_text(self.begin_date_input, begin_date)
    # ------------------------------------------------------------------------------------------------------------------
    end_date_input = (By.XPATH, '//input[@ng-model="purchase.end_date"]')

    def input_end_date(self, end_date):
        self.input_text(self.end_date_input, end_date)
    # ------------------------------------------------------------------------------------------------------------------
    license_count_input = (By.XPATH, '//tr/td[text()="Подключение к системе (5x)"]/../td/input[@ng-model="license.count"]')

    def input_license_count(self, license_count):
        self.input_text(self.license_count_input, license_count)
    # ------------------------------------------------------------------------------------------------------------------
    purchase_balance = (By.XPATH, '//form[@name="purchase_form"]//t[@p1="byCurrency(purchase.balance)"]')

    def get_purchase_balance(self):
        get_purchase_balance = self.get_numeric_value(self.purchase_balance)
        self.logger.info(f"get_purchase_balance: {get_purchase_balance}")
        return get_purchase_balance
    # ------------------------------------------------------------------------------------------------------------------
    purchase_total_amount = (By.XPATH, '//form[@name="purchase_form"]//t[@p1="byCurrency(purchase.total_amount)"]')

    def get_purchase_total_amount(self):
        get_purchase_total_amount = self.get_numeric_value(self.purchase_total_amount)
        self.logger.info(f"get_purchase_balance: {get_purchase_total_amount}")
        return get_purchase_total_amount
    # ------------------------------------------------------------------------------------------------------------------

    def click_buy_button(self):
        self.click(self.buy_button)
    # ------------------------------------------------------------------------------------------------------------------
    # purchase -> modal
    # ------------------------------------------------------------------------------------------------------------------
    modal_content = (By.XPATH, '//div[@class="modal-content"]//h6[@class="modal-title"]')

    def get_modal_content(self):
        self.assertions.assert_element_visible(self.modal_content, message="License: Purchase -> Modal title")
    # ------------------------------------------------------------------------------------------------------------------
    purchase_check_checkbox = (By.XPATH, '//div[@id="purchaseModal"]//input[@ng-model="q.purchase_check"]/../span')

    def click_purchase_check(self):
        self.click(self.purchase_check_checkbox)
    # ------------------------------------------------------------------------------------------------------------------
    save_purchase_button = (By.XPATH, '//button[@ng-click="savePurchase(\'Y\')"]')

    def click_save_purchase_button(self):
        self.click(self.save_purchase_button)
    # ------------------------------------------------------------------------------------------------------------------
