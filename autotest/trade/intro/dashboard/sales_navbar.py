from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class SalesNavbar(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    sales_navbar_header = (By.XPATH, "//h3/span[contains(text(), 'Продажа')]")

    def element_visible(self):
        self.wait_for_element_visible(self.sales_navbar_header)
    # ------------------------------------------------------------------------------------------------------------------
    orders_button = (By.XPATH, "//a/span[contains(text(), 'Заказы')]")

    def click_orders_button(self):
        self.click(self.orders_button)
    # ------------------------------------------------------------------------------------------------------------------
    orders_archive_button = (By.XPATH, "//div[@id='kt_header_menu']/ul/li[2]/div/div/ul/li[2]/ul/li[4]/a")

    def click_orders_archive_button(self):
        self.click(self.orders_archive_button)
    # ------------------------------------------------------------------------------------------------------------------
