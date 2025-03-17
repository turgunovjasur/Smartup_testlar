from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class LicenseUserList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-class="q.classAttach"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)

    # ------------------------------------------------------------------------------------------------------------------
    all_checkbox = (By.XPATH, '//b-grid[@name="table"]//div[@class="tbl-header"]//input/following-sibling::span')
    detach_checked_button = (By.XPATH, '//button[@ng-click="detachChecked()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_all_checkbox(self):
        element = self._wait_for_presence(self.all_checkbox)
        self._click_js(element, self.all_checkbox)
        self.click(self.detach_checked_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    detach_button = (By.XPATH, '//button[@ng-class="q.classDetach"]')

    def click_detach_button(self):
        self.click(self.detach_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Available users:
    # ------------------------------------------------------------------------------------------------------------------
    header_attach_button = (By.XPATH, '//button[@ng-class="q.classAttach"]')

    def attach_button_visible(self):
        return self.wait_for_element_visible(self.header_attach_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, natural_person_name):
        self.find_row_and_click(element_name=natural_person_name)
    # ------------------------------------------------------------------------------------------------------------------
    attach_button = (By.XPATH, '//button[@ng-click="attach(row)"]')

    def click_attach_button(self):
        self.click(self.attach_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
