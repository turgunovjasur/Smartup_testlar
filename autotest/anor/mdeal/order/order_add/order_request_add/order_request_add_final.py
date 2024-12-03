from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class OrderRequestAddFinal(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="nextStep()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    request_number_input = (By.XPATH, '//input[@ng-model="d.request_number"]')

    def input_request_number(self, request_number):
        self.input_text(self.request_number_input, request_number)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="nextStep()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
