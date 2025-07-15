from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class WriteOffAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    write_off_number_input = (By.XPATH, '//input[@ng-model="d.writeoff_number"]')

    def input_write_off_number(self, write_off_number):
        self.input_text(self.write_off_number_input, write_off_number)
    # ------------------------------------------------------------------------------------------------------------------
    def get_data_input_value(self):
        locator = (By.XPATH, f'//input[@ng-model="d.writeoff_date"]')
        return self.input_text(locator, get_value=True)
    # ------------------------------------------------------------------------------------------------------------------
    warehouses_input = (By.XPATH, '//b-input[@name="warehouses"]//input')
    options_warehouse = (By.XPATH, '//b-input[@name="warehouses"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_warehouses(self, warehouse_name):
        self.click_options(self.warehouses_input, self.options_warehouse, warehouse_name)
    # ------------------------------------------------------------------------------------------------------------------
    reasons_input = (By.XPATH, '//b-input[@name="reasons"]//input')
    options_reason = (By.XPATH, '//b-input[@name="reasons"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_reasons(self, reason_name):
        self.click_options(self.reasons_input, self.options_reason, reason_name)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    select_button = (By.XPATH, '//div[contains(@id,"inventory_kind_G")]//button[contains(.,"Подбор")]')

    def click_select_button(self):
        self.click(self.select_button)
    # ------------------------------------------------------------------------------------------------------------------
    get_product_row = (By.XPATH, '//b-pg-grid[@name="items0"]//div[@class="tbl-row ng-scope"]')

    def element_visible_product(self):
        self.wait_for_element_visible(self.get_product_row)
    # ------------------------------------------------------------------------------------------------------------------
    # Select
    # ------------------------------------------------------------------------------------------------------------------
    header_select = (By.XPATH, '//button[@ng-click="close()"]')

    def element_visible_select(self):
        self.wait_for_element_visible(self.header_select)
    # ------------------------------------------------------------------------------------------------------------------
    search_input = (By.XPATH, '//b-pg-controller[@name="items"]//input[@ng-model="g.searchValue"]')

    def input_search(self, product_name):
        self.input_text(self.search_input, product_name)
    # ------------------------------------------------------------------------------------------------------------------
    quantity_input = (By.XPATH, '//b-pg-grid[@name="items"]//input[@ng-model="row.quantity"]')

    def input_quantity(self, product_quantity):
        self.input_text(self.quantity_input, product_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    move_one_button = (By.XPATH, '//b-pg-grid[@name="items"]//button[contains(@ng-click,"moveOne")]')

    def click_move_one_button(self):
        self.click(self.move_one_button)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
