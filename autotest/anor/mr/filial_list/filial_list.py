from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class FilialList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = By.XPATH, '//button[@ng-click="fi.add()"]'

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    add_button = By.XPATH, '//button[@ng-click="fi.add()"]'

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_filial_row(self, filial_name):
        self.find_row_and_click(element_name=filial_name)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = By.XPATH, '//button[@ng-click="view(row)"]'

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
