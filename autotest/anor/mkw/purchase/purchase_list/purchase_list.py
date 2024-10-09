import time
from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class PurchaseList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    purchase_list_header = (By.XPATH, "//div/ul/li/a[contains(text(), 'Поступления ТМЦ на склад')]")

    def element_visible(self):
        self.wait_for_element_visible(self.purchase_list_header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, "//button[@id='anor288-button-add']")

    def click_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    # purchase_id
    # ------------------------------------------------------------------------------------------------------------------
    barcode_button = (By.XPATH, "//div[contains(text(), 'Штрих-код')]")

    def click_2x(self):
        self.click_multiple_time(self.barcode_button, click_count=2, delay=1)
    # ------------------------------------------------------------------------------------------------------------------
    first_list_purchase = (By.XPATH, "//b-grid[@id='anor288-bgrid-table']//div[@class='tbl-row']/div[2]")
    view_button = (By.XPATH, "//div[@class='tbl-row-action']/div/button[1]")

    def open_purchase_list(self):
        time.sleep(2)
        self.click(self.first_list_purchase)
        time.sleep(2)
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
