from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class PurchasePage(BasePage):
    ##############################################################################
    purchase_page_header = "//div[@id='anor113-wizard_wrapper-main']"

    def element_visible(self, purchase_page_header):
        self.wait_for_element_visible((By.XPATH, purchase_page_header))

    ##############################################################################
    purchases_input = "//div[@id='anor113-input-b_input-purchases']/descendant::input[1]"
    purchases_elem = "//div[@id='anor113-input-b_input-purchases']//div[@class='hint-body ng-scope']/div[1]"
    quantity_input = "(//div[@class='tbl-cell']/input[@type='text'])[1]"
    ##############################################################################

    def fill_form(self, purchases_input, purchases_elem,
                  quantity_input, quantity):
        self.input_text_elem((By.XPATH, purchases_input), (By.XPATH, purchases_elem))
        self.input_text((By.XPATH, quantity_input), quantity)

    ##############################################################################
    price_finish = "//div[@class='tbl-row ng-scope']/div[9]"
    margin_finish = "//div[@class='tbl-row ng-scope']/div[10]"
    vat_finish = "//div[@class='tbl-row ng-scope']/div[11]"
    amount_finish = "//div[@class='tbl-row ng-scope']/div[13]"
    ##############################################################################

    def calculate(self, price_start, price_finish,
                  margin_start, margin_finish,
                  vat_start, vat_finish,
                  amount_start, amount_finish):
        self.price_finish = self.check_count(price_finish)
        self.margin_finish = self.check_count(margin_finish)
        self.vat_finish = self.check_count(vat_finish)
        self.amount_finish = self.check_count(amount_finish)

        try:
            assert price_start == self.price_finish, f"Expected price: {price_start}, Actual: {self.price_finish}"
            print(f"Price values match: {price_start} == {self.price_finish}")

            assert margin_start == self.margin_finish, f"Expected margin: {margin_start}, Actual: {self.margin_finish}"
            print(f"Margin values match: {margin_start} == {self.margin_finish}")

            assert vat_start == self.vat_finish, f"Expected vat: {vat_start}, Actual: {self.vat_finish}"
            print(f"Vat values match: {vat_start} == {self.vat_finish}")

            assert amount_start == self.amount_finish, f"Expected amount: {amount_start}, Actual: {self.amount_finish}"
            print(f"Amount values match: {amount_start} == {self.amount_finish}")

            print("All values are correct")
        except AssertionError as e:
            print(f"Assertion Error: {str(e)}")
            self.take_screenshot("check_count_error")
            raise

    ##############################################################################
    def check_number(self):
        return {
            'price': self.price_finish,
            'margin': self.margin_finish,
            'vat': self.vat_finish,
            'amount': self.amount_finish
        }

    ##############################################################################
    next_button = "//div[@id='anor113-wizard-extra_cost']"

    def click_button(self, next_button):
        self.click((By.XPATH, next_button))

    ##############################################################################