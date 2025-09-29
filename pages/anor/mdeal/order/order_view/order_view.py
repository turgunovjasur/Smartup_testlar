from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta


class OrderView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//div[@class='card-title']/h5/t")

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------

    def get_input_value_in_order_view(self, input_name, data_type="text"):
        data_types = {
            "numeric": self.get_numeric_value,
            "text": self.get_text
        }
        if data_type not in data_types:
            raise ValueError(f"Incorrect data_type: {data_type}. Allowed values: 'numeric', 'text'")

        locator = (By.XPATH, f'//t[contains(text(),"{input_name}")]/../../span')
        return data_types[data_type](locator)
    # ------------------------------------------------------------------------------------------------------------------
    setting_button = (By.XPATH, '//b-pg-controller[@name="goods_items_view"]//div[@role="group"]/button')
    setting_tbl_button = (By.XPATH, '//b-pg-controller[@name="goods_items_view"]//div[@role="group"]/div[@x-placement="bottom-end"]/a')

    def click_setting_button(self):
        self.click(self.setting_button)
        self.click(self.setting_tbl_button)
    # ------------------------------------------------------------------------------------------------------------------
    get_product_total_quantity = (By.XPATH, "//b-pg-grid[@name='goods_items_view']/following-sibling::div//div[contains(@class, 'sg-cell') and t[text()='Общее кол-во']]")
    get_product_total_price = (By.XPATH, "//b-pg-grid[@name='goods_items_view']/following-sibling::div//div[contains(@class, 'sg-cell') and t[text()='Сумма']]")
    get_product_total_sum = (By.XPATH, "//b-pg-grid[@name='goods_items_view']/following-sibling::div//div[contains(@class, 'sg-cell') and t[text()='Итого']]")

    def check_items(self):
        self.wait_for_element_visible(self.get_product_total_quantity)
        quantity = self.get_numeric_value(self.get_product_total_quantity)
        price = self.get_numeric_value(self.get_product_total_price)
        total_sum = self.get_numeric_value(self.get_product_total_sum)
        return quantity, price, total_sum
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, "//button[@id='trade82-button-close']")

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
    # navbar_button='consignment'
    # ------------------------------------------------------------------------------------------------------------------

    def click_tablist_button(self, tablist_name):
        """
        tablist_name = ['Основная информация', 'Консигнация', 'Визиты', 'Дополнительная информация',
                        'Примечания', 'Чат', 'История изменений']
        """
        tablist_button = (By.XPATH, f'//div[@class="card-title"]/ul[@role="tablist"]//span[contains(text(), "{tablist_name}")]')
        self.click(tablist_button)
    # ------------------------------------------------------------------------------------------------------------------
    get_row_consignment = (By.XPATH, '//b-pg-grid[@name="consignments"]//div[@class="tbl-body"]//div[contains(@class, "tbl-no-data-row") and contains(text(), "нет данных")]')

    def check_row_consignment(self):
        self.wait_for_element_visible(self.get_row_consignment)
    # ------------------------------------------------------------------------------------------------------------------

    def check_consignments(self, add_date):
        """add_date = [30, 20, 10]"""
        current_date = datetime.now()
        future_date = current_date + timedelta(days=add_date)
        formatted_date = future_date.strftime("%d.%m.%Y")
        get_consignment_amount = (By.XPATH, f"//b-pg-grid[@name='consignments']//div[contains(@class, 'tbl-row')]/div[contains(@class, 'tbl-cell') and contains(text(), '{formatted_date}')]/following-sibling::div[1]")
        # print(f'formatted_date: {formatted_date}')
        return self.get_text(get_consignment_amount)

    # ------------------------------------------------------------------------------------------------------------------
    # navbar_button='audit'
    # ------------------------------------------------------------------------------------------------------------------

    def click_navbar_button(self, navbar_name):
        """navbar_name = ['Название', 'ТМЦ']"""
        audit = (By.XPATH, f'//div[contains(@ng-show,"audit")]//a[contains(text(),"{navbar_name}")]')
        self.click(audit)
    # ------------------------------------------------------------------------------------------------------------------
    get_header = (By.XPATH, '//b-grid[@name="header_audits"]')
    get_product = (By.XPATH, '//b-grid[@name="product_audits"]')

    def check_tablist_body(self, header=False, product=False):
        if header:
            self.wait_for_element_visible(self.get_header)
        if product:
            self.wait_for_element_visible(self.get_product)
    # ------------------------------------------------------------------------------------------------------------------
    def find_row(self, product_name):
        self.find_row_and_click(element_name=product_name,
                                xpath_pattern=f"//b-grid//div[contains(@class, 'tbl')]//div[contains(@class, 'tbl-row')]//div[contains(@class, 'tbl-cell') and normalize-space(text())='{product_name}']")
    # ------------------------------------------------------------------------------------------------------------------
    audit_details_button = (By.XPATH, "//button[@ng-click=\"auditDetails(row, 'products')\"]")

    def click_audit_details_button(self):
        self.click(self.audit_details_button)
    # ------------------------------------------------------------------------------------------------------------------
    get_order_audit = (By.XPATH, '//div[@role="tabpanel"]//b-pg-grid[@name="order_audits"]')

    def check_get_order_audit_body(self):
        self.wait_for_element_visible(self.get_order_audit)
    # ------------------------------------------------------------------------------------------------------------------
    close_toolbar_button = (By.XPATH, '//div[contains(@class,"b-toolbar")]/button[@ng-click="page.close()"]')

    def click_close_toolbar_button(self):
        self.click(self.close_toolbar_button)
    # ------------------------------------------------------------------------------------------------------------------