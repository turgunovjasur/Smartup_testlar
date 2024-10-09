from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ProductId(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    card_title_header = By.XPATH, "id('anor66-button-save')"

    def element_visible(self):
        self.wait_for_element_visible(self.card_title_header)
    # ------------------------------------------------------------------------------------------------------------------
    name_input = By.XPATH, "id('anor66-input-text-name')/input"

    def input_name_edit(self, name_text):
        self.input_text(self.name_input, name_text)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = By.XPATH, "id('anor66-button-save')"

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
