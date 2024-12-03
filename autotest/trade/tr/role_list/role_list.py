from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class RoleList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="fi.add()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def click_row_button(self, role_name):
        self.find_row_and_click(element_name=role_name)
    # ------------------------------------------------------------------------------------------------------------------
    edit_button = (By.XPATH, '//button[@ng-click="edit(row)"]')

    def click_edit_button(self):
        self.click(self.edit_button)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, '//button[@ng-click="view(row)"]')

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
