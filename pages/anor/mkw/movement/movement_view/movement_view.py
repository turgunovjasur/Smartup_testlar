from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class MovementView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//div[@id='anor374-card_title-main']")

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    get_movement_number = (By.XPATH, "//span[@id='anor374-span-movement_number']/t")

    def check_movement_number(self):
        return self.get_numeric_value(self.get_movement_number)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------