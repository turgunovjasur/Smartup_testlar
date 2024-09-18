from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class OverloadAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = ""

    def element_visible(self, header):
        self.wait_for_element_visible((By.XPATH, header))
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    name_input = ''
    name_elem = 'overload_add'

    def input_name(self, name_input, name_elem):
        self.input_text((By.XPATH, name_input), name_elem)
    # ------------------------------------------------------------------------------------------------------------------
    product_input = ''
    product_elem = ''

    def input_product(self, product_input, product_elem):
        self.input_text_elem((By.XPATH, product_input), (By.XPATH, product_elem))
    # ------------------------------------------------------------------------------------------------------------------
    conditions_quantity_input = ''
    conditions_quantity = '10'

    def input_conditions_quantity(self, conditions_quantity_input, conditions_quantity):
        self.input_text((By.XPATH, conditions_quantity_input), conditions_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    overload_product_input = ''
    overload_product = ''

    def input_overload_product(self, overload_product_input, overload_product):
        self.input_text_elem((By.XPATH, overload_product_input), (By.XPATH, overload_product))
    # ------------------------------------------------------------------------------------------------------------------
    overload_product_quantity_input = ''
    overload_product_quantity = '1'

    def input_overload_product_quantity(self, overload_product_quantity_input, overload_product_quantity):
        self.input_text((By.XPATH, overload_product_quantity_input), overload_product_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = ""

    def click_save_button(self, save_button):
        self.click((By.XPATH, save_button))
    # ------------------------------------------------------------------------------------------------------------------
