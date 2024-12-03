from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class RobotAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="save()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, '//input[@ng-model="d.name"]')

    def input_name(self, name):
        self.input_text(self.name_input, name)
    # ------------------------------------------------------------------------------------------------------------------
    role_input = (By.XPATH, '//b-input[@name="roles"]//div[@class="input"]//input')
    role_options = (By.XPATH, '//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_roles(self, role_name):
        self.click_options(self.role_input, self.role_options, role_name, scroll_enabled=True)
    # ------------------------------------------------------------------------------------------------------------------
    person_input = (By.XPATH, '//b-input[@name="persons"]//input')
    person_options = (By.XPATH, '//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_persons(self, natural_person_name):
        self.click_options(self.person_input, self.person_options, natural_person_name)
    # ------------------------------------------------------------------------------------------------------------------
    room_input = (By.XPATH, '//b-input[@name="rooms"]//input')
    room_options = (By.XPATH, '//b-input[@name="rooms"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_rooms(self, room_name):
        self.click_options(self.room_input, self.room_options, room_name)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
