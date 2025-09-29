from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class Spot(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="selectSpotTemplate()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    template_button = (By.XPATH, '//button[@ng-click="selectSpotTemplate()"]')

    def click_template(self):
        self.click(self.template_button)
    # ------------------------------------------------------------------------------------------------------------------
    product_groups_input = (By.XPATH, '//b-input[@name="product_groups"]//input')
    product_groups_options = (By.XPATH, '//b-input[@name="product_groups"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_product_groups(self, product_group_name):
        self.click_options(self.product_groups_input, self.product_groups_options, product_group_name)
    # ------------------------------------------------------------------------------------------------------------------
    setting_button = (By.XPATH, '//button[@ng-click="setting()"]')

    def click_setting(self):
        self.click(self.setting_button)
    # ------------------------------------------------------------------------------------------------------------------
    preferences_clear_button = (By.XPATH, '//button[@ng-click="preferencesClear()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_preferences_clear(self):
        self.click(self.preferences_clear_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    run_button = (By.XPATH, '//button[@ng-click="run()"]')

    def click_run(self):
        self.click(self.run_button)
    # ------------------------------------------------------------------------------------------------------------------
