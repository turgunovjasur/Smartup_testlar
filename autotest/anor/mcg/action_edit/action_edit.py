from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ActionIdEdit(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = By.XPATH, "id('anor718-input-text-name')/input"

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    name_input = By.XPATH, "id('anor718-input-text-name')/input"

    def input_name(self, name_text):
        self.input_text(self.name_input, name_text)
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = By.XPATH, "id('anor718-button-next_step')"

    def click_step_button(self):
        self.click(self.next_step_button)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    inventory_quantity_input = By.XPATH, "id('anor718-input-text-main_value')/input"

    def input_inventory_quantity(self, inventory_quantity_elem):
        self.input_text(self.inventory_quantity_input, inventory_quantity_elem)
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
