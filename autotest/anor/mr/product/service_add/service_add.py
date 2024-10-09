from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class ServiceAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = By.XPATH, "id('anor85-button-save')"

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    name_input = By.XPATH, "id('anor85-input-text-name')/input"

    def input_name(self, name_elem):
        self.input_text(self.name_input, name_elem)
    # ------------------------------------------------------------------------------------------------------------------
    measure_input = By.XPATH, "(id('anor85-input-b_input-measure_short_name')//input)[2]"
    measure_elem = By.XPATH, "id('anor85-input-b_input-measure_short_name')//div[@class='hint-body ng-scope']/div[1]"

    def input_measurement(self):
        self.input_text_elem(self.measure_input, self.measure_elem)
    # ------------------------------------------------------------------------------------------------------------------
    order_input = By.XPATH, "id('anor85-input-text-order_no')/input"

    def input_order(self, order):
        self.input_text(self.order_input, order)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = By.XPATH, "id('anor85-button-save')"

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
