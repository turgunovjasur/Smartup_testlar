import time
from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ReturnList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    return_header = (By.XPATH, "//ul/li/a[contains(text(), 'Причины возврата')]")

    def element_visible(self):
        assert "Причины возврата" in self.get_text(self.return_header), "'Return' page did not open!"
    # ------------------------------------------------------------------------------------------------------------------
    list_first_elem = (By.XPATH, "(//div[@class='tbl-row']/div[2])[1]")

    def click_first_elem_button(self):
        time.sleep(2)
        self.click(self.list_first_elem)
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
