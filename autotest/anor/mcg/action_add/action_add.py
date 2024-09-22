from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class ActionAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = "(//h3/t[contains(text(), Главное)])[1]"

    def element_visible(self, header):
        self.wait_for_element_visible((By.XPATH, header))
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    name_input = "id('anor718-input-text-name')/input"
    name_elem = 'action_add'

    def input_name(self, name_input, name_elem):
        self.input_text((By.XPATH, name_input), name_elem)
    # ------------------------------------------------------------------------------------------------------------------
    bonus_warehouse_input = "(id('anor718-input-b_input-bonus_warehouse')//input)[2]"
    bonus_warehouse_elem = "id('anor718-input-b_input-bonus_warehouse')//div[@class='hint-body ng-scope']/div[1]"

    def input_bonus_warehouse(self, bonus_warehouse_input, bonus_warehouse_elem):
        self.input_text_elem((By.XPATH, bonus_warehouse_input), (By.XPATH, bonus_warehouse_elem))
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = "id('anor718-button-next_step')"

    def click_step_button(self, next_step_button):
        self.click((By.XPATH, next_step_button))
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    type_condition_input = "(id('anor718-ui_select-rule_kind')//span[1])[1]"
    # type_condition_elem = "(id('ui-select-choices-66')//span)[2]"
    type_condition_elem = "id('ui-select-choices-row-9-1')"

    def input_type_condition(self, type_condition_input, type_condition_elem):
        self.input_text_elem_js((By.XPATH, type_condition_input), (By.XPATH, type_condition_elem))
    # ------------------------------------------------------------------------------------------------------------------
    inventory_input = "id('rule_products')//input"
    inventory_elem = "id('rule_products')//div[@class='hint-body ng-scope']/div[1]"

    def input_inventory(self, inventory_input, inventory_elem):
        self.input_text_elem((By.XPATH, inventory_input), (By.XPATH, inventory_elem))
    # ------------------------------------------------------------------------------------------------------------------
    inventory_quantity_input = "id('anor718-input-text-main_value')/input"
    inventory_quantity_elem = '10'

    def input_inventory_quantity(self, inventory_quantity_input, inventory_quantity_elem):
        self.input_text((By.XPATH, inventory_quantity_input), inventory_quantity_elem)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    bonus_inventory_input = "(id('bonus_products')//input)[1]"
    bonus_inventory_elem = "id('bonus_products')//div[@class='hint-body ng-scope']/div[1]"

    def input_bonus_inventory(self, bonus_inventory_input, bonus_inventory_elem):
        self.input_text_elem((By.XPATH, bonus_inventory_input), (By.XPATH, bonus_inventory_elem))
    # ------------------------------------------------------------------------------------------------------------------
    bonus_inventory_quantity_input = "id('anor718-input-text-product_value')/input"
    bonus_inventory_quantity_elem = '1'

    def input_bonus_inventory_quantity(self, bonus_inventory_quantity_input, bonus_inventory_quantity_elem):
        self.input_text((By.XPATH, bonus_inventory_quantity_input), bonus_inventory_quantity_elem)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    save_button = "id('anor718-button-next_step')"
    yes_button = "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_save_button(self, save_button, yes_button):
        self.click((By.XPATH, save_button))
        self.click((By.XPATH, yes_button))
    # ------------------------------------------------------------------------------------------------------------------
