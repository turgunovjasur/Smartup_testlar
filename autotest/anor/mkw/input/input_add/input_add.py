from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class InputAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//div[@id="anor113-wizard_wrapper-main"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    input_number_input = (By.XPATH, '//div[@id="anor113-input-text-input_number"]//input')

    def input_number(self, input_number):
        self.input_text(self.input_number_input, input_number)
    # ------------------------------------------------------------------------------------------------------------------
    warehouses_input = (By.XPATH, '//b-input[@name="warehouses"]//input')
    options_warehouses = (By.XPATH, '//b-input[@name="warehouses"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_warehouse(self, warehouse_name):
        self.click_options(self.warehouses_input, self.options_warehouses, warehouse_name)
    # ------------------------------------------------------------------------------------------------------------------
    extra_cost_checkbox = (By.XPATH, '//div[@id="anor113-input-checkbox-extra_cost_enabled"]//span')

    def click_extra_cost_checkbox(self):
        self.click(self.extra_cost_checkbox)
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = (By.XPATH, '//button[@id="anor113-button-finish-nextstep"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_next_step(self, save=False):
        self.click(self.next_step_button)
        if save:
            self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    purchases_input = (By.XPATH, '//div[@id="anor113-input-b_input-purchases"]//input')
    options_purchases = (By.XPATH, '//div[@id="anor113-input-b_input-purchases"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div[position()=1]')

    def input_purchase(self, purchase_number):
        self.click_options(self.purchases_input, self.options_purchases, purchase_number)
    # ------------------------------------------------------------------------------------------------------------------
    quantity_input = (By.XPATH, '//b-pg-grid[@name="purchase_items_0"]//input[@ng-model="row.quantity"]')

    def input_quantity(self, purchase_quantity):
        self.input_text(self.quantity_input, purchase_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    extra_costs_input = (By.XPATH, '//b-input[@name="extra_costs"]//input')
    add_button = (By.XPATH, '//b-input[@name="extra_costs"]//a[@ng-click="_$bInput.onAddClick()"]')

    def input_extra_cost(self):
        self.click(self.extra_costs_input)
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    distribute_extra_cost_button = (By.XPATH, '//button[@id="anor113-button-distribute_extra_costs"]')

    def click_distribute_extra_cost_button(self):
        self.click(self.distribute_extra_cost_button)
    # ------------------------------------------------------------------------------------------------------------------
