from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ReturnList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    return_header = (By.XPATH, '//button[@ng-click="add()"')

    def element_visible(self):
        self.wait_for_element_visible(self.return_header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="add()"')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------