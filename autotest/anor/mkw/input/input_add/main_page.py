import random
import time
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.number = None
    # ------------------------------------------------------------------------------------------------------------------
    main_page_header = (By.XPATH, "//div[@id='anor113-wizard_wrapper-main']")

    def element_visible(self):
        self.wait_for_element_visible(self.main_page_header)
    # ------------------------------------------------------------------------------------------------------------------
    input_number_input = (By.XPATH, "//div[@id='anor113-input-text-input_number']/input")
    warehouse_input = (By.XPATH, "//div[@id='anor113-input-b_input-warehouse_name']/descendant::input[2]")
    warehouse_elem = (By.XPATH, "//div[@id='anor113-input-b_input-warehouse_name']//div[@class='hint-body ng-scope']/div[1]")
    extra_cost_enabled_checkbox = (By.XPATH, "//div[@id='anor113-input-checkbox-extra_cost_enabled']/descendant::label[@class='checkbox']")

    def fill_form(self):
        self.number = random.randint(1, 9999)
        self.input_text(self.input_number_input, self.number)
        self.input_text_elem(self.warehouse_input, self.warehouse_elem)
        time.sleep(1)
        self.click(self.extra_cost_enabled_checkbox)
        time.sleep(1)
    # ------------------------------------------------------------------------------------------------------------------

    def random_number(self):
        return self.number
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = (By.XPATH, "//div[@id='anor113-wizard-purchase']")

    def click_button(self):
        self.click(self.next_step_button)

    # ------------------------------------------------------------------------------------------------------------------
