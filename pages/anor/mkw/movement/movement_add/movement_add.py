from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class MovementAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//div[@id="anor133-wizard_step-main"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    movement_number_input = (By.XPATH, '//div[@id="anor133-input-text-movement_number"]//input')

    def input_movement_number(self, movement_number):
        self.input_text(self.movement_number_input, movement_number)
    # ------------------------------------------------------------------------------------------------------------------
    from_warehouses_input = (By.XPATH, '//div[@id="anor133-input-b_input-from_warehouses"]//input')
    options_from_warehouse = (By.XPATH, '//div[@id="anor133-input-b_input-from_warehouses"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_from_warehouses(self, from_warehouses):
        self.click_options(self.from_warehouses_input, self.options_from_warehouse, from_warehouses)
    # ------------------------------------------------------------------------------------------------------------------
    to_warehouses_input = (By.XPATH, '//div[@id="anor133-input-b_input-to_warehouses_name"]//input')
    options_to_warehouse = (By.XPATH, '//div[@id="anor133-input-b_input-to_warehouses_name"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_to_warehouses(self, to_warehouses):
        self.click_options(self.to_warehouses_input, self.options_to_warehouse, to_warehouses)
    # ------------------------------------------------------------------------------------------------------------------
    product_input = (By.XPATH, '//b-input[@id="anor133-input-b_input-fast_search_query-0"]//input')
    options_product = (By.XPATH, '(//b-input[@id="anor133-input-b_input-fast_search_query-0"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div)[2]')

    def input_product(self, product_name):
        self.click_options(self.product_input, self.options_product, product_name)
    # ------------------------------------------------------------------------------------------------------------------
    quantity_input = (By.XPATH, '//input[@id="anor133-input-text-quantity-0"]')

    def input_quantity(self, product_quantity):
        self.input_text(self.quantity_input, product_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = (By.XPATH, '//button[@id="anor133-button-finish"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_next_step_button(self, save=False):
        self.click(self.next_step_button)
        if save:
            self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------