from selenium.webdriver.common.by import By
from pages.core.md.base_page import BasePage


class OrderSelect(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header_text = (By.XPATH, '//button[@ng-click="close()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header_text)
    # ------------------------------------------------------------------------------------------------------------------
    warehouses_input = (By.XPATH, '//b-input[@name="warehouses"]//input')
    options_warehouse = (By.XPATH, '//b-input[@name="warehouses"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def input_warehouses(self, warehouse_name):
        self.clear_element(self.warehouses_input)
        self.click_options(self.warehouses_input, self.options_warehouse, warehouse_name)
    # ------------------------------------------------------------------------------------------------------------------
    price_types_input = (By.XPATH, '//b-input[@name="price_types"]//input')
    options_price_type = (By.XPATH, '//b-input[@name="price_types"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def input_price_types(self, price_type_name):
        self.click_options(self.price_types_input, self.options_price_type, price_type_name)
    # ------------------------------------------------------------------------------------------------------------------
    quantity_input = (By.XPATH, '(//div[@id="available"]//input[@ng-model="row.quantity"])[1]')

    def input_product_quantity(self, product_quantity):
        self.input_text(self.quantity_input, product_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    collect_row_button = (By.XPATH, '(//div[@id="available"]//button[@ng-click="toCollect(row)"])[1]')

    def input_collect_row_button(self):
        self.click(self.collect_row_button)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
