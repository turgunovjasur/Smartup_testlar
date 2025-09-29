from selenium.webdriver.common.by import By
from pages.core.md.base_page import BasePage


class SupplierView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    get_name = (By.XPATH, '//div[@class="b-offcanvas-hide"]/span[1]')

    def check_supplier_name(self):
        return self.get_text(self.get_name)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
