from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class PurchaseAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//div[@id="anor289-wizard-main"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    supplier_input = (By.XPATH, '(//div[@id="anor289-inputs-binput-reftypes"]//input)[1]')
    supplier_options = (By.XPATH, '//div[@id="anor289-inputs-binput-reftypes"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def input_supplier(self, supplier_name):
        self.click_options(self.supplier_input, self.supplier_options, supplier_name)
    # ------------------------------------------------------------------------------------------------------------------
    checkbox_input = (By.XPATH, '//div[@id="anor289-input-checkbox-extracostenabled"]//span')

    def click_extra_cost_checkbox(self):
        self.click(self.checkbox_input)
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = (By.XPATH, '//button[@id="anor289-button-nextstep"]')
    save_button = (By.XPATH, '//button[@id="anor289-button-save"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_next_step_button(self, save_button=False):
        if not save_button:
            self.click(self.next_step_button)
        else:
            self.click(self.save_button)
            self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    product_input = (By.XPATH, '(//b-input[contains(@id,"anor289-input-binput-fastsearchquery-G-")])[last()]//input')
    product_options = (By.XPATH, '((//b-input[contains(@id,"anor289-input-binput-fastsearchquery-G-")])[last()])//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div[1]')

    def input_product(self, product_name):
        self.click_options(self.product_input, self.product_options, product_name)
    # ------------------------------------------------------------------------------------------------------------------
    quantity_input = (By.XPATH, '(//input[contains(@id,"anor289-input-text-quantity-G-")])[last()-1]')

    def input_quantity(self, product_quantity):
        self.input_text(self.quantity_input, product_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    price_input = (By.XPATH, '(//input[contains(@id,"anor289-input-text-price-G-")])[last()-1]')

    def input_price(self, product_price):
        self.input_text(self.price_input, product_price)
    # ------------------------------------------------------------------------------------------------------------------
    purchase_number_input = (By.XPATH, '//div[@id="anor289-input-text-purchasenumber"]//input')

    def input_purchase_number(self, purchase_number):
        self.input_text(self.purchase_number_input, purchase_number)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    extra_cost_input = (By.XPATH, '//b-input[@id="anor289-input-binput-extracostnumber"]//input')
    add_input = (By.XPATH, '//b-input[@id="anor289-input-binput-extracostnumber"]//a[@ng-click="_$bInput.onAddClick()"]')

    def input_extra_cost(self):
        self.click(self.extra_cost_input)
        self.click(self.add_input)
    # ------------------------------------------------------------------------------------------------------------------
    calc_extra_cost_button = (By.XPATH, '//button[@id="anor289-button-calcextracost"]')

    def click_calc_extra_cost_button(self):
        self.click(self.calc_extra_cost_button)
    # ------------------------------------------------------------------------------------------------------------------

    def get_product_total_amount(self, product_name):
        get_product = (By.XPATH, f'//div[@id="extra_cost_products"]//div[text()="{product_name}"]/following-sibling::div/input')
        self.get_numeric_value(get_product)
    # ------------------------------------------------------------------------------------------------------------------
