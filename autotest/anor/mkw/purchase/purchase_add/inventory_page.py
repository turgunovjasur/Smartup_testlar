import time

from selenium.webdriver.common.by import By

from autotest.core.md.base_page import BasePage


class InventoryPage(BasePage):
    ##############################################################################
    inventory_page_header_xpath = "//div/descendant::div/h3/t[contains(text(), 'Основное')]"

    def element_visible(self, inventory_page_header_xpath):
        self.wait_for_element_visible((By.XPATH, inventory_page_header_xpath))

    ##############################################################################
    inventory_input = "//b-input[@id= 'anor289-input-binput-fastsearchquery-G-0']/descendant::input[@placeholder= 'Поиск...']"
    inventory = "//div[@class= 'tbl-cell']/b-input[@id= 'anor289-input-binput-fastsearchquery-G-0']/descendant::div[@class= 'hint-body ng-scope']/div[1]"
    # inventory = "Mis Nat Candy Gold"

    qty_input = "//input[@id= 'anor289-input-text-quantity-G-0']"
    qty = "10"

    price_input = "//input[@id= 'anor289-input-text-price-G-0']"
    price = "120000"

    def fill_form(self, inventory_input, inventory, qty_input, qty, price_input, price):
        time.sleep(1)

        self.input_text_elem((By.XPATH, inventory_input), (By.XPATH, inventory))
        time.sleep(1)

        self.input_text((By.XPATH, qty_input), (By.XPATH, qty))
        self.input_text((By.XPATH, price_input), (By.XPATH, price))

    ##############################################################################
    inventory_page_next_button_xpath = "//div[@id= 'anor289-wizard-finishing']"

    def click_button(self, inventory_page_next_button_xpath):
        self.wait_and_click((By.XPATH, inventory_page_next_button_xpath))
    ##############################################################################
