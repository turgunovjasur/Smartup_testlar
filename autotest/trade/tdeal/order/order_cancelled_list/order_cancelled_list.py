import time

from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class OrderCancelledList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//ul/li/a/span[contains(text(), 'Главное')]")

    def element_visible(self):
        assert "Главное" in self.get_text(self.header), "'OrderCancelledList' page did not open!"
    # ------------------------------------------------------------------------------------------------------------------
    list_first_elem = (By.XPATH, "(//div[@class='tbl-row']/div[2])[1]")

    def click_first_elem_button(self):
        time.sleep(2)
        self.click(self.list_first_elem)
    # ------------------------------------------------------------------------------------------------------------------
    delete_one_button = (By.XPATH, "//button[@ng-click='deleteOne(row)']")
    yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_delete_one_button(self):
        self.click(self.delete_one_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
