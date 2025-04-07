from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ExtraCostSharing(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    purchases_input = (By.XPATH, '//b-input[@name="purchases"]//input')
    purchases_options = (By.XPATH, '//b-input[@name="purchases"]//div[contains(@class,"hint-item")]/div[contains(@class,"form-row")]/div')

    def input_purchases(self, purchase_number):
        self.click_options(self.purchases_input, self.purchases_options, purchase_number)
    # ------------------------------------------------------------------------------------------------------------------
    select_items_button = (By.XPATH, '//b-pg-grid[@name="purchases"]//button[@ng-click="selectItems(purchase)"]')
    add_items_button = (By.XPATH, '//b-pg-grid[@name="purchase_items"]//button[@ng-click="addItem(item)"]')

    def click_select_items_button(self):
        self.click(self.select_items_button)
        self.click(self.add_items_button)
    # ------------------------------------------------------------------------------------------------------------------
    close_modal_button = (By.XPATH, '//form[@name="modal"]//button[@b-hotkey="close"]')

    def click_close_modal_button(self):
        self.click(self.close_modal_button)
    # ------------------------------------------------------------------------------------------------------------------
    separate_button = (By.XPATH, '//button[@ng-click="seperate()"]')

    def click_separate_button(self):
        self.click(self.separate_button)
    # ------------------------------------------------------------------------------------------------------------------
    post_button = (By.XPATH, '//button[@ng-click="post()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_post_button(self):
        self.click(self.post_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
