from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class PriceTypeIdView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    card_title_header = By.XPATH, "//div[@class='card-title']/h5/t"

    def element_visible(self):
        self.wait_for_element_visible(self.card_title_header)
    # ------------------------------------------------------------------------------------------------------------------
    price_name = By.XPATH, "id('anor793-navbar-header-information')/div/span[1]"

    def get_elements(self):
        self.get_text(self.price_name)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = By.XPATH, "id('anor793-button-close')"

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
