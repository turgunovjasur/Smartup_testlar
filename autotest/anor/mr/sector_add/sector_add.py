from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class SectorAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//div[@class="col-sm-14"]/button[@ng-click="save()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, '//form[@name="form"]//input[@ng-model="d.name"]')

    def input_name(self, sector_name):
        self.input_text(self.name_input, sector_name)
    # ------------------------------------------------------------------------------------------------------------------
    rooms_input = (By.XPATH, '//b-input[@model="d.rooms"]//input')
    room_options = (By.XPATH, '//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_rooms(self, room_name):
        self.click_options(self.rooms_input, self.room_options, room_name)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//div[@id="kt_content"]//div[@class="col-sm-14"]//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
