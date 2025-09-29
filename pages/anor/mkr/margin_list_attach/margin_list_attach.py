from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class MarginListAttach(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="add()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="add()"]')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, margin_name):
        self.find_row_and_click(element_name=margin_name)
    # ------------------------------------------------------------------------------------------------------------------
    delete_button = (By.XPATH, '//button[@ng-click="deleteOne(row)"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_delete_button(self):
        self.click(self.delete_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
