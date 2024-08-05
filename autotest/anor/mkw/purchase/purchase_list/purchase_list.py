from autotest.core.md.base_page import BasePage

from selenium.webdriver.common.by import By


class PurchaseList(BasePage):
    ##############################################################################
    purchase_list_header_xpath = "//div/ul/li/a[contains(text(), 'Поступления ТМЦ на склад')]"

    def element_visible(self, purchase_list_header_xpath):
        self.wait_for_element_visible((By.XPATH, purchase_list_header_xpath))

    ##############################################################################
    create_button_xpath = "//div/button[contains(text(), 'Создать')]"

    def click_button(self, create_button_xpath):
        self.wait_and_click((By.XPATH, create_button_xpath))
    ##############################################################################
