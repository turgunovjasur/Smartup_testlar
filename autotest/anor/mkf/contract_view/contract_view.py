from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class ContractView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    get_contract_name = (By.XPATH, '//div[@class="b-offcanvas-hide mt-4"]/span[1]')

    def check_contract_name(self):
        return self.get_text(self.get_contract_name)
    # ------------------------------------------------------------------------------------------------------------------
    get_currency_name = (By.XPATH, "//div[contains(@class,'col-sm-12')]/label/t[contains(text(),'Валюта')]/ancestor::label/following-sibling::span")

    def check_currency_name(self):
        return self.get_text(self.get_currency_name)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
