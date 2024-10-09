import time
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class InventoryPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    inventory_page_header = "//div[@id='anor133-wizard_step-main']"

    def element_visible(self, inventory_page_header):
        self.wait_for_element_visible((By.XPATH, inventory_page_header))
    # ------------------------------------------------------------------------------------------------------------------
    fast_search_input = "//b-input[@id= 'anor133-input-b_input-fast_search_query-0']//input"
    fast_search_elem = "//b-input[@id= 'anor133-input-b_input-fast_search_query-0']//div[@class='hint-body ng-scope']/div"
    quantity_input = "//input[@id='anor133-input-text-quantity-0']"

    def fill_form(self, fast_search_input, fast_search_elem,
                  quantity_input, quantity):
        self.input_text_elem((By.XPATH, fast_search_input), (By.XPATH, fast_search_elem))
        self.input_text((By.XPATH, quantity_input), quantity)
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = "//div[@id='anor133-wizard_step-finish']"

    def click_button(self, next_step_button):
        self.click((By.XPATH, next_step_button))

    # ------------------------------------------------------------------------------------------------------------------
