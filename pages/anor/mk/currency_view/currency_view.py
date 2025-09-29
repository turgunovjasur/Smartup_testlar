from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta


class CurrencyView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//div[@class='card-title']/h5/t")

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def click_navbar_button(self, navbar_button):
        navbar = (By.XPATH, f"(//div[contains(@class,'navi navi-bolder')]//div[contains(@class,'navi-item')]/a)[{navbar_button}]")
        self.click(navbar)
    # ------------------------------------------------------------------------------------------------------------------
    add_rate_button = (By.XPATH, '//button[@ng-click="openAddRate()"]')

    def click_add_rate_button(self):
        self.click(self.add_rate_button)
    # ------------------------------------------------------------------------------------------------------------------
    exchange_rate_input = (By.XPATH, '//div[@class="modal-content"]//div[@class="form-group"]/input[@ng-model="p.data.rate"]')

    def input_exchange_rate_button(self, exchange_rate):
        self.input_text(self.exchange_rate_input, exchange_rate)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
    get_row = (By.XPATH, '//div[@class="tbl"]//div[@class="tbl-row"]')

    def check_row(self):
        return self.wait_for_element_visible(self.get_row)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
