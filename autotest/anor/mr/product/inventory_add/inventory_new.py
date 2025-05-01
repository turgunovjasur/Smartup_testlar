from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage
from utils.exception import ElementVisibilityError


class InventoryNew(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    inventory_new_header = (By.XPATH, "//button[@id='anor66-button-save' and contains(text(), 'Сохранить')]")

    def element_visible(self):
        return self.wait_for_element_visible(self.inventory_new_header)
    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, '//div[@id= "anor66-input-text-name"]/input')

    def input_name(self, product_name):
        self.input_text(self.name_input, product_name)
    # ------------------------------------------------------------------------------------------------------------------
    measurement_input = (By.XPATH, '//div[@id= "anor66-input-text-measure_short_name"]//b-input[@name="measures"]//input')
    measurement_elem = (By.XPATH, '//div[@id= "anor66-input-text-measure_short_name"]//b-input[@name="measures"]'
                                  '//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def input_measurement(self, measurement_name):
        self.click_options(self.measurement_input, self.measurement_elem, measurement_name)
    # ------------------------------------------------------------------------------------------------------------------
    goods_checkbox = (By.XPATH, "//label[@id='anor66-input-checkbox-inventory_kinds-G']")

    def click_goods_checkbox(self):
        self.click(self.goods_checkbox)
    # ------------------------------------------------------------------------------------------------------------------
    suppliers_input = (By.XPATH, '//b-input[@name="suppliers"]//input')
    suppliers_options = (By.XPATH, '//b-input[@name="suppliers"]//div[contains(@class,"hint-item")]/div[contains(@class,"form-row")]/div')

    def input_suppliers(self, supplier_name):
        self.click_options(self.suppliers_input, self.suppliers_options, supplier_name)
    # ------------------------------------------------------------------------------------------------------------------
    product_checkbox = (By.XPATH, "//label[@id='anor66-input-checkbox-inventory_kinds-P']")

    def click_product_checkbox(self):
        self.click(self.product_checkbox)
    # ------------------------------------------------------------------------------------------------------------------
    weight_netto_input = (By.XPATH, '//input[@ng-model="d.weight_netto"]')

    def input_weight_netto(self, weight_netto):
        self.input_text(self.weight_netto_input, weight_netto)
    # ------------------------------------------------------------------------------------------------------------------
    weight_brutto_input = (By.XPATH, '//input[@ng-model="d.weight_brutto"]')

    def input_weight_brutto(self, weight_brutto):
        self.input_text(self.weight_brutto_input, weight_brutto)
    # ------------------------------------------------------------------------------------------------------------------
    litre_input = (By.XPATH, '//input[@ng-model="d.litr"]')

    def input_litre(self, litre):
        self.input_text(self.litre_input, litre)
    # ------------------------------------------------------------------------------------------------------------------
    # product_order_input = (By.XPATH, "//div[@id='anor66-input-text-order_no']/input")
    #
    # def input_order(self, product_order):
    #     self.input_text(self.product_order_input, product_order)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, "//button[@id='anor66-button-save']")

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
    error_massage_xpath = (By.XPATH, '//div[@id="biruniAlertExtended"]//div[@class="modal-content"]//div[@class="modal-title"]//div[@class="ng-binding"]')

    def error_massage(self):
        """Error xabarini tekshirish va olish"""

        try:
            self.wait_for_element(self.error_massage_xpath, timeout=5, wait_type="visibility", error_message=False)
        except ElementVisibilityError:
            return False

        full_text = self.get_text(self.error_massage_xpath)
        if full_text:
            error_code = full_text.split('—')[0].strip() if "—" in full_text else full_text.strip()
            return error_code
    # ------------------------------------------------------------------------------------------------------------------
    clear_button = (By.XPATH, '//b-input[@name="sectors"]//span[@class="clear-button"]')
    sectors_input = (By.XPATH, '//b-input[@name="sectors"]//input')
    sectors_elem = (By.XPATH, '//b-input[@name="sectors"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def input_sectors(self, sector_name):
        self.click(self.clear_button)
        self.click_options(self.sectors_input, self.sectors_elem, sector_name)
    # ------------------------------------------------------------------------------------------------------------------
