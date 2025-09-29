from selenium.webdriver.common.by import By
from pages.core.md.base_page import BasePage


class CashoutList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="q.sc.firstFunc()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="q.sc.firstFunc()"]')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, cashout_number):
        self.find_row_and_click(element_name=cashout_number)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, '//button[@ng-click="view(row)"]')

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    post_button = (By.XPATH, '//button[@ng-click="postOne(row)"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_post_button(self):
        self.click(self.post_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    transaction_button = (By.XPATH, '//button[@ng-click="transactions(row)"]')

    def click_transaction_button(self):
        self.click(self.transaction_button)

    def check_transaction_body(self, timeout):
        report_body = (By.XPATH, '//div[@id="report-content"]')
        self.wait_for_element(report_body, timeout=timeout, wait_type='visibility',
                              screenshot='stocktaking_transaction_not_open')
    # ------------------------------------------------------------------------------------------------------------------
