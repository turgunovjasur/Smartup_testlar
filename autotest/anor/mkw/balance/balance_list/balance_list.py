from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class BalanceList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    balance_header = (By.XPATH, '//button[@ng-if="fi.detail"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.balance_header)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, product_name):
        self.find_row_and_click(element_name=product_name)
    # ------------------------------------------------------------------------------------------------------------------
    detail_button = (By.XPATH, '//button[@ng-click="detailOne(row)"]')

    def click_detail_button(self):
        self.click(self.detail_button)
    # ------------------------------------------------------------------------------------------------------------------
    reload_button = (By.XPATH, '//button[@ng-click="reload()"]')

    def click_reload_button(self):
        self.click(self.reload_button)
    # ------------------------------------------------------------------------------------------------------------------
    get_balance_quantity = (By.XPATH, '//div[contains(@class, "tbl-row")]/div[@class="tbl-cell"][10]')

    def check_balance_quantity(self):
        return self.get_numeric_value(self.get_balance_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    count_number = (By.XPATH, "//div[@class='tbl-body']/div[@class='tbl-row'][3]/div[9]")

    def check_balance(self):
        return self.get_numeric_value(self.count_number)
    # ------------------------------------------------------------------------------------------------------------------

    def get_balance(self, warehouse_name, product_name):
        locator = (By.XPATH, f'//b-grid[@name="table"]//div[contains(.,"{warehouse_name}") and @class="tbl-cell"]/../div[contains(.,"{product_name}")]/../div/div')
        return self.get_numeric_value(locator)
    # ------------------------------------------------------------------------------------------------------------------
