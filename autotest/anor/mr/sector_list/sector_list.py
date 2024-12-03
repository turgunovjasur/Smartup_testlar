from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class SectorList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="add()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="add()"]')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, sector_name):
        self.find_row_and_click(element_name=sector_name)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, '//button[@ng-click="view(row)"]')

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
