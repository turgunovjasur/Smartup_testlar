from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class SalesWorkTemplateAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="save()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, '//input[@ng-model="d.name"]')

    def input_name(self, template_name):
        self.input_text(self.name_input, template_name)
    # ------------------------------------------------------------------------------------------------------------------
    product_groups_input = (By.XPATH, '//b-input[@name="product_groups"]//input')
    options_product_groups = (By.XPATH, '//b-input[@name="product_groups"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_product_groups(self, product_group_name):
        self.click_options(self.product_groups_input, self.options_product_groups, product_group_name)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
