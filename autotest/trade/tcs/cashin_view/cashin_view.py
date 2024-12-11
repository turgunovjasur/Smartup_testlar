from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class CashinView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    get_cashin_number = (By.XPATH, '//div[@class="b-offcanvas-hide"]/span[1]')

    def check_cashin_number(self):
        return self.get_numeric_value(self.get_cashin_number)
    # ------------------------------------------------------------------------------------------------------------------
    get_client_name = (By.XPATH, '//div[@class="form-group"]/label/t[normalize-space(text())="Клиент"]'
                                 '/ancestor::label/following-sibling::span')

    def check_client_name(self):
        return self.get_text(self.get_client_name)
    # ------------------------------------------------------------------------------------------------------------------
    get_total_price = (By.XPATH, '//div[@class="col-sm"]/label/t[normalize-space(text())="Сумма"]'
                                 '/ancestor::label/following-sibling::span')

    def check_total_price(self):
        return self.get_numeric_value(self.get_total_price)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
