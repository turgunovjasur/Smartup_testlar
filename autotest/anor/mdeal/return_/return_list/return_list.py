from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ReturnList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    return_header = (By.XPATH, '//button[@ng-if="q.sc.first"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.return_header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-if="q.sc.first"]')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, client_name):
        self.find_row_and_click(element_name=client_name)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, "//button[@ng-click='view(row)']")

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    draft_one_button = (By.XPATH, "//button[@ng-click='draftOne(row)']")
    yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_draft_one_button(self):
        self.click(self.draft_one_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    delete_one_button = (By.XPATH, "//button[@ng-click='deleteOne(row)']")

    def click_delete_one_button(self):
        self.click(self.delete_one_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    archive_one_button = (By.XPATH, '//button[@ng-click="archiveOne(row)"]')

    def click_archive_one_button(self):
        self.click(self.archive_one_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    shipped_one_button = (By.XPATH, '//button[@ng-click="shippedOne(row)"]')

    def click_shipped_one_button(self):
        self.click(self.shipped_one_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
