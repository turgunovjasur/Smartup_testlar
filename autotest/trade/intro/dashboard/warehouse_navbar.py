from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class WarehouseNavbar(BasePage):
    ##############################################################################
    warehouse_navbar_header = "//li/h3/span[contains(text(), 'Документы')]"

    def element_visible(self, warehouse_navbar_header):
        self.wait_for_element_visible((By.XPATH, warehouse_navbar_header))

    ##############################################################################
    purchases_button = "//ul/li[4]/a[2]"

    def click_button_purchases(self, purchases_button):
        self.click((By.XPATH, purchases_button))

    ##############################################################################
    inventory_receipts_button = "//ul/li[5]/a[2]"

    def click_button_inventory_receipts(self, inventory_receipts_button):
        self.click((By.XPATH, inventory_receipts_button))

    ##############################################################################
    internal_movements_button = "//ul/li/a/span[contains(text(), 'Внутренние перемещения')]"

    def click_button_internal_movements(self, internal_movements_button_xpath):
        self.click((By.XPATH, internal_movements_button_xpath))

    ##############################################################################