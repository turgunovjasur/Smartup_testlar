from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class MovementList(BasePage):
    ##############################################################################
    movement_list_header = "//button[@id='anor132-button-add']"

    def element_visible(self, movement_list_header):
        self.wait_for_element_visible((By.XPATH, movement_list_header))

    ##############################################################################
    create_button = "//button[@id='anor132-button-add']"

    def click_button(self, create_button):
        self.click((By.XPATH, create_button))

    ##############################################################################
    movement_list_first = '(//div[@class="tbl-row"]/div[2])[1]'
    view_button = '//button[contains(text(), "Просмотр")]'

    def fill_form(self, movement_list_first, view_button):
        self.click((By.XPATH, movement_list_first))
        self.click((By.XPATH, view_button))

    ##############################################################################