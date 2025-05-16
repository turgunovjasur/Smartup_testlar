from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class SalesWork(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    show_setting_button = (By.XPATH, '//button[@ng-click="q.show_setting = true"]')

    def click_show_setting(self):
        self.click(self.show_setting_button)
    # ------------------------------------------------------------------------------------------------------------------
    generate_button = (By.XPATH, '//button[@ng-click="generate()"]')

    def click_generate(self):
        self.click(self.generate_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Setting
    # ------------------------------------------------------------------------------------------------------------------
    header_setting = (By.XPATH, '//button[@ng-click="q.show_setting = false"]')

    def element_visible_setting(self):
        return self.wait_for_element_visible(self.header_setting)
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
