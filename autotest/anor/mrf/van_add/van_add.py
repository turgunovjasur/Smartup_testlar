from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class VanAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.closet()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, '//input[@ng-model="d.name"]')

    def input_name(self, van_name):
        self.input_text(self.name_input, van_name)
    # ------------------------------------------------------------------------------------------------------------------
    carrying_input = (By.XPATH, '//input[@ng-model="d.carrying"]')

    def input_carrying(self, carrying_name):
        self.input_text(self.carrying_input, carrying_name)
    # ------------------------------------------------------------------------------------------------------------------
    van_number_input = (By.XPATH, '//input[@ng-model="d.van_number"]')

    def input_van_number(self, van_number):
        self.input_text(self.van_number_input, van_number)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
