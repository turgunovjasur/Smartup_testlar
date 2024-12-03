from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ProductSetPrice(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="save()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    text = (By.XPATH, '//label[@class="form-view ng-binding"]')

    def check_product(self):
        return self.get_text(self.text)
    # ------------------------------------------------------------------------------------------------------------------
    prices_input = (By.XPATH, '//b-pg-grid[@name="prices"]//input')

    def input_prices(self, product_price):
        self.input_text(self.prices_input, product_price)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')
    yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
