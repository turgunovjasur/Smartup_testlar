from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class SpotTemplateAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '(//button[@ng-click="page.close()"])[2]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, '//input[@ng-model="d.name"]')

    def input_name(self, template_name):
        self.input_text(self.name_input, template_name)
    # ------------------------------------------------------------------------------------------------------------------
    order_no_input = (By.XPATH, '//input[@ng-model="d.order_no"]')

    def input_order_nomer(self, order_nomer):
        self.input_text(self.order_no_input, order_nomer)
    # ------------------------------------------------------------------------------------------------------------------
    product_groups_input = (By.XPATH, '//b-input[@name="product_groups"]//input')
    product_groups_options = (By.XPATH, '//b-input[@name="product_groups"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_product_groups(self, product_group_name):
        self.click_options(self.product_groups_input, self.product_groups_options, product_group_name)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '(//button[@ng-click="save()"])[2]')

    def click_save(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
