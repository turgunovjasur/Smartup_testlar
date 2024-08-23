import random
import time
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class MainPage(BasePage):
    ##############################################################################
    main_page_header = "//div[@id='anor133-wizard_step-main']"

    def element_visible(self, main_page_header):
        self.wait_for_element_visible((By.XPATH, main_page_header))

    ##############################################################################
    movement_no_input = "(//div[@id='anor133-input-text-movement_number']//input)[2]"

    consignor_warehouse = "//div[@id= 'anor133-input-b_input-from_warehouses']//b-input//input"
    consignor_warehouse_elem = "//div[@id= 'anor133-input-b_input-from_warehouses']//div[@class='hint-body ng-scope']/div[1]"

    consignee_warehouse = "//div[@id= 'anor133-input-b_input-to_warehouses_name']//b-input//input"
    consignee_warehouse_elem = "//div[@id= 'anor133-input-b_input-to_warehouses_name']//div[@class='hint-body ng-scope']/div[2]"

    def fill_form(self, movement_no_input,
                  consignor_warehouse, consignor_warehouse_elem,
                  consignee_warehouse, consignee_warehouse_elem):
        self.number = random.randint(1, 9999)
        time.sleep(1)
        self.input_text((By.XPATH, movement_no_input), self.number)
        self.input_text_elem((By.XPATH, consignor_warehouse), (By.XPATH, consignor_warehouse_elem))
        time.sleep(1)
        self.input_text_elem((By.XPATH, consignee_warehouse), (By.XPATH, consignee_warehouse_elem))
        time.sleep(1)

    ##############################################################################
    def random_number(self):
        return self.number

    ##############################################################################
    next_button = "//div[@id= 'anor133-wizard_step-inventory']"

    def click_button(self, next_button):
        self.click((By.XPATH, next_button))

    ##############################################################################