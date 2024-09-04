from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class ServiceAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = "id('anor85-button-save')"

    def element_visible(self, header):
        self.wait_for_element_visible((By.XPATH, header))
    # ------------------------------------------------------------------------------------------------------------------
    name_input = "id('anor85-input-text-name')/input"

    def input_name(self, name_input, name_elem):
        self.input_text((By.XPATH, name_input), name_elem)
    # ------------------------------------------------------------------------------------------------------------------
    measure_input = "(id('anor85-input-b_input-measure_short_name')//input)[2]"
    measure_elem = "id('anor85-input-b_input-measure_short_name')//div[@class='hint-body ng-scope']/div[1]"

    def input_measurement(self, measure_input, measure_elem):
        self.input_text_elem((By.XPATH, measure_input), (By.XPATH, measure_elem))
    # ------------------------------------------------------------------------------------------------------------------
    order_input = "id('anor85-input-text-order_no')/input"

    def input_order(self, order_input, order):
        self.input_text((By.XPATH, order_input), order)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = "id('anor85-button-save')"

    def click_save_button(self, save_button):
        self.click((By.XPATH, save_button))
    # ------------------------------------------------------------------------------------------------------------------
