from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ProductIdView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    card_title_header = "//h5/t[contains(text(),'Основная информация')]"

    def element_visible(self, card_title_header):
        self.wait_for_element_visible((By.XPATH, card_title_header))
    # ------------------------------------------------------------------------------------------------------------------
    service_name = ""

    def get_elements(self, service_name):
        self.get_element_value(service_name, as_int=True)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = "id('anor694-button-close')"

    def click_close_button(self, close_button):
        self.click((By.XPATH, close_button))
    # ------------------------------------------------------------------------------------------------------------------
