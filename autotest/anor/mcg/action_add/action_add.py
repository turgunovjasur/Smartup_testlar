from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class ActionAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    # Page 1
    # ------------------------------------------------------------------------------------------------------------------
    header = By.XPATH, "(//h3/t[contains(text(), Главное)])[1]"

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    name_input = By.XPATH, "id('anor718-input-text-name')/input"

    def input_name(self, name_elem):
        self.input_text(self.name_input, name_elem)
    # ------------------------------------------------------------------------------------------------------------------
    end_date_input = By.XPATH, "//div[@id='anor718-input-b_input-end_date']/input"

    def input_end_date(self, end_date):
        self.input_text(self.end_date_input, end_date)
    # ------------------------------------------------------------------------------------------------------------------
    room_input = By.XPATH, "(id('anor718-input-b_input-rooms')//input)[2]"
    room_elem = By.XPATH, "id('anor718-input-b_input-rooms')//div[@class='hint-body ng-scope']/div[1]"

    def input_room(self):
        self.input_text_elem(self.room_input, self.room_elem)
    # ------------------------------------------------------------------------------------------------------------------
    bonus_warehouse_input = By.XPATH, "(id('anor718-input-b_input-bonus_warehouse')//input)[2]"
    bonus_warehouse_elem = By.XPATH, "id('anor718-input-b_input-bonus_warehouse')//div[@class='hint-body ng-scope']/div[1]"

    def input_bonus_warehouse(self):
        self.input_text_elem(self.bonus_warehouse_input, self.bonus_warehouse_elem)
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
    next_step_button = By.XPATH, "id('anor718-button-next_step')"

    def click_step_button(self):
        self.click(self.next_step_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Page 2
    # ------------------------------------------------------------------------------------------------------------------
    type_condition_input = By.XPATH, "(id('anor718-ui_select-rule_kind')//span[1])[1]"
    type_condition_elem = By.XPATH, "id('ui-select-choices-row-9-1')"

    def input_type_condition(self):
        self.input_text_elem(self.type_condition_input, self.type_condition_elem)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_input = By.XPATH, "id('rule_products')//input"
    inventory_elem = By.XPATH, "id('rule_products')//div[@class='hint-body ng-scope']/div[3]"

    def input_inventory(self):
        self.input_text_elem(self.inventory_input, self.inventory_elem)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_quantity_input = By.XPATH, "id('anor718-input-text-main_value')/input"

    def input_inventory_quantity(self, inventory_quantity_elem):
        self.input_text(self.inventory_quantity_input, inventory_quantity_elem)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    bonus_inventory_input = By.XPATH, "(id('bonus_products')//input)[1]"
    bonus_inventory_elem = By.XPATH, "id('bonus_products')//div[@class='hint-body ng-scope']/div[1]"

    def input_bonus_inventory(self):
        self.input_text_elem(self.bonus_inventory_input, self.bonus_inventory_elem)
    # ------------------------------------------------------------------------------------------------------------------
    bonus_inventory_quantity_input = By.XPATH, "id('anor718-input-text-product_value')/input"

    def input_bonus_inventory_quantity(self, bonus_inventory_quantity_elem):
        self.input_text(self.bonus_inventory_quantity_input, bonus_inventory_quantity_elem)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    save_button = By.XPATH, "id('anor718-button-next_step')"
    yes_button = By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
