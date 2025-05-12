import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class IntegrationThree(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-class="q.classSettings"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    show_setting_button = (By.XPATH, '//button[@ng-class="q.classSettings"]')

    def click_show_setting(self):
        self.click(self.show_setting_button)
    # ------------------------------------------------------------------------------------------------------------------
    date_input = (By.XPATH, '//input[@ng-model="d.begin_date"]')
    input_option = (By.XPATH, '//input[@ng-model="d.begin_date"]/parent::div/div')

    def input_date(self):
        one_month_ago = datetime.now() - relativedelta(months=1)
        date = one_month_ago.strftime("%d.%m.%Y")
        self.input_text(self.date_input, date)
        self._check_dropdown_closed(self.input_option)
    # ------------------------------------------------------------------------------------------------------------------
    generate_button = (By.XPATH, '//button[contains(@ng-click,"run") and @class="btn btn-primary"]')

    def click_generate(self):
        self._wait_for_all_loaders(log_text='click_generate')
        self.click(self.generate_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Generate
    # ------------------------------------------------------------------------------------------------------------------

    def check_report_document(self, document):
        click_sheet = (By.XPATH, f'//div[@id="report-sheets"]//a[@data-target="#sheet{document}"]')
        self.click(click_sheet)
        time.sleep(1)
        sheet = (By.XPATH, f'//div[@id="sheet{document}"]')
        return self.wait_for_element_visible(sheet)
    # ------------------------------------------------------------------------------------------------------------------
    iframe = (By.XPATH, '//iframe[@class="report-frame"]')

    def switch_to_iframe(self, exit_iframe=False):
        if exit_iframe:
            self.driver.switch_to.default_content()
            self.logger.info("➡️ Default content (asosiy sahifa) ga qaytildi.")
        else:
            try:
                iframe = self.wait_for_element(self.iframe, wait_type="presence")
                self.driver.switch_to.frame(iframe)
                self.logger.info("✅ Iframe ichiga o'tildi.")
            except Exception as e:
                self.logger.error(f"❌ Iframe switch xatosi: {e}")
                raise
    # ------------------------------------------------------------------------------------------------------------------
    # Setting
    # ------------------------------------------------------------------------------------------------------------------
    header_setting = (By.XPATH, '//button[@ng-click="saveSettings()"]')

    def element_visible_setting(self):
        return self.wait_for_element_visible(self.header_setting)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="saveSettings()"]')

    def click_save(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
