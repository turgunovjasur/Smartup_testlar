from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class ActionAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    # Page 1
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "(//h3/t[contains(text(), Главное)])[1]")

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, "id('anor718-input-text-name')/input")

    def input_name(self, action_name):
        self.input_text(self.name_input, action_name)
    # ------------------------------------------------------------------------------------------------------------------
    end_date_input = (By.XPATH, "//div[@id='anor718-input-b_input-end_date']/input")

    def input_end_date(self, end_date):
        self.input_text(self.end_date_input, end_date)
    # ------------------------------------------------------------------------------------------------------------------
    room_input = (By.XPATH, '//div[@id="anor718-input-b_input-rooms"]//input')
    room_options = (By.XPATH, '//div[@id="anor718-input-b_input-rooms"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_room(self, room_name):
        self.click_options(self.room_input, self.room_options, room_name)
    # ------------------------------------------------------------------------------------------------------------------
    bonus_warehouse_input = (By.XPATH, '//div[@id="anor718-input-b_input-bonus_warehouse"]//input')
    bonus_warehouse_options = (By.XPATH, '//div[@id="anor718-input-b_input-bonus_warehouse"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_bonus_warehouse(self, warehouse_name):
        self.click_options(self.bonus_warehouse_input, self.bonus_warehouse_options, warehouse_name)
    # ------------------------------------------------------------------------------------------------------------------
    warehouses_input = (By.XPATH, '//div[@id="anor718-input-b_input-warehouses"]//input')
    warehouses_options = (By.XPATH, '//div[@id="anor718-input-b_input-warehouses"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_warehouses(self, warehouse_name):
        self.click_options(self.warehouses_input, self.warehouses_options, warehouse_name)
    # ------------------------------------------------------------------------------------------------------------------
    tip_action_input = (By.XPATH, '//div[@ng-model="d.calc_kind"]/div/span')
    tip_options = {
        'quant': (By.XPATH, '//div[@ng-model="d.calc_kind"]/ul/li/div[3]'),
        'amount': (By.XPATH, '//div[@ng-model="d.calc_kind"]/ul/li/div[4]'),
        'weight': (By.XPATH, '//div[@ng-model="d.calc_kind"]/ul/li/div[5]'),
        'box_quant': (By.XPATH, '//div[@ng-model="d.calc_kind"]/ul/li/div[6]'),
        'mixed': (By.XPATH, '//div[@ng-model="d.calc_kind"]/ul/li/div[7]')
    }

    def input_tip_action(self, tip=None):
        self.click(self.tip_action_input)
        if tip in self.tip_options:
            self.click(self.tip_options[tip])
        else:
            raise ValueError("Error tip: Only 'quant', 'amount', 'weight', 'box_quant', and 'mixed' are allowed.")
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = (By.XPATH, '//button[@id="anor718-button-next_step"]')

    def click_step_button(self):
        self.click(self.next_step_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Page 2
    # ------------------------------------------------------------------------------------------------------------------
    type_condition_input = (By.XPATH, "(id('anor718-ui_select-rule_kind')//span[1])[1]")
    type_condition_elem = (By.XPATH, "id('ui-select-choices-row-9-1')")

    def input_type_condition(self):
        self.input_text_elem(self.type_condition_input, self.type_condition_elem)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_input = (By.XPATH, '//b-input[@id="rule_products"]//input')
    options_inventory = (By.XPATH, '//b-input[@id="rule_products"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div[1]')

    def input_inventory(self, product_name):
        self.click_options(self.inventory_input, self.options_inventory, product_name)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_quantity_input = (By.XPATH, '//form[@name="step1"]//input[@ng-model="rule.main_value"]')

    def input_inventory_quantity(self, inventory_quantity):
        self.input_text(self.inventory_quantity_input, inventory_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    bonus_inventory_input = (By.XPATH, "(id('bonus_products')//input)[1]")
    bonus_inventory_elem = (By.XPATH, "id('bonus_products')//div[@class='hint-body ng-scope']/div[1]")

    def input_bonus_inventory(self):
        self.input_text_elem(self.bonus_inventory_input, self.bonus_inventory_elem)
    # ------------------------------------------------------------------------------------------------------------------
    bonus_inventory_quantity_input = (By.XPATH, "id('anor718-input-text-product_value')/input")

    def input_bonus_inventory_quantity(self, bonus_inventory_quantity_elem):
        self.input_text(self.bonus_inventory_quantity_input, bonus_inventory_quantity_elem)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, "id('anor718-button-next_step')")
    yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
