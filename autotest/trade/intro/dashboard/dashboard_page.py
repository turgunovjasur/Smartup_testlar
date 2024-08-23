import time
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class DashboardPage(BasePage):
    ##############################################################################
    dashboard_header_xpath = "//div/h3[contains(text(), 'Trade')]"

    def element_visible(self, dashboard_header_xpath):
        self.wait_for_element_visible((By.XPATH, dashboard_header_xpath))

    ##############################################################################
    hover_show_button = "//div[@class='pt-3 px-2']"
    filial_button = "//div[@class= 'menus']/child::li[2]/child::a[2]"

    def click_hover_show_button(self, hover_show_button, filial_button):
        self.click((By.XPATH, hover_show_button))
        time.sleep(1)
        self.click((By.XPATH, filial_button))

    ##############################################################################
    sales_button = "//li/a/span[contains(text(), 'Продажа')]"

    def click_sales_button(self, sales_button):
        self.click((By.XPATH, sales_button))

    ##############################################################################
    warehouse_button = "//ul/li[3]/a[@class='menu-link menu-toggle']"

    def click_warehouse_button(self, warehouse_button):
        self.click((By.XPATH, warehouse_button))

    ##############################################################################
    active_session_header = "//h3/t[contains(text(),'Активные сеансы')]"

    def element_visible_session(self, active_session_header, timeout=1):
        self.wait_for_element_visible((By.XPATH, active_session_header), timeout)

    ##############################################################################
    delete_session_button = "(//button[@class='btn btn-icon btn-danger'])[1]"

    def click_button_delete_session(self, delete_session_button, timeout=1):
        self.click((By.XPATH, delete_session_button), timeout=timeout)

    ##############################################################################