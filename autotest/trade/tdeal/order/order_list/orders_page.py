import time

from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class OrdersList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@id="trade81-button-add"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    count_number = (By.XPATH, "//div[@id='trade81-sg_header-info']//div[@class='sg-sub-row ng-scope']/div[1]")
    count_info = (By.XPATH, "//div[@id='trade81-sg_header-info']")

    def check_order(self):
        if self.wait_for_element_visible(self.count_info):
            return self.get_numeric_value(self.count_number)
        else:
            return 0
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, "//button[@id='trade81-button-add']")

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, "//button[@id='trade81-button-view']")

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    edit_button = (By.XPATH, '//button[@id="trade81-button-edit"]')

    def click_edit_button(self):
        self.click(self.edit_button)
    # ------------------------------------------------------------------------------------------------------------------
    copy_button = (By.XPATH, '//button[@id="trade81-button-show_copy_modal"]')

    def click_copy_button(self):
        self.click(self.copy_button)
    # ------------------------------------------------------------------------------------------------------------------
    return_button = (By.XPATH, '//button[@id="trade81-button-edit"]')

    def click_return_button(self):
        self.click(self.return_button)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    copy_title = (By.XPATH, "//h4/t[contains(text(), 'Копировать заказ')]")

    def element_visible_copy_title(self):
        return self.wait_for_element_visible(self.copy_title)
    # ------------------------------------------------------------------------------------------------------------------
    persons_input = (By.XPATH, '//b-input[@name="persons"]//input[@ng-model="_$bInput.searchValue"]')
    clear_button = (By.XPATH, '//b-input[@name="persons"]//span[@class="clear-button"]')
    options_persons = (By.XPATH, '//b-input[@name="persons"]//div[contains(@class,"hint")]//div[contains(@class,"hint-item")]/div')

    def input_persons(self, client_name_A, client_name_B):
        self.click(self.clear_button)
        self.click_options(self.persons_input, self.options_persons, client_name_A)
        self.click_options(self.persons_input, self.options_persons, client_name_B)
    # ------------------------------------------------------------------------------------------------------------------
    copy_save_button = (By.XPATH, '//button[@ng-click="copy()"]')

    def click_copy_save_button(self):
        self.click(self.copy_save_button)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, client_name):
        self.find_row_and_click(element_name=client_name, checkbox=True)
    # ------------------------------------------------------------------------------------------------------------------
    reload_button = (By.XPATH, '//button[@ng-click="reload()"]')

    def click_reload_button(self):
        self.click(self.reload_button)
    # -----------------------------------------------------------------------------------------------------------------
    change_status_one_button = (By.XPATH, "//button[@id='trade81-button-change_status_one']")
    yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_change_status_button(self, status_name):
        self.click(self.change_status_one_button)
        status_button = (
            By.XPATH, f"//button[@id='trade81-button-change_status_one']/following-sibling::div/a[contains(text(), '{status_name}')]")
        self.click(status_button)
        self.click(self.yes_button)
    # -----------------------------------------------------------------------------------------------------------------
