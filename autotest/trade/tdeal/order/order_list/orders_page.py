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
        if self.get_element(self.count_info):
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

    def find_row(self, client_name):
        self.find_row_and_click(element_name=client_name)
    # -----------------------------------------------------------------------------------------------------------------
    change_status_one_button = (By.XPATH, "//button[@id='trade81-button-change_status_one']")
    yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_change_status_button(self, status_name):
        self.click(self.change_status_one_button)
        status_button = (By.XPATH, f"//button[@id='trade81-button-change_status_one']/following-sibling::div/a[contains(text(), '{status_name}')]")
        self.click(status_button)
        self.click(self.yes_button)
    # -----------------------------------------------------------------------------------------------------------------
