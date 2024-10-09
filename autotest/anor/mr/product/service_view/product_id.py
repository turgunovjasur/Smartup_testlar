from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ProductIdView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    card_title_header = By.XPATH, "//h5/t[contains(text(),'Основная информация')]"

    def element_visible(self):
        self.wait_for_element_visible(self.card_title_header)
    # ------------------------------------------------------------------------------------------------------------------
    service_name = By.XPATH, ""

    def get_elements(self):
        self.get_text(self.service_name)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = By.XPATH, "id('anor694-button-close')"

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
