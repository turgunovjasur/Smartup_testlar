from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class SupplierAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="save()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    persons_input = (By.XPATH, '(//b-input[@name="persons"]//input)[1]')
    persons_options = (By.XPATH, '//b-input[@name="persons"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_persons(self, supplier_name):
        self.click_options(self.persons_input, self.persons_options, supplier_name)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="save()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_add_button(self):
        self.click(self.add_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
