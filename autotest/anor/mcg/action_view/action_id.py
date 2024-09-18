from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ActionIdView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = ""

    def element_visible(self, header):
        self.wait_for_element_visible((By.XPATH, header))
    # ------------------------------------------------------------------------------------------------------------------
    action_name = ""

    def get_elements(self, action_name):
        self.get_element_value(action_name, as_int=True)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = ""

    def click_close_button(self, close_button):
        self.click((By.XPATH, close_button))
    # ------------------------------------------------------------------------------------------------------------------
