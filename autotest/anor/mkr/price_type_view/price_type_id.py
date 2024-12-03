from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class PriceTypeIdView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    card_title_header = (By.XPATH, "//div[@class='card-title']/h5/t")

    def element_visible(self):
        return self.wait_for_element_visible(self.card_title_header)
    # ------------------------------------------------------------------------------------------------------------------
    get_name = (By.XPATH, "//div[@id='anor793-navbar-header-information']//span[1]")

    def get_elements(self):
        return self.get_text(self.get_name)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, "//button[@id='anor793-button-close']")

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
