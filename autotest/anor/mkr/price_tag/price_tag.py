from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class PriceTag(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="run()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    product_name_input = (By.XPATH, '//b-input[@name="products"]//input[@ng-model="row.product_name"]')
    product_options = (By.XPATH, '//b-input[@name="products"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')


    def input_product_name(self, product_name):
        self.click_options(self.product_name_input, self.product_options, product_name)
    # ------------------------------------------------------------------------------------------------------------------
    run_button = (By.XPATH, '//button[@ng-click="run()"]')

    def click_run_button(self):
        self.click(self.run_button)
    # ------------------------------------------------------------------------------------------------------------------

    def click_windows_enter(self):
        import pyautogui

        pyautogui.press('enter')
        self.logger.info("Fayl muvaffaqiyatli tanlandi!")
    # ------------------------------------------------------------------------------------------------------------------
