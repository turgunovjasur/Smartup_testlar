from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class PurchasePage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    purchase_page_header = (By.XPATH, "//div[@id='anor113-wizard_wrapper-main']")

    def element_visible(self):
        self.wait_for_element_visible(self.purchase_page_header)

    # ------------------------------------------------------------------------------------------------------------------
    purchases_input = (By.XPATH, "//div[@id='anor113-input-b_input-purchases']/descendant::input[1]")
    purchases_elem = (By.XPATH, "//div[@id='anor113-input-b_input-purchases']//div[@class='hint-body ng-scope']/div[1]")
    # ------------------------------------------------------------------------------------------------------------------

    def fill_form(self):
        self.input_text_elem(self.purchases_input, self.purchases_elem)
    # ------------------------------------------------------------------------------------------------------------------
    quantity_input = (By.XPATH, "(//div[@class='tbl-cell']/input[@type='text'])[1]")

    price_xpath = (By.XPATH, "//div[@class='tbl-row ng-scope']/div[9]")
    amount_xpath = (By.XPATH, "//div[@class='tbl-row ng-scope']/div[13]")
    # margin_xpath = (By.XPATH, "//div[@class='tbl-row ng-scope']/div[10]")
    # vat_percent_xpath = (By.XPATH, "//div[@class='tbl-row ng-scope']/div[11]")

    def calculate(self, quantity):
        self.input_text(self.quantity_input, quantity)
        price = self.get_numeric_value(self.price_xpath)
        amount = quantity * price
        amount_xpath = self.get_numeric_value(self.amount_xpath)
        try:
            assert amount == amount_xpath, f"Expected amount: {amount}, but got: {amount_xpath}"
            print(f"Successful!: Total price {amount} = {amount_xpath}")

        except AssertionError:
            self.take_screenshot("amount_error")
            print(f"Miscalculated: {amount} =! {amount_xpath}")
    # ------------------------------------------------------------------------------------------------------------------
    next_button = (By.XPATH, "//div[@id='anor113-wizard-extra_cost']")

    def click_button(self):
        self.click(self.next_button)
    # ------------------------------------------------------------------------------------------------------------------
