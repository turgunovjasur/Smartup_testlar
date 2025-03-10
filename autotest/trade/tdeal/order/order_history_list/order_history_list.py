from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By

from utils.exception import LoaderTimeoutError


class OrdersHistoryList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//div[@class="dropdown cursor-pointer"]//span')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, client_name):
        self.find_row_and_click(element_name=client_name)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, "//button[@id='trade83-button-view']")

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    change_status_one_button = (By.XPATH, "//button[@id='trade83-button-change_status_one']")
    save_status_one_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_change_status_one_button(self):
        self.click(self.change_status_one_button)
        self.click(self.save_status_one_button)
    # -----------------------------------------------------------------------------------------------------------------
    return_button = (By.XPATH, "//button[@id='trade83-button-return_deal']")

    def click_return_button(self):
        self.click(self.return_button)
    # -----------------------------------------------------------------------------------------------------------------
    report_one_button = (By.XPATH, '//button[@id="trade83-button-report_one"]')
    options_report_one = (By.XPATH, '//button[@id="trade83-button-report_one"]/following-sibling::ul/li/a/span')

    def click_report_one_button(self, report_name):
        self.click_options(self.report_one_button, self.options_report_one, report_name)
    # ------------------------------------------------------------------------------------------------------------------

    def click_reports_all_button(self, report_name, all_button=False):
        if all_button:
            self.click(self.report_one_button)
        try:
            options = (By.XPATH, f'//button[@id="trade83-button-report_one"]/following-sibling::ul/li//*[self::span or self::t][contains(text(),"{report_name}")]')
            self.click(options)
        except LoaderTimeoutError:
            pass
    # -----------------------------------------------------------------------------------------------------------------
