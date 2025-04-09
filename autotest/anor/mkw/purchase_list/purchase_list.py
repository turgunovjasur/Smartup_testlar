from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


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
    transactions_button = (By.XPATH, '//button[@id="anor288-button-transactions"]')

    def click_transactions_button(self):
        self.click(self.transactions_button)

    get_row = (By.XPATH, '(//td[@class="bsr-27" and @colspan="2"])[2]')

    def get_extra_cost_amount(self):
        return self.get_numeric_value(self.get_row)
    # ------------------------------------------------------------------------------------------------------------------
    post_button = (By.XPATH, '//button[@id="anor288-button-post"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_post_button(self):
        self.click(self.post_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    report_button = (By.XPATH, '//button[@ng-click="openChat(row.purchase_id)"]/following-sibling::div/button')
    items_button = (By.XPATH, '//button[contains(@class,"btn btn-xs")]/following-sibling::span')

    def click_report_button(self):
        self.click(self.report_button)
        self.click(self.items_button)

    get_extra_cost_report = (By.XPATH, '(//tr/td/following-sibling::td[@class="bsr-26"])[5]')

    def get_extra_cost_amount_for_report(self):
        return self.get_numeric_value(self.get_extra_cost_report)
    # ------------------------------------------------------------------------------------------------------------------
    reload_button = (By.XPATH, '//button[@ng-click="reload()"]')

    def click_reload_button(self):
        self.click(self.reload_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, purchase_number):
        self.find_row_and_click(element_name=purchase_number)
    # ------------------------------------------------------------------------------------------------------------------
    status_one_button = (By.XPATH, "//button[@id='anor288-button-changestatus']")
    status_draft_button = (By.XPATH, "//div[@id='statusDropDown']//div[@class='card-body p-0']/a[1]")
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
