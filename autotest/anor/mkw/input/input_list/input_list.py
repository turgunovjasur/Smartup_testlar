from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class InputList(BasePage):
    ##############################################################################
    input_list_header = "//div[@id='kt_content']/descendant::h6"

    def element_visible(self, input_list_header):
        self.wait_for_element_visible((By.XPATH, input_list_header))

    ##############################################################################
    create_button = "//button[@id='anor113-button-add']"

    def click_button(self, create_button):
        self.click((By.XPATH, create_button))

    ##############################################################################
    # Input_id
    ##############################################################################
    date_button = "//div[contains(text(), 'Время')]"
    first_element = "//div[@class='tbl-row'][1]/div[3]"
    view_button = "//button[@id='anor113-button-view']"

    def click_2x(self, date_button):
        self.click_multiple_time((By.XPATH, date_button), click_count=2, delay=1)

    def fill_form(self, first_element, view_button):
        self.click((By.XPATH, first_element))
        self.click((By.XPATH, view_button))

    ##############################################################################