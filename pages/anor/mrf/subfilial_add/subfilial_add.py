from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class SubFilialAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = By.XPATH, '//button[@ng-click="save()"]'

    def element_visible(self):
        return self.wait_for_element_visible(self.header)

    # ------------------------------------------------------------------------------------------------------------------
    name_input = By.XPATH, '//div[@class="card-body"]//input[@ng-model="d.name"]'

    def input_name(self, sub_filial_name):
        self.input_text(self.name_input, sub_filial_name)

    # ------------------------------------------------------------------------------------------------------------------
    rooms_input = By.XPATH, '//b-input[@name="rooms"]//input'
    options_locator = (By.XPATH, '//b-input[@name="rooms"]//div[contains(@class,"hint-body")]//div[contains(@class,"form-row")]')

    def input_rooms(self, room_name):
        self.click_options(self.rooms_input, self.options_locator, room_name)

    # ------------------------------------------------------------------------------------------------------------------
    save_button = By.XPATH, '//button[@ng-click="save()"]'

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
