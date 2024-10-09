from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class InputId(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    input_id_header = (By.XPATH, "//h5/t[contains(text(),'Основная информация')]")

    def element_visible(self):
        self.wait_for_element_visible(self.input_id_header)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_button = (By.XPATH, "//div[@id='anor390-navbar_item-items']/a")

    def fill_form(self):
        self.click(self.inventory_button)
    # ------------------------------------------------------------------------------------------------------------------
    total_amount = (By.XPATH, "//div[@class='tbl-row ng-scope']/div[10]")
    quantity = (By.XPATH, "//div[@class='tbl-row ng-scope']/div[8]")

    def get_elements(self):
        self.check_count(self.total_amount)
        self.check_count(self.quantity)
    # ------------------------------------------------------------------------------------------------------------------
