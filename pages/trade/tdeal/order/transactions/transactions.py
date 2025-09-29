from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class Transaction(BasePage):
    # ------------------------------------------------------------------------------------------------------------------

    def check_transaction_body(self, timeout):
        report_body = (By.XPATH, '//div[@id="report-content"]')
        self.wait_for_element(report_body, timeout=timeout, wait_type='visibility', screenshot='input_report_not_open')
    # ------------------------------------------------------------------------------------------------------------------