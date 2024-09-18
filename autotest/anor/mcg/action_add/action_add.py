from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class ActionAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = ""

    def element_visible(self, header):
        self.wait_for_element_visible((By.XPATH, header))
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    name_input = ''
    name_elem = 'action_add'

    def input_name(self, name_input, name_elem):
        self.input_text((By.XPATH, name_input), name_elem)
    # ------------------------------------------------------------------------------------------------------------------
    bonus_warehouse_input = ''
    bonus_warehouse_elem = ''

    def input_bonus_warehouse(self, bonus_warehouse_input, bonus_warehouse_elem):
        self.input_text_elem((By.XPATH, bonus_warehouse_input), (By.XPATH, bonus_warehouse_elem))
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = ""

    def click_step_button(self, next_step_button):
        self.click((By.XPATH, next_step_button))
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    type_condition_input = ''
    type_condition_elem = ''

    def input_type_condition(self, type_condition_input, type_condition_elem):
        self.input_text_elem((By.XPATH, type_condition_input), (By.XPATH, type_condition_elem))
    # ------------------------------------------------------------------------------------------------------------------
    inventory_input = ''
    inventory_elem = ''

    def input_inventory(self, inventory_input, inventory_elem):
        self.input_text_elem((By.XPATH, inventory_input), (By.XPATH, inventory_elem))
    # ------------------------------------------------------------------------------------------------------------------
    inventory_quantity_input = ''
    inventory_quantity_elem = ''

    def input_inventory_quantity(self, inventory_quantity_input, inventory_quantity_elem):
        self.input_text((By.XPATH, inventory_quantity_input), inventory_quantity_elem)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    bonus_inventory_input = ''
    bonus_inventory_elem = ''

    def input_bonus_inventory(self, bonus_inventory_input, bonus_inventory_elem):
        self.input_text_elem((By.XPATH, bonus_inventory_input), (By.XPATH, bonus_inventory_elem))
    # ------------------------------------------------------------------------------------------------------------------
    bonus_inventory_quantity_input = ''
    bonus_inventory_quantity_elem = ''

    def input_bonus_inventory_quantity(self, bonus_inventory_quantity_input, bonus_inventory_quantity_elem):
        self.input_text((By.XPATH, bonus_inventory_quantity_input), bonus_inventory_quantity_elem)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    save_button = ""

    def click_save_button(self, save_button):
        self.click((By.XPATH, save_button))
    # ------------------------------------------------------------------------------------------------------------------
