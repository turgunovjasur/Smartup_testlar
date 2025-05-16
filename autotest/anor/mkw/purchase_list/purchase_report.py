from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class PurchaseReport(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    def element_visible(self):
        locator = (By.XPATH, '//td[normalize-space()="Итог"]')
        return self.wait_for_element_visible(locator)
    # ------------------------------------------------------------------------------------------------------------------
    def get_extra_cost_total_amount_for_report(self):
        locator = (By.XPATH, '//td[normalize-space()="Итог"]/following-sibling::td[1]')
        return self.get_numeric_value(locator)

    def get_extra_cost_amount_for_report(self, product_name):
        locator = (By.XPATH, f'//td[normalize-space()="{product_name}"]/following-sibling::td[7]')
        return self.get_numeric_value(locator)
    # ------------------------------------------------------------------------------------------------------------------
