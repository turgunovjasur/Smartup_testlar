from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class PurchaseId(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    purchase_id_header_xpath = (By.XPATH, "//h5/t[contains(text(),'Основная информация')]")

    def element_visible(self):
        self.wait_for_element_visible(self.purchase_id_header_xpath)
    # ------------------------------------------------------------------------------------------------------------------
    purchase_number = (By.XPATH, "//span[@id='anor377-span-purchase_number']")

    def get_purchase_number(self):
        return self.get_numeric_value(self.purchase_number)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_button = (By.XPATH, "//div[@id='anor377-navbar_item-items']/a")

    def click_inventory_button(self):
        self.click(self.inventory_button)
    # ------------------------------------------------------------------------------------------------------------------
    total_quantity = (By.XPATH, "//div[@id='anor377-navbar-total-information']//div[@class='sg-sub-row']/div[2]")
    total_amount = (By.XPATH, "//div[@id='anor377-navbar-total-information']//div[@class='sg-sub-row']/div[3]")
    total_amount_margin = (By.XPATH, "//div[@id='anor377-navbar-total-information']//div[@class='sg-sub-row']/div[4]")

    def get_elements(self):
        return self.check_count(self.total_amount_margin)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, "//button[@ng-click='page.close()']")

    def click_close_button(self):
        self.click_circle(self.inventory_button)

    # ------------------------------------------------------------------------------------------------------------------
