from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class InventoryNew(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    inventory_new_header = "//button[@id='anor66-button-save' and contains(text(), 'Сохранить')]"

    def element_visible(self, inventory_new_header):
        self.wait_for_element_visible((By.XPATH, inventory_new_header))
    # ------------------------------------------------------------------------------------------------------------------
    name_input = '//div[@id= "anor66-input-text-name"]/input'

    def input_name(self, name_input, name_elem):
        self.input_text((By.XPATH, name_input), name_elem)
    # ------------------------------------------------------------------------------------------------------------------
    measurement_input = '//div[@id= "anor66-input-text-measure_short_name"]//div[@class="simple"]/input'
    measurement_elem = '//div[@id= "anor66-input-text-measure_short_name"]//div[@class=\'hint-body ng-scope\']/div[1]'

    def input_measurement(self, measurement_input, measurement_elem):
        self.input_text_elem((By.XPATH, measurement_input), (By.XPATH, measurement_elem))
    # ------------------------------------------------------------------------------------------------------------------
    goods_checkbox = "//label[@id='anor66-input-checkbox-inventory_kinds-G']"

    def click_goods_checkbox(self, goods_checkbox):
        self.click((By.XPATH, goods_checkbox))
    # ------------------------------------------------------------------------------------------------------------------
    product_checkbox = "//label[@id='anor66-input-checkbox-inventory_kinds-P']"

    def click_product_checkbox(self, product_checkbox):
        self.click((By.XPATH, product_checkbox))
    # ------------------------------------------------------------------------------------------------------------------
    product_order_input = "//div[@id='anor66-input-text-order_no']/input"

    def input_order(self, product_order_input, product_order):
        self.input_text((By.XPATH, product_order_input), product_order)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = "//button[@id='anor66-button-save']"

    def click_save_button(self, save_button):
        self.click((By.XPATH, save_button))
    # ------------------------------------------------------------------------------------------------------------------
