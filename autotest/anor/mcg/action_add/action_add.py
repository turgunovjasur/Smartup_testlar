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
    product_input = (By.XPATH, '//b-input[@id="rule_products"]//input')
    options_product = (By.XPATH, '//b-input[@id="rule_products"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div[1]')

    def input_product_name(self, product_name):
        self.click_options(self.product_input, self.options_product, product_name)
    # ------------------------------------------------------------------------------------------------------------------
    product_quantity_input = (By.XPATH, '//form[@name="step1"]//input[@ng-model="rule.main_value"]')

    def input_product_quantity(self, product_quantity):
        self.input_text(self.product_quantity_input, product_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    bonus_product_input = (By.XPATH, '//b-input[@id="bonus_products"]//input')
    options_bonus_product = (By.XPATH, '//b-input[@id="bonus_products"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div[1]')

    def input_bonus_product(self, bonus_product_name):
        self.click_options(self.bonus_product_input, self.options_bonus_product, bonus_product_name)
    # ------------------------------------------------------------------------------------------------------------------
    bonus_product_quantity_input = (By.XPATH, '//form[@name="step1"]//input[@ng-model="product.value"]')

    def input_bonus_product_quantity(self, bonus_product_quantity):
        self.input_text(self.bonus_product_quantity_input, bonus_product_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    bonus_kind_input = (By.XPATH, '//form[@name="step1"]//div[@ng-model="bonus.bonus_kind"]//span[@ng-click="$select.activate()"]')
    bonus_kind = (By.XPATH, '//form[@name="step1"]//div[@ng-model="bonus.bonus_kind"]//ul//span[contains(text(), "Скидка")]')

    def input_bonus_kind(self):
        self.click(self.bonus_kind_input)
        self.click(self.bonus_kind)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, "id('anor718-button-next_step')")
    yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
