from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class GridSetting(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header_save = (By.XPATH, '//button[@ng-click="save()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header_save)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    save_default_button = (By.XPATH, '//button[@ng-click="saveDefault()"]')
    yes_default_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_save_default_button(self):
        self.click(self.save_default_button)
        self.click(self.yes_default_button)
    # ------------------------------------------------------------------------------------------------------------------
