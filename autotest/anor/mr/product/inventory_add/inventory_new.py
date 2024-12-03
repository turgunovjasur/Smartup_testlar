from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class InventoryNew(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    inventory_new_header = (By.XPATH, "//button[@id='anor66-button-save' and contains(text(), 'Сохранить')]")

    def element_visible(self):
        return self.wait_for_element_visible(self.inventory_new_header)
    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, '//div[@id= "anor66-input-text-name"]/input')

    def input_name(self, name_elem):
        self.input_text(self.name_input, name_elem)
    # ------------------------------------------------------------------------------------------------------------------
    measurement_input = (By.XPATH, '//div[@id= "anor66-input-text-measure_short_name"]//b-input[@name="measures"]//input')
    measurement_elem = (By.XPATH, '//div[@id= "anor66-input-text-measure_short_name"]//b-input[@name="measures"]'
                                  '//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def input_measurement(self, measurement_name):
        self.click_options(self.measurement_input, self.measurement_elem, measurement_name)
    # ------------------------------------------------------------------------------------------------------------------
    goods_checkbox = (By.XPATH, "//label[@id='anor66-input-checkbox-inventory_kinds-G']")

    def click_goods_checkbox(self):
        self.click(self.goods_checkbox)
    # ------------------------------------------------------------------------------------------------------------------
    product_checkbox = (By.XPATH, "//label[@id='anor66-input-checkbox-inventory_kinds-P']")

    def click_product_checkbox(self):
        self.click(self.product_checkbox)
    # ------------------------------------------------------------------------------------------------------------------
    product_order_input = (By.XPATH, "//div[@id='anor66-input-text-order_no']/input")

    def input_order(self, product_order):
        self.input_text(self.product_order_input, product_order)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, "//button[@id='anor66-button-save']")

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
    clear_button = (By.XPATH, '//b-input[@name="sectors"]//span[@class="clear-button"]')
    sectors_input = (By.XPATH, '//b-input[@name="sectors"]//input')
    sectors_elem = (By.XPATH, '//b-input[@name="sectors"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def input_sectors(self, sector_name):
        self.click_options(self.clear_button, self.sectors_elem, sector_name)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//b-input[@name="sectors"]//div/a[@ng-click="_$bInput.onAddClick()"]')

    def input_add_sectors(self):
        self.input_text_elem(self.sectors_input, self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
