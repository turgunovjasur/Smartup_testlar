from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ProductSetPrice(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    # ------------------------------------------------------------------------------------------------------------------
    price1_input = (By.XPATH, '(//input[@ng-model="row.price"])[1]')
    price2_input = (By.XPATH, '(//input[@ng-model="row.price"])[2]')

    def input_set_price(self, price1, price2):
        self.input_text(self.price1_input, price1)
        self.input_text(self.price2_input, price2)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')
    yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
