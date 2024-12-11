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
    post_button = (By.XPATH, '//button[@ng-click="post()"]')

    def click_post_button(self):
        self.click(self.post_button)
    # ------------------------------------------------------------------------------------------------------------------
