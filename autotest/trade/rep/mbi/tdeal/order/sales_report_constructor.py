import time
from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class SalesReportConstructor(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="view()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    search_value_input = (By.XPATH, '//input[@ng-model="q.search_value"]')

    def input_search_value(self, value_name):
        self.input_text(self.search_value_input, value_name)
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
