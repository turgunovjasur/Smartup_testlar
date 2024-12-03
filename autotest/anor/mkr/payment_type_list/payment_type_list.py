from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class PaymentTypeList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="fi.open_attach()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    attach_button = (By.XPATH, '//button[@ng-click="fi.open_attach()"]')

    def click_attach_button(self):
        self.click(self.attach_button)
    # ------------------------------------------------------------------------------------------------------------------
