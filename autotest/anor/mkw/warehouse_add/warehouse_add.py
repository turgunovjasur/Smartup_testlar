from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.exception import ElementNotFoundError


class WarehouseAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//b-page[@class="ng-scope"]//button[@ng-click="save()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    warehouse_input = (By.XPATH, '//input[@ng-model="d.name"]')

    def input_warehouse(self, warehouse_name):
        self.input_text(self.warehouse_input, warehouse_name)
    # ------------------------------------------------------------------------------------------------------------------
    warehouse_types_input = (By.XPATH, '//b-input[@name="warehouse_types"]//input')
    add_warehouse_type_button = (By.XPATH, '//b-input[@name="warehouse_types"]//a[@ng-click="_$bInput.onAddClick()"]')
    options_warehouse_type = (By.XPATH, '//b-input[@name="warehouse_types"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_warehouse_type(self, warehouse_type_name):
        try:
            self.click_options(self.warehouse_types_input, self.options_warehouse_type, warehouse_type_name, screenshot=False)
            return True
        except ElementNotFoundError:
            self.click(self.add_warehouse_type_button)
            return False
    # ------------------------------------------------------------------------------------------------------------------
    room_input = (By.XPATH, '//b-input[@name="rooms"]//input')
    options_room = (By.XPATH, '//b-input[@name="rooms"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_room(self, room_name):
        self.click_options(self.room_input, self.options_room, room_name)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//b-page[@class="ng-scope"]//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------