from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class Optimum(BasePage):
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
        self._wait_for_all_loaders()
        self.click(self.generate_button)
    # ------------------------------------------------------------------------------------------------------------------
    is_all_filials = (By.XPATH, '//input[@ng-model="q.is_all_filials"]')

    def click_all_filial_checkbox(self):
        self.click_checkbox(self.is_all_filials, state=False)
    # ------------------------------------------------------------------------------------------------------------------
    filial_input = (By.XPATH, '//b-input[@name="filials"]//input')
    filial_options = (By.XPATH, '//b-input[@name="filials"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_filial(self, filial_name):
        self.click_options(self.filial_input, self.filial_options, filial_name)
    # ------------------------------------------------------------------------------------------------------------------
    # Setting
    # ------------------------------------------------------------------------------------------------------------------
    header_setting = (By.XPATH, '//button[@ng-click="q.show_setting = false"]')

    def element_visible_setting(self):
        return self.wait_for_element_visible(self.header_setting)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
    product_groups_input = (By.XPATH, '//b-input[@name="product_groups"]//input')
    product_groups_options = (By.XPATH, '//b-input[@name="product_groups"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_product_groups(self, product_group):
        self.click_options(self.product_groups_input, self.product_groups_options, product_group)
    # ------------------------------------------------------------------------------------------------------------------
    prefix_transfer_out_input = (By.XPATH, '//input[@ng-model="d.prefix_transfer_out"]')

    def input_prefix_transfer_out(self, prefix_transfer_out):
        self.input_text(self.prefix_transfer_out_input, prefix_transfer_out)
    # ------------------------------------------------------------------------------------------------------------------
    prefix_transfer_in_input = (By.XPATH, '//input[@ng-model="d.prefix_transfer_in"]')

    def input_prefix_transfer_in(self, prefix_transfer_in):
        self.input_text(self.prefix_transfer_in_input, prefix_transfer_in)
    # ------------------------------------------------------------------------------------------------------------------
    prefix_write_off_input = (By.XPATH, '//input[@ng-model="d.prefix_write_off"]')

    def input_prefix_write_off(self, prefix_write_off):
        self.input_text(self.prefix_write_off_input, prefix_write_off)
    # ------------------------------------------------------------------------------------------------------------------
    prefix_warehouse_receipt_input = (By.XPATH, '//input[@ng-model="d.prefix_warehouse_receipt"]')

    def input_prefix_warehouse_receipt(self, prefix_warehouse_receipt):
        self.input_text(self.prefix_warehouse_receipt_input, prefix_warehouse_receipt)
    # ------------------------------------------------------------------------------------------------------------------
    prefix_site_transfer_out_input = (By.XPATH, '//input[@ng-model="d.prefix_site_transfer_out"]')

    def input_prefix_site_transfer_out(self, prefix_site_transfer_out):
        self.input_text(self.prefix_site_transfer_out_input, prefix_site_transfer_out)
    # ------------------------------------------------------------------------------------------------------------------
    prefix_site_transfer_in_input = (By.XPATH, '//input[@ng-model="d.prefix_site_transfer_in"]')

    def input_prefix_site_transfer_in(self, prefix_site_transfer_in):
        self.input_text(self.prefix_site_transfer_in_input, prefix_site_transfer_in)
    # ------------------------------------------------------------------------------------------------------------------
    prefix_production_write_off_input = (By.XPATH, '//input[@ng-model="d.prefix_production_write_off"]')

    def input_prefix_production_write_off(self, prefix_production_write_off):
        self.input_text(self.prefix_production_write_off_input, prefix_production_write_off)
    # ------------------------------------------------------------------------------------------------------------------
    prefix_production_receipt_input = (By.XPATH, '//input[@ng-model="d.prefix_production_receipt"]')

    def input_prefix_production_receipt(self, prefix_production_receipt):
        self.input_text(self.prefix_production_receipt_input, prefix_production_receipt)
    # ------------------------------------------------------------------------------------------------------------------