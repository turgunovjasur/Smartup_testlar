from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class WarehouseNavbar(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    warehouse_navbar_header = (By.XPATH, "//li/h3/span[contains(text(), 'Документы')]")

    def element_visible(self):
        self.wait_for_element_visible(self.warehouse_navbar_header)
    # ------------------------------------------------------------------------------------------------------------------
    purchases_button = (By.XPATH, "//ul/li[4]/a[2]")

    def click_button_purchases(self):
        self.click(self.purchases_button)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_receipts_button = (By.XPATH, "//ul/li[5]/a[2]")

    def click_button_inventory_receipts(self):
        self.click(self.inventory_receipts_button)
    # ------------------------------------------------------------------------------------------------------------------
    internal_movements_button = (By.XPATH, "//ul/li/a/span[contains(text(), 'Внутренние перемещения')]")

    def click_button_internal_movements(self):
        self.click(self.internal_movements_button)
    # ------------------------------------------------------------------------------------------------------------------
