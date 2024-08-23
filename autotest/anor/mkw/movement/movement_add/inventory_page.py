import time
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class InventoryPage(BasePage):
    ##############################################################################
    inventory_page_header_xpath = "//div[@id='anor133-wizard_step-main']"

    def element_visible(self, inventory_page_header_xpath):
        self.wait_for_element_visible((By.XPATH, inventory_page_header_xpath))

    ##############################################################################
    inventory_input = "//b-pg-grid[@id= 'anor133-input-b_pg_grid-inventories']//div/input"
    inventory_input_elem = "//b-pg-grid[@id= 'anor133-input-b_pg_grid-inventories']/descendant::div[@class='hint-item ng-scope active']"
    quantity_input = "//input[@id='anor133-input-text-quantity-0']"
    quantity = "1"

    def fill_form(self, inventory_input, inventory_input_elem,
                  quantity_input, quantity):
        self.input_text_elem((By.XPATH, inventory_input), (By.XPATH, inventory_input_elem))
        time.sleep(1)
        self.input_text((By.XPATH, quantity_input), quantity)
        time.sleep(1)

    ##############################################################################
    next_button = "//div[@id='anor133-wizard_step-finish']"

    def click_button(self, next_button):
        self.click((By.XPATH, next_button))

    ##############################################################################