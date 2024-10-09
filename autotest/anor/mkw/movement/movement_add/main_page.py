import random
import time
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class MainPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    main_page_header = "//div[@id='anor133-wizard_step-main']"

    def element_visible(self, main_page_header):
        self.wait_for_element_visible((By.XPATH, main_page_header))

    # ------------------------------------------------------------------------------------------------------------------
    movement_number_input = "(//div[@id='anor133-input-text-movement_number']//input)[2]"
    from_warehouses_input = "//div[@id= 'anor133-input-b_input-from_warehouses']//b-input//input"
    from_warehouses_elem = "//div[@id= 'anor133-input-b_input-from_warehouses']//div[@class='hint-body ng-scope']/div[1]"
    to_warehouses_input = "//div[@id= 'anor133-input-b_input-to_warehouses_name']//b-input//input"
    to_warehouses_elem = "//div[@id= 'anor133-input-b_input-to_warehouses_name']//div[@class='hint-body ng-scope']/div[2]"
    # ------------------------------------------------------------------------------------------------------------------

    def fill_form(self, movement_number_input,
                  from_warehouses_input, from_warehouses_elem,
                  to_warehouses_input, to_warehouses_elem):
        self.number = random.randint(1, 9999)
        time.sleep(1)
        self.input_text((By.XPATH, movement_number_input), self.number)
        self.input_text_elem((By.XPATH, from_warehouses_input), (By.XPATH, from_warehouses_elem))
        time.sleep(1)
        self.input_text_elem((By.XPATH, to_warehouses_input), (By.XPATH, to_warehouses_elem))
        time.sleep(1)
    # ------------------------------------------------------------------------------------------------------------------

    def random_number(self):
        return self.number
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = "//div[@id= 'anor133-wizard_step-inventory']"

    def click_button(self, next_step_button):
        self.click((By.XPATH, next_step_button))
    # ------------------------------------------------------------------------------------------------------------------
