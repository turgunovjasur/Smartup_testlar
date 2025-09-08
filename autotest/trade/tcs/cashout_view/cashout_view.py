from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class CashoutView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="edit()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------

    def get_input_value(self, input_name, clean=False):
        locator = (By.XPATH, f'//div[contains(@ng-show,"main")]//t[contains(text(),"{input_name}")]/../../span')
        return self.get_text(locator, clean=clean)
    # ------------------------------------------------------------------------------------------------------------------

    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Audits
    # ------------------------------------------------------------------------------------------------------------------

    def click_navbar_items(self, item_name):
        locator = (By.XPATH, f'//div[contains(@class,"navi navi-bolder")]//t[contains(text(),"{item_name}")]')
        self.click(locator)
    # ------------------------------------------------------------------------------------------------------------------

    def check_audits(self, column_name):
        locator = (By.XPATH, f'//b-grid[@name="audits"]//div[@class="tbl-cell" and contains(text(),"{column_name}")]')
        self.wait_for_element_visible(locator)
    # ------------------------------------------------------------------------------------------------------------------
