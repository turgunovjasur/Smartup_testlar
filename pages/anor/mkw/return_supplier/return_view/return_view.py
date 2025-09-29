from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ReturnView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------

    def get_input_value(self, input_name, clean=False):
        locator = (By.XPATH, f'//label/t[contains(text(),"{input_name}")]/../../span')
        return self.get_text(locator, clean=clean)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------