from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class PaymentTypeListAttach(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    checkbox_all = (By.XPATH, '(//b-grid[@name="table"]//label)[1]')
    attach_button = (By.XPATH, '//button[@ng-click="attachMany()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_checkbox_all(self):
        self.click(self.checkbox_all)
        self.click(self.attach_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
