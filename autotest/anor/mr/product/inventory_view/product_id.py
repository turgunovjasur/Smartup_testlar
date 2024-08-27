from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ProductId(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    card_title_header = "//h5/t[contains(text(),'Основная информация')]"

    def element_visible(self, card_title_header):
        self.wait_for_element_visible((By.XPATH, card_title_header))
    # ------------------------------------------------------------------------------------------------------------------
    product_name = "(id('anor393-span-name')/span/text())[1]"

    def get_elements(self, product_name):
        self.get_element_value(product_name, as_int=True)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = "id('anor393-button-close')"

    def click_close_button(self, close_button):
        self.click((By.XPATH, close_button))
    # ------------------------------------------------------------------------------------------------------------------
