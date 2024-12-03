from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class RoomAdd(BasePage):
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
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
