from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class StocktakingSelect(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header_select = (By.XPATH, '//button[@ng-click="close()"]')

    def element_visible_select(self):
        self.wait_for_element_visible(self.header_select)
    # ------------------------------------------------------------------------------------------------------------------
    search_input = (By.XPATH, '//b-pg-controller[@name="items"]//input[@ng-model="g.searchValue"]')

    def input_search(self, product_name):
        self.input_text(self.search_input, product_name)
    # ------------------------------------------------------------------------------------------------------------------
    row_quant_input = (By.XPATH, '//b-pg-grid[@name="items"]//input[@ng-model="row.new_quant"]')

    def input_row_quant(self, product_row_quant):
        return self.input_text(self.row_quant_input, product_row_quant)
    # ------------------------------------------------------------------------------------------------------------------
    move_one_button = (By.XPATH, '//b-pg-grid[@name="items"]//button[contains(@ng-click,"moveOne")]')

    def click_move_one_button(self):
        self.click(self.move_one_button)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
    def get_value_by_column_name(self, column_name):
        headers_locator = (By.XPATH, '//b-pg-grid[@name="items"]//div[@class="tbl-header-cell"]')
        headers = self._wait_for_presence_all(headers_locator, visible_only=True)

        column_index = None
        for index, element in enumerate(headers, start=1):
            if column_name in element.text:
                column_index = index
                break

        if column_index is None:
            raise ValueError(f"'{column_name}' title topilmadi.")

        value_locator = (By.XPATH, f'//b-pg-grid[@name="items"]//div[contains(@class,"tbl-cell ng")][{column_index - 1}]')

        return self.get_text(value_locator)
    # ------------------------------------------------------------------------------------------------------------------
