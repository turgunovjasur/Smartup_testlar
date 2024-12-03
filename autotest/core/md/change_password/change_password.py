from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class ChangePassword(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//div[@class="alert-icon"]/i')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    current_password_input = (By.XPATH, '//input[@id="current_password"]')

    def input_current_password(self, current_password):
        self.input_text(self.current_password_input, current_password)
    # ------------------------------------------------------------------------------------------------------------------
    new_password_input = (By.XPATH, '//input[@id="new_password"]')

    def input_new_password(self, new_password):
        self.input_text(self.new_password_input, new_password)
    # ------------------------------------------------------------------------------------------------------------------
    rewritten_password_input = (By.XPATH, '//input[@id="rewritten_password"]')

    def input_rewritten_password(self, rewritten_password):
        self.input_text(self.rewritten_password_input, rewritten_password)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
