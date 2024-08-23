import json
import os
from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class PurchaseId(BasePage):
    ##############################################################################
    purchase_id_header_xpath = "//h5/t[contains(text(),'Основная информация')]"

    def element_visible(self, purchase_id_header_xpath):
        self.wait_for_element_visible((By.XPATH, purchase_id_header_xpath))

    ##############################################################################
    purchase_number = "//span[@id='anor377-span-purchase_number']/t"

    def get_purchase_number(self):
        return self.check_count(self.purchase_number)

    ##############################################################################
    inventory_button = "//div[@id='anor377-navbar_item-items']/a"

    def fill_form(self, inventory_button):
        self.click((By.XPATH, inventory_button))

    ##############################################################################
    total_quantity = "//div[@id='anor377-navbar-total-information']//div[@class='sg-sub-row']/div[2]"
    total_amount = "//div[@id='anor377-navbar-total-information']//div[@class='sg-sub-row']/div[3]"
    total_amount_margin = "//div[@id='anor377-navbar-total-information']//div[@class='sg-sub-row']/div[4]"

    def get_elements(self):
        return self.check_count(self.total_amount_margin)

    ##############################################################################