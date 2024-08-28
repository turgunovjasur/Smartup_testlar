from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class PriceTypeIdView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    card_title_header = "//div[@class='card-title']/h5/t"

    def element_visible(self, card_title_header):
        self.wait_for_element_visible((By.XPATH, card_title_header))
    # ------------------------------------------------------------------------------------------------------------------
    price_name = "id('anor793-navbar-header-information')/div/span[1]"

    def get_elements(self, price_name):
        self.get_element_value(price_name, as_int=True)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = "id('anor793-button-close')"

    def click_close_button(self, close_button):
        self.click((By.XPATH, close_button))
    # ------------------------------------------------------------------------------------------------------------------
