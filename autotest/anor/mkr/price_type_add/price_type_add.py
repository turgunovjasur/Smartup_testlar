from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class PriceTypeAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = By.XPATH, "id('anor183-button-save')"

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    code_input = By.XPATH, "id('anor183-input-text-code')/input"

    def input_code(self, code):
        self.input_text(self.code_input, code)
    # ------------------------------------------------------------------------------------------------------------------
    name_input = By.XPATH, "id('anor183-input-text-name')/input"

    def input_name(self, name):
        self.input_text(self.name_input, name)
    # ------------------------------------------------------------------------------------------------------------------
    currency_name_input = By.XPATH, "(id('anor183-input-b_input-currency_name')//input)[2]"
    currency_name = By.XPATH, "id('anor183-input-b_input-currency_name')//div[@class='hint-body ng-scope']/div[7]"

    def input_currency_name(self):
        self.input_text_elem(self.currency_name_input, self.currency_name)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = By.XPATH, "id('anor183-button-save')"

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
