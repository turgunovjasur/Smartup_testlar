from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ExtraCostAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    articles_input = (By.XPATH, '//b-input[@name="articles"]//input')
    add_articles_button = (By.XPATH, '//b-input[@name="articles"]//a[@ng-click="_$bInput.onAddClick()"]')
    get_row = (By.XPATH, '//b-input[@name="articles"]//div[contains(@class,"hint-item")]/div[contains(@class,"form-row")]/div')

    def input_articles(self):
        self.click(self.articles_input)

        if not self._wait_for_visibility(self.get_row, timeout=5, error_message=True):
            self.click(self.add_articles_button)
            return False

        self.click(self.get_row)
        return True
    # ------------------------------------------------------------------------------------------------------------------
    corr_templates_input = (By.XPATH, '//b-input[@name="corr_templates"]//input')
    corr_templates_options = (By.XPATH, '//b-input[@name="corr_templates"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_corr_templates(self, corr_template_name):
        self.click_options(self.corr_templates_input, self.corr_templates_options, corr_template_name)
    # ------------------------------------------------------------------------------------------------------------------
    amount_input = (By.XPATH, '//input[@ng-model="d.amount"]')

    def input_amount(self, extra_cost_amount):
        self.input_text(self.amount_input, extra_cost_amount)
    # ------------------------------------------------------------------------------------------------------------------
    note_input = (By.XPATH, '//textarea[@ng-model="d.note"]')

    def input_note(self, note_text):
        self.input_text(self.note_input, note_text)
    # ------------------------------------------------------------------------------------------------------------------
    products_input = (By.XPATH, '//b-input[@name="products"]//input')
    products_options = (By.XPATH, '//b-input[@name="products"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def input_products(self, product_name):
        self.click_options(self.products_input, self.products_options, product_name)
    # ------------------------------------------------------------------------------------------------------------------
    quantity_input = (By.XPATH, '//b-pg-grid[@name="products"]//input[@ng-model="item.quantity"]')

    def input_quantity(self, product_quantity):
        self.input_text(self.quantity_input, product_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    price_input = (By.XPATH, '//b-pg-grid[@name="products"]//input[@ng-model="item.price"]')

    def input_price(self, product_price):
        self.input_text(self.price_input, product_price)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
