from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.exception import ElementVisibilityError


class LicenseUserList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    # attach user
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-class="q.classAttach"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    all_checkbox = (By.XPATH, '//b-grid[@name="table"]//div[@class="tbl-header"]//input/following-sibling::span')

    def click_all_checkbox(self):
        element = self.wait_for_element(self.all_checkbox, wait_type="presence")
        self._click(element, self.all_checkbox, _click_js=True)
    # ------------------------------------------------------------------------------------------------------------------
    detach_checked_button = (By.XPATH, '//button[@ng-click="detachChecked()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_detach_checked_button(self):
        self.click(self.detach_checked_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    row_no_data = (By.XPATH, '//b-grid[@name="table"]//div[@class="tbl-body"]/div[contains(@class,"no-data")]')

    def get_row_no_data(self):
        try:
            self.wait_for_element(self.row_no_data, wait_type="visibility", timeout=5)
            self.logger.warning(f"No data in table")
            return True
        except ElementVisibilityError:
            return False
    # ------------------------------------------------------------------------------------------------------------------
    detach_button = (By.XPATH, '//button[@ng-class="q.classDetach"]')

    def click_detach_button(self):
        self.click(self.detach_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Available users:
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, natural_person_name):
        row_locator = f"(//div[contains(@class, 'tbl-row')]//div[contains(@class, 'tbl-cell') and contains(.,'{natural_person_name}')])[last()]"
        limit_locator = f'(//button[@class="btn btn-default rounded-0 ng-binding"])[last()]'
        limit_option_locator = f'(//button[@class="btn btn-default rounded-0 ng-binding"]/following-sibling::div/a[4])[last()]'

        self.find_row_and_click(element_name=natural_person_name,
                                xpath_pattern=row_locator,
                                limit_pattern=limit_locator,
                                limit_option_pattern=limit_option_locator)
    # ------------------------------------------------------------------------------------------------------------------
    attach_button = (By.XPATH, '//button[@ng-click="attach(row)"]')

    def click_attach_button(self):
        self.click(self.attach_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
