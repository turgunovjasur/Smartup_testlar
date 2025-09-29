from selenium.webdriver.common.by import By
from pages.core.md.base_page import BasePage


class InputView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//h5/t[contains(text(),'Основная информация')]")

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    get_input_number = (By.XPATH, '//div[@id="anor390-navbar-header-information"]//t[@p1="d.input_number"]')

    def check_input_number(self):
        return self.get_numeric_value(self.get_input_number)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
