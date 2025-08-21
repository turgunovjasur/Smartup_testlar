from autotest.core.md.base_page import BasePage
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
    # licence and document
    # ------------------------------------------------------------------------------------------------------------------
    header_licence = (By.XPATH, '//div[@class="card-title"]//t[contains(text(),"Лицензии и документы")]')

    def licence_and_document_visible(self):
        self.wait_for_element_visible(self.header_licence)
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
        self.assertions.assert_element_visible(self.buy_button)
    # ------------------------------------------------------------------------------------------------------------------
    payers_input = (By.XPATH, '//b-input[@name="payers"]//input')
    options_payer = (By.XPATH, '//b-input[@name="payers"]//div[contains(@class,"form-row")]')

    def input_payers(self, payer_name):
        self.click_options(self.buy_button, self.options_payer, payer_name)
    # ------------------------------------------------------------------------------------------------------------------
    contract_input = (By.XPATH, '//b-input[@name="contract"]//input')
    options_contract = (By.XPATH, '//b-input[@name="contract"]//div[contains(@class,"form-row")]')

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
