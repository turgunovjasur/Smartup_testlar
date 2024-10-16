import time
from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class OrdersPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    order_page_header = (By.XPATH, "//ul/li/a[contains(text(), 'Опросники')]")

    def element_visible(self):
        assert "Опросники" in self.get_text(self.order_page_header), "'order_page' page did not open!"
    # ------------------------------------------------------------------------------------------------------------------
    count_number = (By.XPATH, "//div[@id='trade81-sg_header-info']//div[@class='sg-sub-row ng-scope']/div[1]")
    count_info = (By.XPATH, "//div[@id='trade81-sg_header-info']")

    def check_order(self):
        if self.find_element(self.count_info, timeout=2):
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
    list_first_elem = (By.XPATH, "(//div[@class='tbl-row']/div[2])[1]")

    def click_first_elem_button(self):
        time.sleep(2)
        self.click(self.list_first_elem)
    # ------------------------------------------------------------------------------------------------------------------
    # change_status_one
    # -----------------------------------------------------------------------------------------------------------------
    change_status_one_button = (By.XPATH, "//button[@id='trade81-button-change_status_one']")
    status_button_6 = (By.XPATH, "//button[@id='trade81-button-change_status_one']/following-sibling::div/a[6]")
    status_button_7 = (By.XPATH, "//button[@id='trade81-button-change_status_one']/following-sibling::div/a[7]")
    yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_change_status_one_button(self, index=None):
        self.click(self.change_status_one_button)
        if index is None or index == 6:
            self.click(self.status_button_6)
        elif index == 7:
            self.click(self.status_button_7)
        else:
            raise ValueError("Error index. Only 6 or 7 button allowed.")
        self.click(self.yes_button)
    # -----------------------------------------------------------------------------------------------------------------
