from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class LegalPersonList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="q.oa.firstFn()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="q.oa.firstFn()"]')
    # add_button = (By.XPATH, '//sdllsklfk')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, legal_person_name):
        self.find_row_and_click(element_name=legal_person_name)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, '//button[@ng-click="view(row)"]')

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    limit_button = (By.XPATH, '//button[@class="btn btn-default rounded-0 ng-binding"]')

    def click_limit_button(self, limit):
        self.click(self.limit_button)

        item_button = (By.XPATH, f'//button[@class="btn btn-default rounded-0 ng-binding"]/following-sibling::div/a[{limit}]')
        self.click(item_button)
    # ------------------------------------------------------------------------------------------------------------------
