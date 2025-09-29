from selenium.webdriver.common.by import By
from pages.core.md.base_page import BasePage


class Offset(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, client_name):
        check_row = (By.XPATH, f"//div[contains(@class, 'tbl')]//div[contains(@class, 'tbl-row')]//div[contains(@class, 'tbl-cell')]//label[normalize-space(text())='{client_name}']/ancestor::div[@class='tbl-cell']/following-sibling::div[9]//button")
        self.click(check_row)
    # ------------------------------------------------------------------------------------------------------------------

    def check_balance(self, client_name):
        get_balance = (By.XPATH, f"//div[contains(@class, 'tbl-cell')]//label[normalize-space(text())='{client_name}']/ancestor::div[@class='tbl-cell']/following-sibling::div[5]/div")
        return self.get_numeric_value(get_balance)
    # ------------------------------------------------------------------------------------------------------------------

    def check_balance_payment(self, client_name):
        get_balance_payment = (By.XPATH, f"//div[contains(@class, 'tbl-cell')]//label[normalize-space(text())='{client_name}']""/ancestor::div[@class='tbl-cell']/following-sibling::div[7]/div")
        return self.get_numeric_value(get_balance_payment)
    # ------------------------------------------------------------------------------------------------------------------
    post_button = (By.XPATH, '//button[@ng-click="post()"]')

    def click_post_button(self):
        self.click(self.post_button)
    # ------------------------------------------------------------------------------------------------------------------
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_yes_button(self):
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    cashboxes_input = (By.XPATH, '//b-input[@name="cashboxes"]//input')
    cashboxes_locator = (By.XPATH, '//b-input[@name="cashboxes"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_cashboxes(self, cash_register_name):
        self.click_options(self.cashboxes_input, self.cashboxes_locator, cash_register_name)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
