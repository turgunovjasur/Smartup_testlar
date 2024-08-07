import time

from selenium.webdriver.common.by import By

from autotest.core.md.base_page import BasePage


class DashboardPage(BasePage):
    ##############################################################################
    dashboard_header_xpath = "//div/h3[contains(text(), 'Trade')]"

    def element_visible(self, dashboard_header_xpath):
        self.wait_for_element_visible((By.XPATH, dashboard_header_xpath))

    ##############################################################################
    organizations_menu = "//div[@class='pt-3 px-2']"
    organizations_xpath = "//div[@class= 'menus']/child::li[2]/child::a[3]"

    def click_organizations_button(self, organizations_menu, organizations_xpath):
        self.wait_and_click((By.XPATH, organizations_menu))
        time.sleep(2)
        self.wait_and_click((By.XPATH, organizations_xpath))

    ##############################################################################
    sales_button_xpath = "//li/a/span[contains(text(), 'Продажа')]"

    def click_sales_button(self, sales_button_xpath):
        self.wait_and_click((By.XPATH, sales_button_xpath))

    ##############################################################################
    warehouse_button_xpath = "//ul/li[3]/a[@class='menu-link menu-toggle']"

    def click_warehouse_button(self, warehouse_button_xpath):
        self.wait_and_click((By.XPATH, warehouse_button_xpath))
    ##############################################################################
