from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class InputList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@id="anor113-button-add"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, "//button[@id='anor113-button-add']")

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, input_number):
        self.find_row_and_click(element_name=input_number)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, '//button[@id="anor113-button-view"]')

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    change_status_button = (By.XPATH, '(//button[@id="anor113-button-edit"]/following-sibling::div/button)[1]')
    completed_button = (By.XPATH, '//button[@id="anor113-button-edit"]/following-sibling::div//a[@ng-click="completedOne(row)"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_change_status_button(self):
        self.click(self.change_status_button)
        self.click(self.completed_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    # transaction
    # ------------------------------------------------------------------------------------------------------------------
    transactions_button = (By.XPATH, '//button[@ng-click="transactions(row)"]')

    def click_transactions_button(self):
        self.click(self.transactions_button)

    def check_transaction_body(self, timeout):
        report_body = (By.XPATH, '//div[@id="report-content"]')
        self.wait_for_element(report_body, timeout=timeout, wait_type='visibility', screenshot='input_report_not_open')
    # ------------------------------------------------------------------------------------------------------------------
    # report
    # ------------------------------------------------------------------------------------------------------------------
    report_button = (By.XPATH, '//div[contains(@ng-if,"report")]/button')
    report_1 = (By.XPATH, '(//div[contains(@ng-if,"report")]//li//span)[1]')

    def click_report_button(self):
        self.click(self.report_button)
        self.click(self.report_1)

    def check_report_body(self, timeout):
        report_body = (By.XPATH, '//div[@id="report-content"]')
        self.wait_for_element(report_body, timeout=timeout, wait_type='visibility', screenshot='input_report_not_open')
    # ------------------------------------------------------------------------------------------------------------------
