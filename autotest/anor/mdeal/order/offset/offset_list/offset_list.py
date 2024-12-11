from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class OffsetList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="selectOffsetType()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, client_name):
        self.find_row_and_click(element_name=client_name)
    # ------------------------------------------------------------------------------------------------------------------
    detail_button = (By.XPATH, '//button[@ng-click="offsetDetails(row)"]')

    def click_detail_button(self):
        self.click(self.detail_button)
    # ------------------------------------------------------------------------------------------------------------------
    post_button = (By.XPATH, '//button[@ng-click="postOne(row)"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_post_button(self):
        self.click(self.post_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
