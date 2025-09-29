from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ReturnList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    return_header = (By.XPATH, '//button[@ng-click="add()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.return_header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="add()"]')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, '//button[@ng-click="view(row)"]')

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    transaction_button = (By.XPATH, '//button[@ng-click="transactions(row)"]')

    def click_transaction_button(self):
        self.click(self.transaction_button)

    def check_transaction_body(self, timeout):
        report_body = (By.XPATH, '//div[@id="report-content"]')
        self.wait_for_element(report_body,
                              timeout=timeout,
                              wait_type='visibility',
                              screenshot='return_supplier_transaction_not_open')
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, return_number):
        self.find_row_and_click(element_name=return_number)
    # ------------------------------------------------------------------------------------------------------------------