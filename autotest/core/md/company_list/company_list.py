from time import time
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class CompanyList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="fi.add()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="fi.add()"]')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    reload_button = (By.XPATH, '//button[@ng-click="reload()"]')

    def click_reload_button(self):
        self.click(self.reload_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_company(self, code_input):
        self.find_row_and_click(element_name=code_input)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, '//button[@ng-click="view(row)"]')

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
