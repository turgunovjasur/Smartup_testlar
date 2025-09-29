from selenium.webdriver.common.by import By
from pages.core.md.base_page import BasePage


class PriceTypeListAttach(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    attach_many_button = (By.XPATH, '//button[@ng-click="attachMany()"]')
    attach_button = (By.XPATH, '//button[@id="anor182-button-attach"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def find_rows(self, price_type_name):
        self.find_row_and_click(element_name=price_type_name)
        self.click(self.attach_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
