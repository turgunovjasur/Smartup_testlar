import time

from autotest.core.md.base_page import BasePage

from selenium.webdriver.common.by import By


class PurchaseList(BasePage):
    ##############################################################################
    purchase_list_header_xpath = "//div/ul/li/a[contains(text(), 'Поступления ТМЦ на склад')]"

    def element_visible(self, purchase_list_header_xpath):
        self.wait_for_element_visible((By.XPATH, purchase_list_header_xpath))

    ##############################################################################
    create_button_xpath = "//div/button[contains(text(), 'Создать')]"

    def click_button(self, create_button_xpath):
        self.wait_and_click((By.XPATH, create_button_xpath))
    ##############################################################################
    purchase_list_1 = "//div[@id='formRow']/descendant::b-grid/descendant::div[4]/following-sibling::div/div[2][@class='tbl-row']"
    list_view = "//div[@class='tbl-row-action']/div/button[1]"

    def check_purchase_list(self, purchase_list_1, list_view):
        self.click((By.XPATH, purchase_list_1))
        self.click((By.XPATH, list_view))
        time.sleep(2)
        print('ok')

    ##############################################################################
