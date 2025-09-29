from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class TemplateList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="add()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="add()"]')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, template_name):
        self.find_row_and_click(element_name=template_name)
    # ------------------------------------------------------------------------------------------------------------------
    attach_role_button = (By.XPATH, '//button[@ng-if="fi.attach_role"]')

    def click_attach_role_button(self):
        self.click(self.attach_role_button)
    # ------------------------------------------------------------------------------------------------------------------
    detach_role_button = (By.XPATH, '//button[@ng-class="q.classDetach"]')

    def click_detach_role_button(self):
        self.click(self.detach_role_button)
    # ------------------------------------------------------------------------------------------------------------------
