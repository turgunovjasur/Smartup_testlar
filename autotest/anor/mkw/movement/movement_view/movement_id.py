from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class MovementId(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    card_title_header = "//div[@id='anor374-card_title-main']"

    def element_visible(self, card_title_header):
        self.wait_for_element_visible((By.XPATH, card_title_header))
    # ------------------------------------------------------------------------------------------------------------------
    movement_number = (By.XPATH, "//span[@id='anor374-span-movement_number']/t")
    # movement_number = (By.XPATH, "//span[@id='anor374-span-movement_number']/t[contains(text(), '№')]")

    def check_number(self):
        return self.get_numeric_value(self.movement_number)

    # ------------------------------------------------------------------------------------------------------------------
    navi_inventory_button = "//t[contains(text(), 'ТМЦ')]"

    def fill_form(self, navi_inventory_button):
        self.click((By.XPATH, navi_inventory_button))
    # ------------------------------------------------------------------------------------------------------------------
