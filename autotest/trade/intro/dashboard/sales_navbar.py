from selenium.webdriver.common.by import By

from autotest.core.md.base_page import BasePage


class SalesNavbar(BasePage):
    ##############################################################################
    sales_navbar_header = "//h3/span[contains(text(), 'Продажа')]"

    def element_visible(self, sales_navbar_header):
        self.wait_for_element_visible((By.XPATH, sales_navbar_header))

    ##############################################################################
    orders_button = "//a/span[contains(text(), 'Заказы')]"

    def click_button(self, orders_button):
        self.click((By.XPATH, orders_button))
    ##############################################################################
