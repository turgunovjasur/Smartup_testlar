from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ReturnAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//div[@ng-click="goToStep(0)"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    purchases_input = (By.XPATH, '//b-input[@name="purchases"]//input')
    options_purchase = (By.XPATH, '//b-input[@name="purchases"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div[1]')

    def input_purchases(self, purchase_number):
        self.click_options(self.purchases_input, self.options_purchase, purchase_number)
    # ------------------------------------------------------------------------------------------------------------------
    return_number_input = (By.XPATH, '//input[@ng-model="d.return_number"]')

    def input_return_number(self, return_number):
        self.input_text(self.return_number_input, return_number)
    # ------------------------------------------------------------------------------------------------------------------
    warehouses_input = (By.XPATH, '//b-input[@name="warehouses"]//input')
    options_warehouse = (By.XPATH, '//b-input[@name="warehouses"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_warehouses(self, warehouse_name):
        self.click_options(self.warehouses_input, self.options_warehouse, warehouse_name)
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = (By.XPATH, '//button[@ng-click="nextStep()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_next_step_button(self, save=False):
        self.click(self.next_step_button)
        if save:
            self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------

    def get_input_value(self, input_name):
        locator = (By.XPATH, f'//label/t[contains(text(),"{input_name}")]/../../span')
        return self.get_text(locator)
    # ------------------------------------------------------------------------------------------------------------------
    search_input = (By.XPATH, '//b-input[@name="fast_search_query"]//input')
    options_search = (By.XPATH, '//b-input[@name="fast_search_query"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def input_product_search(self, product_name):
        self.click_options(self.search_input, self.options_search, product_name)
    # ------------------------------------------------------------------------------------------------------------------
    quantity_input = (By.XPATH, '//input[@ng-model="item.quantity"]')

    def input_product_quantity(self, product_quantity):
        self.input_text(self.quantity_input, product_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    margin_value_input = (By.XPATH, '//b-pg-grid//div[contains(@ng-model,".margin_value")]//span[@ng-click="$select.activate()"]')

    def click_percent_value_button(self, percent_value):
        self.click(self.margin_value_input)
        percent_value_button = (By.XPATH, f'//b-pg-grid//div[contains(@ng-model,".margin_value")]//div[contains(@class,"ui-select-choices-row")]/span[contains(text(),"{percent_value}")]')
        self.click(percent_value_button)
    # ------------------------------------------------------------------------------------------------------------------