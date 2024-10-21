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

    def click_row_list(self):
        self.click(self.first_list_purchase)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, "//button[@id='anor288-button-view']")

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    status_one_button = (By.XPATH, "//button[@id='anor288-button-changestatus']")
    status_draft_button = (By.XPATH, "//div[@id='statusDropDown']//div[@class='card-body p-0']/a[1]")
    status_yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_status_one_button(self):
        self.click(self.status_one_button)
        self.click(self.status_draft_button)
        self.click(self.status_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    delete_one_button = (By.XPATH, "//button[@id='anor288-button-delete']")
    delete_yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_delete_one_button(self):
        self.click(self.delete_one_button)
        self.click(self.delete_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
