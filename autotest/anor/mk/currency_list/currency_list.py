from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class CurrencyList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = By.XPATH, '//button[@ng-click="add()"]'

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, currency_name):
        self.find_row_and_click(element_name=currency_name)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = By.XPATH, '//button[@ng-click="view(row)"]'

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
