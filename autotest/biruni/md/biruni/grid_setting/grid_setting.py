from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class GridSetting(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="save()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------

    def click_options_button(self, option_name):
        option = (By.XPATH, f'//ul[contains(@class, "gs-extra-list ui-sortable")]/li[@id="{option_name}"]/div')
        self.click(option)
    # ------------------------------------------------------------------------------------------------------------------
