from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class PurchaseList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//button[@id='anor288-button-add']")

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, "//button[@id='anor288-button-add']")

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, '//button[@id="anor288-button-view"]')

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    post_button = (By.XPATH, '//button[@id="anor288-button-post"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_post_button(self):
        self.click(self.post_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    reload_button = (By.XPATH, '//button[@ng-click="reload()"]')

    def click_reload_button(self):
        self.click(self.reload_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, purchase_number):
        self.find_row_and_click(element_name=purchase_number)
    # ------------------------------------------------------------------------------------------------------------------
    # status_one_button = (By.XPATH, "//button[@id='anor288-button-changestatus']")
    status_one_button = (By.XPATH, '//div[@class="tbl-row open"]//div[@class="tbl-cell"]//div[@class="dropdown"]')

    # status_draft_button = (By.XPATH, "//div[@id='statusDropDown']//div[@class='card-body p-0']/a[1]")
    status_draft_button = (By.XPATH, f'//div[@id="dropdown" and @class="dropdown show"]//button[contains(@onclick,"Черновик")]')

    status_yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_status_one_button(self):
        self.click(self.status_one_button)
        self.click(self.status_draft_button)
        self.click(self.status_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    delete_one_button = (By.XPATH, "//button[@id='anor288-button-delete']")
    delete_yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_delete_one_button(self):
        self.click(self.delete_one_button)
        self.click(self.delete_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    # transaction
    # ------------------------------------------------------------------------------------------------------------------
    transactions_button = (By.XPATH, '//button[@id="anor288-button-transactions"]')

    def click_transactions_button(self):
        self.click(self.transactions_button)

    def check_transaction_body(self, timeout):
        report_body = (By.XPATH, '//div[@id="report-content"]')
        self.wait_for_element(report_body, timeout=timeout, wait_type='visibility', screenshot='purchase_transaction_not_open')
    # ------------------------------------------------------------------------------------------------------------------
    # report
    # ------------------------------------------------------------------------------------------------------------------
    report_button = (By.XPATH, '//button[@ng-click="openChat(row.purchase_id)"]/following-sibling::div/button')
    items_button = (By.XPATH, '//button[contains(@class,"btn btn-xs")]/following-sibling::span')

    def click_report_button(self):
        self.click(self.report_button)
        self.click(self.items_button)

    def get_extra_cost_total_amount_for_report(self, td=4):
        get_extra_cost_total_amount = (By.XPATH, f'//td[text()="Итог"]/following-sibling::td[{td}]')
        return self.get_numeric_value(get_extra_cost_total_amount)

    def get_extra_cost_amount_for_report(self, product_name, td=6):
        get_extra_cost = (By.XPATH, f'//td[text()="{product_name}"]/following-sibling::td[{td}]')
        return self.get_numeric_value(get_extra_cost)

    def check_report_body(self, timeout):
        report_body = (By.XPATH, '//div[@id="report-content"]')
        self.wait_for_element(report_body, timeout=timeout, wait_type='visibility', screenshot='purchase_report_not_open')
    # ------------------------------------------------------------------------------------------------------------------
