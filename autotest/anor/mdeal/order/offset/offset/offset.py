from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class Offset(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    check_row = ("//div[contains(@class, 'tbl')]//div[contains(@class, 'tbl-row')]"
                 "//div[contains(@class, 'tbl-cell')]//label[normalize-space(text())='{client_name}']"
                 "/ancestor::div[@class='tbl-cell']/following-sibling::div[9]//button")

    def find_row(self, client_name):
        locator = (By.XPATH, self.check_row.replace('{client_name}', client_name))
        return self.click(locator)
    # ------------------------------------------------------------------------------------------------------------------
    get_balance = ("//div[contains(@class, 'tbl-cell')]//label[normalize-space(text())='{client_name}']"
                   "/ancestor::div[@class='tbl-cell']/following-sibling::div[5]/div")

    def check_balance(self, client_name):
        locator = (By.XPATH, self.get_balance.replace('{client_name}', client_name))
        return self.get_numeric_value(locator)
    # ------------------------------------------------------------------------------------------------------------------
    get_balance_payment = ("//div[contains(@class, 'tbl-cell')]//label[normalize-space(text())='{client_name}']"
                   "/ancestor::div[@class='tbl-cell']/following-sibling::div[7]/div")

    def check_balance_payment(self, client_name):
        locator = (By.XPATH, self.get_balance_payment.replace('{client_name}', client_name))
        return self.get_numeric_value(locator)
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
    cashboxes_locator = (
        By.XPATH, '//b-input[@name="cashboxes"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_cashboxes(self, cash_register_name):
        self.click_options(self.cashboxes_input, self.cashboxes_locator, cash_register_name)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
