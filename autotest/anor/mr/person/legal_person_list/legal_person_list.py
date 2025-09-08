from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class LegalPersonList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="q.oa.firstFn()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="q.oa.firstFn()"]')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    search_input = (By.XPATH, '//b-grid-controller//input[@type="search"]')

    def input_search(self, element_name):
        self.input_text(self.search_input, element_name)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, legal_person_name):
        self.find_row_and_click(element_name=legal_person_name)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, '//button[@ng-click="view(row)"]')

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
