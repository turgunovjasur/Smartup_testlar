from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class WriteOffList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="add()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="add()"]')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, '//button[@ng-click="view(row)"]')

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    expense_button = (By.XPATH, '//button[@ng-click="expense(row)"]')

    def click_expense_button(self):
        self.click(self.expense_button)
    # ------------------------------------------------------------------------------------------------------------------
    transaction_button = (By.XPATH, '//button[@ng-click="transactions(row)"]')

    def click_transaction_button(self):
        self.click(self.transaction_button)

    def check_transaction_body(self, timeout):
        report_body = (By.XPATH, '//div[@id="report-content"]')
        self.wait_for_element(report_body, timeout=timeout, wait_type='visibility', screenshot='write_off_transaction_not_open')
    # ------------------------------------------------------------------------------------------------------------------
    dropdown = (By.XPATH, '//b-grid//button[@data-toggle="dropdown"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_change_status_button(self, status_name):
        self.click(self.dropdown)
        locator = (By.XPATH, f'//b-grid//button[@data-toggle="dropdown"]/following-sibling::div[contains(.,"{status_name}")]')
        self.click(locator)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, write_off_number):
        self.find_row_and_click(element_name=write_off_number)
    # ------------------------------------------------------------------------------------------------------------------
