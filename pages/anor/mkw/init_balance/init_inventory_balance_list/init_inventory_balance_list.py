from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class InitInventoryBalanceList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="add()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="add()"]')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    reload_button = (By.XPATH, '//button[@ng-click="reload()"]')

    def click_reload_button(self):
        self.click(self.reload_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, balance_number):
        self.find_row_and_click(element_name=balance_number)
    # ------------------------------------------------------------------------------------------------------------------
    post_one_button = (By.XPATH, '//button[@ng-click="postOne(row)"]')
    yes_post_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_post_one_button(self):
        self.click(self.post_one_button)
        self.click(self.yes_post_button)
    # ------------------------------------------------------------------------------------------------------------------
