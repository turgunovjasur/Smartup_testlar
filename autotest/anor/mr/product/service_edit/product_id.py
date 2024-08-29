from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ProductIdEdit(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    card_title_header = ""

    def element_visible(self, card_title_header):
        self.wait_for_element_visible((By.XPATH, card_title_header))
    # ------------------------------------------------------------------------------------------------------------------
    name_input = ""

    def input_name_edit(self, name_input, name_text):
        self.input_text((By.XPATH, name_input), name_text)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = ""

    def click_save_button(self, save_button):
        self.click((By.XPATH, save_button))
    # ------------------------------------------------------------------------------------------------------------------
