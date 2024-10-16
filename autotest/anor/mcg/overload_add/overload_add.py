from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class OverloadAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = By.XPATH, "(//div/h6)[1]"

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    name_input = By.XPATH, "id('anor724-input-text-name')/input"

    def input_name(self, name_elem):
        self.input_text(self.name_input, name_elem)
    # ------------------------------------------------------------------------------------------------------------------
    product_input = By.XPATH, "id('anor724-input-b_input-product_name')//input[@ng-model='d.product_name']"
    product_elem = By.XPATH, "id('anor724-input-b_input-product_name')//div[@class='hint-body ng-scope']/div[3]"

    def input_product(self):
        self.input_text_elem(self.product_input, self.product_elem)
    # ------------------------------------------------------------------------------------------------------------------
    conditions_quantity_input = By.XPATH, "id('anor724-input-text-from_value')//input"

    def input_conditions_quantity(self, conditions_quantity):
        self.input_text(self.conditions_quantity_input, conditions_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    overload_product_input = By.XPATH, "(id('anor724-input-b_pg_grid-product_name-0')//input)[1]"
    overload_product = By.XPATH, "id('anor724-input-b_pg_grid-product_name-0')//div[@class='hint-body ng-scope']/div[2]"

    def input_overload_product(self):
        self.input_text_elem(self.overload_product_input, self.overload_product)
    # ------------------------------------------------------------------------------------------------------------------
    overload_product_quantity_input = By.XPATH, "id('anor724-input-text-value-0')"

    def input_overload_product_quantity(self, overload_product_quantity):
        self.input_text(self.overload_product_quantity_input, overload_product_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = By.XPATH, "id('anor724-button-save')"
    yes_button = By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
