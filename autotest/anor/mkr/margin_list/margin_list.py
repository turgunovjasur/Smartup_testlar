from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class MarginList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-if="fi.open_attach"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    attach_button = (By.XPATH, '//button[@ng-if="fi.open_attach"]')

    def click_attach_button(self):
        self.click(self.attach_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, margin_name):
        self.find_row_and_click(element_name=margin_name)
    # ------------------------------------------------------------------------------------------------------------------
    attach_one_button = (By.XPATH, '//button[@ng-click="attachOne(row)"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_attach_one_button(self):
        self.click(self.attach_one_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
