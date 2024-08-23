from selenium.webdriver.common.by import By

from autotest.core.md.base_page import BasePage


class InputId(BasePage):
    ##############################################################################
    input_id_header = "//h5/t[contains(text(),'Основная информация')]"

    def element_visible(self, input_id_header):
        self.wait_for_element_visible((By.XPATH, input_id_header))

    ##############################################################################
    inventory_button = "//div[@id='anor390-navbar_item-items']/a"

    def fill_form(self, inventory_button):
        self.click((By.XPATH, inventory_button))

    ##############################################################################
    total_amount = "//div[@class='tbl-row ng-scope']/div[10]"
    quantity = "//div[@class='tbl-row ng-scope']/div[8]"

    def get_elements(self):
        total_amount = self.check_count(self.total_amount)
        quantity = self.check_count(self.quantity)
        return {
            'start_total_amount': total_amount,
            'quantity': quantity,
        }

    ##############################################################################