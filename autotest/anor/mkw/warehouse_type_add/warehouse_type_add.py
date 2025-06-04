from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class WarehouseTypeAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//b-page[@class="ng-scope"]//button[@ng-click="save()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    warehouse_type_input = (By.XPATH, '//b-page[@class="ng-scope"]//input[@ng-model="d.name"]')

    def input_warehouse_name(self, warehouse_type_name):
        self.input_text(self.warehouse_type_input, warehouse_type_name)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//b-page[@class="ng-scope"]//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------