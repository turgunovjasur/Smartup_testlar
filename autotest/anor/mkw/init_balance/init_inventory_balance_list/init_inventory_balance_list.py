from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class InitInventoryBalanceList(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="add()"]')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
