from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class CashinView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    get_cashin_number = (By.XPATH, '//div[@class="b-offcanvas-hide"]/span[1]')

    def check_cashin_number(self):
        return self.get_numeric_value(self.get_cashin_number)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
