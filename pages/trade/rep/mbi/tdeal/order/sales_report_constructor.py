import time
from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class SalesReportConstructor(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="view()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    search_value_input = (By.XPATH, '//input[@ng-model="q.search_value"]')

    def input_search_option(self, option_name):
        self.input_text(self.search_value_input, option_name)
        time.sleep(2)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, '//button[@ng-click="view()"]')

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------

    def click_source_and_target(self, option_name, field_name):
        source = (By.XPATH, f'//ul[@ng-model="d.fields"]/li//span[contains(text(),"{option_name}")]/..')

        fields = {
            "row": "rowOpts",
            "col": "colOpts",
            "filter": "filterOpts",
            "value": "valueOpts",
        }
        if field_name not in fields:
            raise ValueError(f"Noto'g'ri field_name: '{field_name}'. Ruxsat etilgan qiymatlar: {list(fields.keys())}")

        target = (By.XPATH, f'//ul[@ui-sortable="{fields[field_name]}"]')
        self.click_drag_and_drop(source=source, target=target)
    # ------------------------------------------------------------------------------------------------------------------

    def input_filter_fields(self, option_name, clear=False):
        if clear:
            clear_locator = (By.XPATH, f'//b-input/ancestor::li//span[contains(text(),"{option_name}")]/ancestor::li//span[@class="clear-button"]')
            self.click(clear_locator)
        # input_locator = (By.XPATH, f'//b-input/ancestor::li//span[contains(text(),"{option_name}")]/ancestor::li//input')
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
    report_content = (By.XPATH, '//div[@id="report-content"]//td[@class="bsr-2"]')

    def get_order_id_list(self):
        """Report ichidagi barcha order ID larni matn sifatida ro'yxatga qaytaradi."""
        elements = self._wait_for_presence_all(self.report_content)
        order_ids = []

        for element in elements:
            text = element.text.strip()
            if text:
                order_ids.append(text)

        return order_ids
    # ------------------------------------------------------------------------------------------------------------------