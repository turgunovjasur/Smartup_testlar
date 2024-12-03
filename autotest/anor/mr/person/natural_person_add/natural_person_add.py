from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class NaturalPersonAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = By.XPATH, '//button[@ng-click="save()"]'

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    name_input = By.XPATH, '//input[@ng-model="d.first_name"]'

    def input_name(self, natural_person_name):
        self.input_text(self.name_input, natural_person_name)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = By.XPATH, '//button[@ng-click="save()"]'
    yes_button = By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]'

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
