from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class SalesWorkTemplateList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()" and @ng-hide="page.isFirst()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="add()"]')

    def click_add(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
