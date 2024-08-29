from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class ServiceAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = ""

    def element_visible(self, header):
        self.wait_for_element_visible((By.XPATH, header))
    # ------------------------------------------------------------------------------------------------------------------
    name_input = ''

    def input_name(self, name_input, name_elem):
        self.input_text((By.XPATH, name_input), name_elem)
    # ------------------------------------------------------------------------------------------------------------------
    measure_input = ''
    measure_elem = ''

    def input_measurement(self, measure_input, measure_elem):
        self.input_text_elem((By.XPATH, measure_input), (By.XPATH, measure_elem))
    # ------------------------------------------------------------------------------------------------------------------
    order_input = ""

    def input_order(self, order_input, order):
        self.input_text((By.XPATH, order_input), order)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = ""

    def click_save_button(self, save_button):
        self.click((By.XPATH, save_button))
    # ------------------------------------------------------------------------------------------------------------------
