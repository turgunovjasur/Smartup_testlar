import random
import time
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class MainPage(BasePage):
    ##############################################################################
    main_page_header = "//div[@id='anor113-wizard_wrapper-main']"

    def element_visible(self, main_page_header):
        self.wait_for_element_visible((By.XPATH, main_page_header))

    ##############################################################################
    input_number_input = "//div[@id='anor113-input-text-input_number']/input"
    warehouse_input = "//div[@id='anor113-input-b_input-warehouse_name']/descendant::input[2]"
    warehouse_elem = "//div[@id='anor113-input-b_input-warehouse_name']//div[@class='hint-body ng-scope']/div[1]"
    extra_cost_enabled_checkbox = "//div[@id='anor113-input-checkbox-extra_cost_enabled']/descendant::label[@class='checkbox']"

    def fill_form(self, input_number_input, warehouse_input, warehouse_elem, extra_cost_enabled_checkbox):
        self.number = random.randint(1, 9999)
        self.input_text((By.XPATH, input_number_input), self.number)
        self.input_text_elem((By.XPATH, warehouse_input), (By.XPATH, warehouse_elem))
        time.sleep(1)
        self.click((By.XPATH, extra_cost_enabled_checkbox))
        time.sleep(1)

    ##############################################################################
    def random_number(self):
        return self.number

    ##############################################################################
    next_step_button = "//div[@id='anor113-wizard-purchase']"

    def click_button(self, next_step_button):
        self.click((By.XPATH, next_step_button))

    ##############################################################################