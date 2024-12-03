from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class OrderRequestAddProduct(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="nextStep()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = (By.XPATH, '//button[@ng-click="nextStep()"]')

    def click_next_step_button(self):
        self.click(self.next_step_button)
    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, '//b-input[@name="inventory_products"]//input')
    name_options = (By.XPATH, '//b-input[@name="inventory_products"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def input_name(self, product_name):
        self.click(self.name_input)
        element = self.wait_for_element_visible(self.name_options)
        element_text = element.text

        first_text = element_text.split()[0]
        assert first_text == product_name, f"Error: {first_text} != {product_name}"
        self.click(self.name_options)
    # ------------------------------------------------------------------------------------------------------------------
    quantity_input = (By.XPATH, '//div[@class="tbl-cell"]/input[@ng-model="item.requested_quant"]')

    def input_quantity(self, product_quantity):
        self.input_text(self.quantity_input, product_quantity)
    # ------------------------------------------------------------------------------------------------------------------
