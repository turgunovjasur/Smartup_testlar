from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class SpotTemplateList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="add()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="add()"]')

    def click_add(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close(row)"]')

    def click_close(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, template_name):
        self.find_row_and_click(element_name=template_name)
    # ------------------------------------------------------------------------------------------------------------------
