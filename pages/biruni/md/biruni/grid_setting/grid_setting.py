from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class GridSetting(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    group_button = (By.XPATH, '//b-grid-controller[@name="table"]//div[@role="group"]/button')
    grid_setting_button = (By.XPATH, '//b-grid-controller[@name="table"]//div[@role="group"]/div/a[@ng-click="openGridSetting()"]')

    def click_group_button(self):
        self.click(self.group_button)
        self.click(self.grid_setting_button)
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="save()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------

    def click_options_button(self, option_name):
        option = (By.XPATH, f'//ul[contains(@class, "ui-sortable")]/li[@id="{option_name}"]/div')
        self.click(option)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
    save_default_button = (By.XPATH, '//button[@ng-click="saveDefault()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_save_default_button(self):
        self.click(self.save_default_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------

    def click_search_type_switch(self, search_type):
        locator = (By.XPATH, f'//input[@ng-model="d.search"]/following-sibling::span[contains(text(),"{search_type}")]/../input')
        self.click_checkbox(locator)
    # ------------------------------------------------------------------------------------------------------------------
