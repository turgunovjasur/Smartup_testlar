from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class MovementId(BasePage):
    ##############################################################################
    movement_id_header = "//div[@id='anor374-card_title-main']"

    def element_visible(self, movement_id_header):
        self.wait_for_element_visible((By.XPATH, movement_id_header))

    ##############################################################################
    number = "//span[@id='anor374-span-movement_number']"

    def get_elements(self):
        number = self.check_count(self.number)
        return {
            'number': number
        }

    ##############################################################################
    inventory_button_xpath = "//t[contains(text(), 'ТМЦ')]"

    def fill_form(self, inventory_button_xpath):
        self.click((By.XPATH, inventory_button_xpath))

    ##############################################################################