from selenium.webdriver.common.by import By

from autotest.core.md.base_page import BasePage


class InventoryPage(BasePage):
    ##############################################################################
    inventory_page_header_xpath = ""

    def element_visible(self, inventory_page_header_xpath):
        self.wait_for_element_visible((By.XPATH, inventory_page_header_xpath))

    ##############################################################################
    inventory = "(//div[@class= 'tbl-cell']//div[@class= 'simple']/input)[1]"
    inventory_elem_xpath = "//div[contains(text(), 'un / Greenwhite solutions / Узбекистан')]"

    def fill_form(self, inventory, inventory_elem_xpath):
        self.input_text_elem((By.XPATH, inventory), (By.XPATH, inventory_elem_xpath))

    ##############################################################################
    inventory_page_next_button_xpath = ""

    def click_button(self, inventory_page_next_button_xpath):
        self.wait_and_click((By.XPATH, inventory_page_next_button_xpath))
    ##############################################################################
