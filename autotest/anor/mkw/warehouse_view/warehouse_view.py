from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class WarehouseView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    get_warehouse_name = (By.XPATH, '(//div[contains(@class,"text-center")]//span)[1]')

    def check_warehouse_name(self):
        return self.get_text(self.get_warehouse_name)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------