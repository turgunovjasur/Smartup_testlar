from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class OrderCopyModal(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    copy_title = (By.XPATH, "//h4/t[contains(text(), 'Копировать заказ')]")

    def element_visible_copy_title(self):
        self.wait_for_element_visible(self.copy_title)
    # ------------------------------------------------------------------------------------------------------------------
    clear_button = (By.XPATH, '//b-input[@name="persons"]//span[@class="clear-button"]')
    persons_input = (By.XPATH, '//b-input[@name="persons"]//input[@ng-model="_$bInput.searchValue"]')
    options_persons = (By.XPATH, '//b-input[@name="persons"]//div[contains(@class,"hint")]//div[contains(@class,"hint-item")]/div')

    def input_persons(self, client_name):
        self.click(self.clear_button)
        self.click_options(self.persons_input, self.options_persons, client_name)
    # ------------------------------------------------------------------------------------------------------------------
    copy_save_button = (By.XPATH, '//button[@ng-click="copy()"]')

    def click_copy_save_button(self):
        self.click(self.copy_save_button)
    # ------------------------------------------------------------------------------------------------------------------