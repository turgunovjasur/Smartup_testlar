from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class LicenseList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '(//div[@class="card-header"]//div[@class="card-title"]//t[contains(text(),"Баланс")])[1]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    navbar_button = (By.XPATH, "//div[contains(@class,'navi-item')]/a[@ng-click=\"changeSection('licenses')\"]")

    def click_navbar_button(self):
        self.click(self.navbar_button)
    # ------------------------------------------------------------------------------------------------------------------
    header_licence = (By.XPATH, '//div[@class="card-title"]//t[contains(text(),"Лицензии и документы")]')

    def licence_visible(self):
        self.wait_for_element_visible(self.header_licence)
    # ------------------------------------------------------------------------------------------------------------------
    tbl_row = (By.XPATH, '(//b-grid[@name="table_license"]//div[@class="tbl-row"])[1]')

    def click_tbl_row_button(self):
        self.click(self.tbl_row)
    # ------------------------------------------------------------------------------------------------------------------
    bind_user_button = (By.XPATH, '//b-grid[@name="table_license"]//button[@ng-click="bindUsers(row)"]')

    def click_bind_user_button(self):
        self.click(self.bind_user_button)
    # ------------------------------------------------------------------------------------------------------------------
