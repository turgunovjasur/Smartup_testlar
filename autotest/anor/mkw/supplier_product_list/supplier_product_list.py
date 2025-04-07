from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class SupplierProductList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    detach_button = (By.XPATH, '//button[@ng-class="q.classDetach"]')

    def click_detach_button(self):
        self.click(self.detach_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, product_name):
        self.find_row_and_click(element_name=product_name)
    # ------------------------------------------------------------------------------------------------------------------
    attach_one_button = (By.XPATH, '//button[@ng-click="attachOne(row)"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_attach_one_button(self):
        self.click(self.attach_one_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    attach_button = (By.XPATH, '//button[@ng-class="q.classAttach"]')

    def click_attach_button(self):
        self.click(self.attach_button)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
