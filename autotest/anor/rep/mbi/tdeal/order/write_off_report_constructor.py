import time
from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class WriteOffReportConstructor(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="view()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    search_value_input = (By.XPATH, '//input[@ng-model="q.search_value"]')

    def input_search_option(self, option_name):
        self.input_text(self.search_value_input, option_name)
        time.sleep(1)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, '//button[@ng-click="viewReport()"]')

    def click_view_button(self):
        time.sleep(1)
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
    iframe = (By.XPATH, '//iframe[@class="report-frame"]')

    def switch_to_iframe(self, exit_iframe=False):
        if exit_iframe:
            self.driver.switch_to.default_content()
            self.logger.info("Default content (asosiy sahifa) ga qaytildi.")
        else:
            try:
                iframe = self.wait_for_element(self.iframe, wait_type="presence")
                self.driver.switch_to.frame(iframe)
                self.logger.info("Iframe ichiga o'tildi.")
            except Exception as e:
                self.logger.error(f"Iframe switch xatosi: {e}")
                raise
    # ------------------------------------------------------------------------------------------------------------------

    def get_value_by_option_name(self, option_name):
        # 1. Headerlar ro'yxatini kutamiz
        headers_locator = (By.XPATH, '//div[@id="report-content"]//table//tr[1]/td')
        headers = self._wait_for_presence_all(headers_locator, visible_only=True)

        # 2. option_name ustunini topamiz
        column_index = None
        for index, element in enumerate(headers, start=1):
            if option_name in element.text:
                column_index = index
                break

        if column_index is None:
            raise ValueError(f"'{option_name}' title topilmadi.")

        # 3. Topilgan index asosida qiymat XPath yasaymiz
        value_locator = (By.XPATH, f"//div[@id='report-content']//table//tr[2]/td[{column_index}]")

        # 4. Matnni get_text orqali olamiz (retry bilan)
        return self.get_text(value_locator)
    # ------------------------------------------------------------------------------------------------------------------