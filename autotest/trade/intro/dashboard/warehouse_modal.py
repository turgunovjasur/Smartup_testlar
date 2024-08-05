from selenium.webdriver.common.by import By

from autotest.core.md.base_page import BasePage


class WarehouseModal(BasePage):
    ##############################################################################
    warehouse_modal_header_xpath = "//li/h3/span[contains(text(), 'Документы')]"

    def element_visible(self, warehouse_modal_header_xpath):
        self.wait_for_element_visible((By.XPATH, warehouse_modal_header_xpath))

    ##############################################################################
    purchases_button_xpath = "//ul/li[4]/a[2]"

    def click_button(self, purchases_button_xpath):
        self.wait_and_click((By.XPATH, purchases_button_xpath))
    ##############################################################################
