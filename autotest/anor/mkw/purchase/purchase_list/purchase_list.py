import time
from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class PurchaseList(BasePage):
    ##############################################################################
    purchase_list_header = "//div/ul/li/a[contains(text(), 'Поступления ТМЦ на склад')]"

    def element_visible(self, purchase_list_header):
        self.wait_for_element_visible((By.XPATH, purchase_list_header))

    ##############################################################################
    add_button = "//button[@id='anor288-button-add']"

    def click_button(self, add_button):
        self.click((By.XPATH, add_button))

    ##############################################################################
    # purchase_id
    ##############################################################################
    barcode_button = "//div[contains(text(), 'Штрих-код')]"

    def click_2x(self, barcode_button):
        self.click_multiple_time((By.XPATH, barcode_button), click_count=2, delay=1)

    ##############################################################################
    first_list_purchase = "//b-grid[@id='anor288-bgrid-table']//div[@class='tbl-row']/div[2]"
    view_button = "//div[@class='tbl-row-action']/div/button[1]"

    def open_purchase_list(self, first_list_purchase, view_button):
        self.click((By.XPATH, first_list_purchase))
        self.click((By.XPATH, view_button))
        time.sleep(1)

    ##############################################################################