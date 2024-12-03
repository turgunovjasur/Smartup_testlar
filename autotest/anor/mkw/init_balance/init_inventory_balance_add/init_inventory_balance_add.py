from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class InitInventoryBalanceAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    balance_number_input = (By.XPATH, '//form[@name="form"]//input[@ng-model="d.balance_number"]')

    def input_balance_number(self, balance_number):
        self.input_text(self.balance_number_input, balance_number)
    # ------------------------------------------------------------------------------------------------------------------
    warehouse_name_input = (By.XPATH, '//b-input[@name="warehouses"]//input[@ng-model="d.warehouse_name"]')
    warehouse_elem = (By.XPATH, '//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_warehouse_name(self, warehouse_name):
        self.click_options(self.warehouse_name_input, self.warehouse_elem, warehouse_name)
    # ------------------------------------------------------------------------------------------------------------------
    product_name_input = (By.XPATH, '//b-input[@name="products"]//input[@ng-model="item.product_name"]')
    product_elem = (By.XPATH, '//b-input[@model="item.product_name"]//div[@class="hint-body ng-scope"]/div[1]')

    def input_product_name(self, product_name):
        self.click_options(self.product_name_input, self.product_elem, product_name)
    # ------------------------------------------------------------------------------------------------------------------
    card_code_input = (By.XPATH, '(//input[@ng-model="item.card_code"])[1]')

    def input_card_code(self, product_card_code):
        self.input_text(self.card_code_input, product_card_code)
    # ------------------------------------------------------------------------------------------------------------------
    quantity_input = (By.XPATH, '(//input[@ng-model="item.quantity"])[1]')

    def input_quantity(self, product_quantity):
        self.input_text(self.quantity_input, product_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    price_input = (By.XPATH, '(//input[@ng-model="item.price"])[1]')

    def input_price(self, product_price):
        self.input_text(self.price_input, product_price)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-if="fi.save"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    reload_button = (By.XPATH, '//button[@ng-click="reload()"]')

    def click_reload_button(self):
        self.click(self.reload_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, balance_number):
        return self.find_row_and_click(element_name=balance_number)
    # ------------------------------------------------------------------------------------------------------------------
    post_one_button = (By.XPATH, '//button[@ng-click="postOne(row)"]')
    yes_post_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_post_one_button(self):
        self.click(self.post_one_button)
        self.click(self.yes_post_button)
    # ------------------------------------------------------------------------------------------------------------------
