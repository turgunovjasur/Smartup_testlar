from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class OverloadAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = "(//div/h6)[1]"

    def element_visible(self, header):
        self.wait_for_element_visible((By.XPATH, header))
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    name_input = "id('anor724-input-text-name')/input"
    name_elem = 'overload_add'

    def input_name(self, name_input, name_elem):
        self.input_text((By.XPATH, name_input), name_elem)
    # ------------------------------------------------------------------------------------------------------------------
    product_input = "id('anor724-input-b_input-product_name')//input[@ng-model='d.product_name']"
    product_elem = "id('anor724-input-b_input-product_name')//div[@class='hint-body ng-scope']/div[1]"

    def input_product(self, product_input, product_elem):
        self.input_text_elem((By.XPATH, product_input), (By.XPATH, product_elem))
    # ------------------------------------------------------------------------------------------------------------------
    conditions_quantity_input = "id('anor724-input-text-from_value')//input"
    conditions_quantity = '10'

    def input_conditions_quantity(self, conditions_quantity_input, conditions_quantity):
        self.input_text((By.XPATH, conditions_quantity_input), conditions_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    overload_product_input = "(id('anor724-input-b_pg_grid-product_name')//input)[1]"
    overload_product = "id('anor724-input-b_pg_grid-product_name')//div[@class='hint-body ng-scope']/div[2]"

    def input_overload_product(self, overload_product_input, overload_product):
        self.input_text_elem((By.XPATH, overload_product_input), (By.XPATH, overload_product))
    # ------------------------------------------------------------------------------------------------------------------
    overload_product_quantity_input = "id('anor724-input-text-value')"
    overload_product_quantity = '1'

    def input_overload_product_quantity(self, overload_product_quantity_input, overload_product_quantity):
        self.input_text((By.XPATH, overload_product_quantity_input), overload_product_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = "id('anor724-button-save')"
    yes_button = "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_save_button(self, save_button, yes_button):
        self.click((By.XPATH, save_button))
        self.click((By.XPATH, yes_button))
    # ------------------------------------------------------------------------------------------------------------------
