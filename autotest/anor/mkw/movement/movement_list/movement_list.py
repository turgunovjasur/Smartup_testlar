from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class MovementList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//button[@id='anor132-button-add']")

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, "//button[@id='anor132-button-add']")

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, '//button[@ng-click="view(row)"]')

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    status_button = (By.XPATH, '//div[@ng-if="q.statuses.length"]/button[@data-toggle="dropdown"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_status_button(self, status):
        self.click(self.status_button)
        status_option = (By.XPATH, f'(//div[@ng-if="q.statuses.length"]/div/a)[{status}]')
        self.click(status_option)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, movement_number):
        self.find_row_and_click(element_name=movement_number)
    # ------------------------------------------------------------------------------------------------------------------