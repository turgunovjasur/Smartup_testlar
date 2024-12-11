from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class OffsetDetailList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, client_name):
        self.find_row_and_click(element_name=client_name)
    # ------------------------------------------------------------------------------------------------------------------
    offset_button = (By.XPATH, '//button[@ng-click="offsetOne(row)"]')

    def click_offset_button(self):
        self.click(self.offset_button)
    # ------------------------------------------------------------------------------------------------------------------
    payment_button = (By.XPATH, '//button[@ng-click="paymentOne(row)"]')

    def click_payment_button(self):
        self.click(self.payment_button)
    # ------------------------------------------------------------------------------------------------------------------
