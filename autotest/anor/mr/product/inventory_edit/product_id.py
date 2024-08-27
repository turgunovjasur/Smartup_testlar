from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ProductId(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    card_title_header = "id('anor66-button-save')"

    def element_visible(self, card_title_header):
        self.wait_for_element_visible((By.XPATH, card_title_header))
    # ------------------------------------------------------------------------------------------------------------------
    name_input = "id('anor66-input-text-name')/input"

    def input_name_edit(self, name_input, name_text):
        self.input_text((By.XPATH, name_input), name_text)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = "id('anor66-button-save')"

    def click_save_button(self, save_button):
        self.click((By.XPATH, save_button))
    # ------------------------------------------------------------------------------------------------------------------
