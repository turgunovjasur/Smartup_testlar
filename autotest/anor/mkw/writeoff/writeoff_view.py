from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class WriteOffView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
    search_input = (By.XPATH, '//b-pg-controller[@name="expenses"]//input')

    def input_search(self, search_name):
        self.input_text(self.search_input, search_name)
    # ------------------------------------------------------------------------------------------------------------------

    def click_navbar_button(self, navbar_name):
        locator = (By.XPATH, f'//div[contains(@class,"navi-item")]//t[contains(.,"{navbar_name}")]')
        self.click(locator)
    # ------------------------------------------------------------------------------------------------------------------

    def check_expenses(self, expense_name):
        locator = (By.XPATH, f'//b-pg-grid[@name="expenses"]//div[contains(text(),"{expense_name}")]')
        self.wait_for_element(locator, wait_type="visibility")
    # ------------------------------------------------------------------------------------------------------------------

    def get_input_value(self, input_name):
        locator = (By.XPATH, f'//label[contains(.,"{input_name}")]/../span')
        return self.get_text(locator)
    # ------------------------------------------------------------------------------------------------------------------
