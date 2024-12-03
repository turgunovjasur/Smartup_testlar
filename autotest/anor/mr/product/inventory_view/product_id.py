from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ProductId(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    card_title_header = By.XPATH, "//h5/t[contains(text(),'Основная информация')]"

    def element_visible(self):
        return self.wait_for_element_visible(self.card_title_header)
    # ------------------------------------------------------------------------------------------------------------------
    product_name = By.XPATH, "//div[@id='anor393-span-name']/span[1]"

    def get_elements(self):
        return self.get_text(self.product_name)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = By.XPATH, "id('anor393-button-close')"

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
