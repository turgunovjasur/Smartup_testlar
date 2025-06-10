from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.exception import ElementVisibilityError


class OrdersList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@id="trade81-button-add"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, "//button[@id='trade81-button-add']")

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, "//button[@id='trade81-button-view']")

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    view_dropdown = (By.XPATH, '//button[@id="trade81-button-view"]/following-sibling::button')

    def click_view_dropdown(self, file_name):
        """file_name = ['Файлы', 'Проводки']"""
        self.click(self.view_dropdown)
        dropdown = (By.XPATH, f'//button[@id="trade81-button-view"]/following-sibling::div/a[contains(text(),"{file_name}")]')
        self.click(dropdown)
    # ------------------------------------------------------------------------------------------------------------------
    edit_button = (By.XPATH, '//button[@id="trade81-button-edit"]')

    def click_edit_button(self):
        self.click(self.edit_button)
    # ------------------------------------------------------------------------------------------------------------------
    edit_dropdown = (By.XPATH, '//button[@id="trade81-button-edit"]/following-sibling::button')

    def click_edit_dropdown(self, file_name):
        """file_name = ['Прикрепить', 'Настройки типа цены', 'Настройка брони']"""
        self.click(self.edit_dropdown)
        dropdown = (By.XPATH, f'//button[@id="trade81-button-edit"]/following-sibling::div/a[contains(text(),"{file_name}")]')
        self.click(dropdown)
    # ------------------------------------------------------------------------------------------------------------------
    copy_button = (By.XPATH, '//button[@id="trade81-button-show_copy_modal"]')

    def click_copy_button(self):
        self.click(self.copy_button)
    # ------------------------------------------------------------------------------------------------------------------
    report_one_button = (By.XPATH, '//button[@id="trade81-button-report_one"]')
    options_report_one = (By.XPATH, '//button[@id="trade81-button-report_one"]/following-sibling::ul/li/a/span')

    def click_report_one_button(self, report_name):
        self.click_options(self.report_one_button, self.options_report_one, report_name)
    # ------------------------------------------------------------------------------------------------------------------

    def click_reports_all_button(self, report_name, all_button=False):
        if all_button:
            self.click(self.report_one_button)
        options = (By.XPATH, f'//button[@id="trade81-button-report_one"]/following-sibling::ul/li//*[self::span or self::t][contains(text(),"{report_name}")]')
        self.click(options)
    # ------------------------------------------------------------------------------------------------------------------
    invoice_report_one_button = (By.XPATH, '//div[@class="tbl-row-action"]//button/t[contains(text(),"Счет-фактуры")]')

    def click_invoice_reports_all_button(self, invoice_report_name):
        self.click(self.invoice_report_one_button)
        options = (By.XPATH, f'//span[contains(text(),"{invoice_report_name}")]/preceding-sibling::button[contains(@ng-click,"invoiceOne")]')
        self.click(options)
    # ------------------------------------------------------------------------------------------------------------------
    return_button = (By.XPATH, '//button[@id="trade81-button-edit"]')

    def click_return_button(self):
        self.click(self.return_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, client_name):
        self.find_row_and_click(element_name=client_name)
    # ------------------------------------------------------------------------------------------------------------------

    def check_header_option(self, option_name):
        try:
            option = (By.XPATH, f'//div[contains(@class, "tbl-header")]//div[@sort-header="{option_name}"]')
            element = self.wait_for_element(option, wait_type="visibility")
            self.logger.info(f'Header option appeared: {option_name}!')
            return element

        except ElementVisibilityError as e:
            raise AssertionError(f'Header option not visible: {option_name}!') from e
    # ------------------------------------------------------------------------------------------------------------------
    reload_button = (By.XPATH, '//button[@ng-click="reload()"]')

    def click_reload_button(self):
        self.click(self.reload_button)
    # -----------------------------------------------------------------------------------------------------------------
    change_status_one_button = (By.XPATH, "//button[@id='trade81-button-change_status_one']")
    yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_change_status_button(self, status_name):
        self.click(self.change_status_one_button)
        status_button = (By.XPATH, f"//button[@id='trade81-button-change_status_one']/following-sibling::div/a[contains(text(), '{status_name}')]")
        self.click(status_button)
        self.click(self.yes_button)
    # -----------------------------------------------------------------------------------------------------------------
    # Modal Copy
    # ------------------------------------------------------------------------------------------------------------------
    copy_title = (By.XPATH, "//h4/t[contains(text(), 'Копировать заказ')]")

    def element_visible_copy_title(self):
        self.wait_for_element_visible(self.copy_title)
    # ------------------------------------------------------------------------------------------------------------------
    clear_button = (By.XPATH, '//b-input[@name="persons"]//span[@class="clear-button"]')

    persons_input = (By.XPATH, '//b-input[@name="persons"]//input[@ng-model="_$bInput.searchValue"]')
    options_persons = (By.XPATH, '//b-input[@name="persons"]//div[contains(@class,"hint")]//div[contains(@class,"hint-item")]/div')

    def input_persons(self, client_name):
        self.click(self.clear_button)
        self.click_options(self.persons_input, self.options_persons, client_name)
    # ------------------------------------------------------------------------------------------------------------------
    copy_save_button = (By.XPATH, '//button[@ng-click="copy()"]')

    def click_copy_save_button(self):
        self.click(self.copy_save_button)
    # ------------------------------------------------------------------------------------------------------------------
