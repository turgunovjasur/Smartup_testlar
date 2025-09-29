from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class TemplateRoleList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, role_name):
        self.find_row_and_click(element_name=role_name)
    # ------------------------------------------------------------------------------------------------------------------
    attach_button = (By.XPATH, '//button[@ng-click="attach(row)"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_attach_button(self):
        self.click(self.attach_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
