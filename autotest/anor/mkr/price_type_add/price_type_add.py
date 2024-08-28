from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class PriceTypeAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = "id('anor183-button-save')"

    def element_visible(self, header):
        self.wait_for_element_visible((By.XPATH, header))
    # ------------------------------------------------------------------------------------------------------------------
    code_input = "id('anor183-input-text-code')/input"

    def input_code(self, code_input, code):
        self.input_text((By.XPATH, code_input), code)
    # ------------------------------------------------------------------------------------------------------------------
    name_input = "id('anor183-input-text-name')/input"

    def input_name(self, name_input, name):
        self.input_text((By.XPATH, name_input), name)
    # ------------------------------------------------------------------------------------------------------------------
    currency_name_input = "(id('anor183-input-b_input-currency_name')//input)[2]"
    currency_name = "id('anor183-input-b_input-currency_name')//div[@class='hint-body ng-scope']/div[7]"

    def input_currency_name(self, currency_name_input, currency_name):
        self.input_text_elem((By.XPATH, currency_name_input), (By.XPATH, currency_name))
    # ------------------------------------------------------------------------------------------------------------------
    save_button = "id('anor183-button-save')"

    def click_save_button(self, save_button):
        self.click((By.XPATH, save_button))
    # ------------------------------------------------------------------------------------------------------------------
