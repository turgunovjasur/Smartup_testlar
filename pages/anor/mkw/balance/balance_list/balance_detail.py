from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class BalanceDetail(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, product_name, warehouse_name):
        self.find_row_and_click(element_name=product_name,
                                xpath_pattern=f'//b-grid[@name="table_detail"]//div[contains(.,"{warehouse_name}") and @class="tbl-cell"]/../div[contains(.,"{product_name}")]')
    # ------------------------------------------------------------------------------------------------------------------
    reload_button = (By.XPATH, '//button[@ng-click="reload()"]')

    def click_reload_button(self):
        self.click(self.reload_button)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
