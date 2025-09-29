from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


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
    # change_status_one_button = (By.XPATH, "//button[@id='trade81-button-change_status_one']")
    change_status_one_button = (By.XPATH, '//div[@class="tbl-row open"]//div[@class="tbl-cell"]//div[@class="dropdown"]')
    yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_change_status_button(self, status_name):
        self.click(self.change_status_one_button)
        # status_button = (By.XPATH, f"//button[@id='trade81-button-change_status_one']/following-sibling::div/a[contains(text(), '{status_name}')]")
        status_button = (By.XPATH, f'//div[@id="dropdown" and @class="dropdown show"]//button[contains(@onclick,"{status_name}")]')
        self.click(status_button)
        self.click(self.yes_button)

    # ==================================================================================================================
    # b-grid-controller

    search_input = (By.XPATH, '//b-grid-controller[@name="table"]//input')

    def input_search(self, search_data=None, clear=False):
        if clear:
            self.clear_element(self.search_input)
            return
        self.input_text(self.search_input, search_data)
    # ------------------------------------------------------------------------------------------------------------------
    reload_button = (By.XPATH, '//button[@ng-click="reload()"]')

    def click_reload_button(self):
        self.click(self.reload_button)
    # ------------------------------------------------------------------------------------------------------------------
    filter_panel_button = (By.XPATH, '//b-grid-controller//button[@ng-click="toggleFilterPanel()"]')

    def click_filter_panel_button(self):
        self.click(self.filter_panel_button)
    # ------------------------------------------------------------------------------------------------------------------

    def click_option_in_filter_panel(self, option_header, option_name, state):
        locator = (By.XPATH, f'//b-grid-filter-panel//span[contains(text(),"{option_header}")]//ancestor::div[@class="b-filter-item"]//div[@class="filter-body"]//span[contains(text(),"{option_name}")]/../input')
        self.click_checkbox(locator, state)
    # ------------------------------------------------------------------------------------------------------------------
    filter_run_button = (By.XPATH, '//div[@class="b-grid-filter-panel"]//button[@ng-click="a.bGridFilter.run()"]')

    def click_filter_run_button(self):
        self.click(self.filter_run_button)
    # ------------------------------------------------------------------------------------------------------------------
    show_all_button = (By.XPATH, '//div[@class="b-grid-filter-panel"]//button[@ng-click="a.bGridFilter.showAll()"]')

    def click_show_all_button(self):
        self.click(self.show_all_button)
    # ------------------------------------------------------------------------------------------------------------------
    close_filter_panel_button = (By.XPATH, '//b-grid-filter-panel//button[contains(@ng-click,"a.grid.g.openFilterPanel")]')

    def click_close_filter_panel(self):
        self.click(self.close_filter_panel_button)

    # b-grid-controller
    # ==================================================================================================================
