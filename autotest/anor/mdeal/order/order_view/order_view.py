from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


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

    def check_items(self):
        self.wait_for_element_visible(self.get_product_total_quantity)
        quantity = self.get_numeric_value(self.get_product_total_quantity)
        price = self.get_numeric_value(self.get_product_total_price)
        return quantity, price
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, "//button[@id='trade82-button-close']")

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
