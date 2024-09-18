from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ActionIdEdit(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = ""

    def element_visible(self, header):
        self.wait_for_element_visible((By.XPATH, header))
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    name_input = ""
    name_text = "action_edit"

    def input_name_edit(self, name_input, name_text):
        self.input_text((By.XPATH, name_input), name_text)
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = ""

    def click_step_button(self, next_step_button):
        self.click((By.XPATH, next_step_button))
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    inventory_quantity_input = ''
    inventory_quantity_elem = ''

    def input_inventory_quantity(self, inventory_quantity_input, inventory_quantity_elem):
        self.input_text((By.XPATH, inventory_quantity_input), inventory_quantity_elem)
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
