import time
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class OrderRequestList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="add()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="add()"]')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, client_name):
        self.find_row_and_click(element_name=client_name)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, '//button[@ng-click="view(row)"]')

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    status_button = (By.XPATH, '//button[@class="btn btn-default dropdown-toggle"]')
    change_status_button = (By.XPATH, '//button[@class="btn btn-default dropdown-toggle"]/following-sibling::div/a[1]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_status_button(self):
        self.click(self.status_button)
        self.click(self.change_status_button)
        self.click(self.yes_button)
        time.sleep(1)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
