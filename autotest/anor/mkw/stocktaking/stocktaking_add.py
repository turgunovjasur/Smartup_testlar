from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class StocktakingAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    stocktaking_number_input = (By.XPATH, '//input[@ng-model="d.stocktaking_number"]')

    def input_stocktaking_number(self, stocktaking_number):
        self.input_text(self.stocktaking_number_input, stocktaking_number)
    # ------------------------------------------------------------------------------------------------------------------
    def get_input_value(self, input_name):
        locator = (By.XPATH, f'//label[contains(.,"{input_name}")]/../input | '
                             f'//label[contains(.,"{input_name}")]/..//input | '
                             f'//label[contains(.,"{input_name}")]/..//textarea')
        return self.input_text(locator, get_value=True)
    # ------------------------------------------------------------------------------------------------------------------
    warehouses_input = (By.XPATH, '//b-input[@name="warehouses"]//input')
    options_warehouse = (By.XPATH, '//b-input[@name="warehouses"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_warehouses(self, warehouse_name):
        self.click_options(self.warehouses_input, self.options_warehouse, warehouse_name)
    # ------------------------------------------------------------------------------------------------------------------
    currencies_input = (By.XPATH, '//b-input[@name="currencies"]//input')

    def input_currencies(self):
        return self.input_text(self.currencies_input, get_value=True)
    # ------------------------------------------------------------------------------------------------------------------
    reasons_input = (By.XPATH, '//b-input[@name="reasons"]//input')
    options_reason = (By.XPATH, '//b-input[@name="reasons"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_reasons(self, reason_name):
        self.click_options(self.reasons_input, self.options_reason, reason_name)
    # ------------------------------------------------------------------------------------------------------------------
    note_input = (By.XPATH, '//textarea[@ng-model="d.note"]')

    def input_note(self, note_name):
        self.input_text(self.note_input, note_name)
    # ------------------------------------------------------------------------------------------------------------------
    product_input = (By.XPATH, '//b-input[@name="product"]//input')
    options_product = (By.XPATH, '//b-input[@name="product"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_product(self, product_name):
        self.click_options(self.product_input, self.options_product, product_name)
    # ------------------------------------------------------------------------------------------------------------------
    item_quant_input = (By.XPATH, '//b-pg-grid[@name="items0"]//input[@ng-model="item.new_quant"]')

    def input_item_quant(self, product_item_quant):
        self.input_text(self.item_quant_input, product_item_quant)
    # ------------------------------------------------------------------------------------------------------------------
    item_income_price_input = (By.XPATH, '//b-pg-grid[@name="items0"]//input[@ng-model="item.income_price"]')

    def input_item_income_price(self, product_item_income_price):
        self.input_text(self.item_income_price_input, product_item_income_price)
    # ------------------------------------------------------------------------------------------------------------------
    post_button = (By.XPATH, '//button[@ng-click="post()"]')
    save_button = (By.XPATH, '//button[@ng-click="save()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_save_button(self, post=False):
        if post:
            self.click(self.post_button)
        else:
            self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//b-pg-grid[@name="items0"]/..//button[contains(.,"Добавить ТМЦ")]')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    select_button = (By.XPATH, '//b-pg-grid[@name="items0"]/..//button[contains(.,"Подбор")]')

    def click_select_button(self):
        self.click(self.select_button)
    # ------------------------------------------------------------------------------------------------------------------
