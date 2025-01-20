from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta


class OrderView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//div[@class='card-title']/h5/t")

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    order_id = (By.XPATH, "(//div[@class='card-body']/div/div/div/div[@class='col-sm'])[1]")

    def check_order_id(self):
        return self.get_numeric_value(self.order_id)
    # ------------------------------------------------------------------------------------------------------------------
    get_status = (By.XPATH, '(//form[@name="form"]//div[@class="row"]//div[@class="col-sm-12"]/span)[1]')

    def check_status(self):
        return self.get_text(self.get_status)
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
    get_client_name = (By.XPATH, '//form[@name="form"]//div[@class="form-group"]//t[contains(text(), "Клиент")]/ancestor::label/following-sibling::span')

    def check_client_name(self):
        return self.get_text(self.get_client_name)
    # ------------------------------------------------------------------------------------------------------------------
    # navbar_button='consignment'
    # ------------------------------------------------------------------------------------------------------------------

    def click_tablist_button(self, navbar_button):
        tablist_button = (By.XPATH, f'//div[@class="card-title"]/ul[@role="tablist"]//span[contains(text(), "{navbar_button}")]')
        self.click(tablist_button)
    # ------------------------------------------------------------------------------------------------------------------
    get_row_consignment = (By.XPATH, '//b-pg-grid[@name="consignments"]//div[@class="tbl-body"]//div[contains(@class, "tbl-no-data-row") and contains(text(), "нет данных")]')

    def check_row_consignment(self):
        self.wait_for_element_visible(self.get_row_consignment)

    def check_consignments(self, add_date):
        current_date = datetime.now()
        future_date = current_date + timedelta(days=add_date)
        formatted_date = future_date.strftime("%d.%m.%Y")
        get_consignment_amount = (By.XPATH, f"//b-pg-grid[@name='consignments']//div[contains(@class, 'tbl-row')]/div[contains(@class, 'tbl-cell') and contains(text(), '{formatted_date}')]/following-sibling::div[1]")
        # print(f'formatted_date: {formatted_date}')
        return self.get_text(get_consignment_amount)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, "//button[@id='trade82-button-close']")

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
