from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class OverloadIdEdit(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = ""

    def element_visible(self, header):
        self.wait_for_element_visible((By.XPATH, header))
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    name_input = ''
    name_elem = 'overload_edit'

    def input_name(self, name_input, name_elem):
        self.input_text((By.XPATH, name_input), name_elem)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = ""

    def click_save_button(self, save_button):
        self.click((By.XPATH, save_button))
    # ------------------------------------------------------------------------------------------------------------------
