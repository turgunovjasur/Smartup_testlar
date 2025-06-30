from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class CisLink(BasePage):
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
    header_setting = (By.XPATH, '//button[@b-hotkey="close"]')

    def element_visible_setting(self):
        return self.wait_for_element_visible(self.header_setting)
    # ------------------------------------------------------------------------------------------------------------------
    identification_code_input = (By.XPATH, '//input[@ng-model="d.identification_code"]')

    def input_identification_code(self, identification_code_name):
        self.input_text(self.identification_code_input, identification_code_name)
    # ------------------------------------------------------------------------------------------------------------------
    person_groups_input = (By.XPATH, '//b-input[@name="person_groups"]//input')
    options_person_groups = (By.XPATH, '//b-input[@name="person_groups"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_person_groups(self, person_groups_name):
        self.click_options(self.person_groups_input, self.options_person_groups, person_groups_name)
    # ------------------------------------------------------------------------------------------------------------------
    product_groups_input = (By.XPATH, '//b-input[@name="product_groups"]//input')
    options_product_groups = (By.XPATH, '//b-input[@name="product_groups"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_product_groups(self, product_group_name):
        self.click_options(self.product_groups_input, self.options_product_groups, product_group_name)
    # ------------------------------------------------------------------------------------------------------------------
    filial_input = (By.XPATH, '//b-input[@name="filials"]//input')
    options_filial = (By.XPATH, '//b-input[@name="filials"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_filial(self, filial_name):
        self.click_options(self.filial_input, self.options_filial, filial_name)
    # ------------------------------------------------------------------------------------------------------------------
    price_types_input = (By.XPATH, '//b-input[@name="price_types"]//input')
    options_price_types = (By.XPATH, '//b-input[@name="price_types"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_price_types(self, price_types_name):
        self.click_options(self.price_types_input, self.options_price_types, price_types_name)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------