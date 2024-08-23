import time
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class InventoryPage(BasePage):
    ##############################################################################
    inventory_page_header = "//div/descendant::div/h3/t[contains(text(), 'Основное')]"

    def element_visible(self, inventory_page_header):
        self.wait_for_element_visible((By.XPATH, inventory_page_header))

    ##############################################################################
    fast_search_input = "//b-input[@id= 'anor289-input-binput-fastsearchquery-G-0']/descendant::input[@placeholder= 'Поиск...']"
    fast_search_element = "//div[@class= 'tbl-cell']/b-input[@id= 'anor289-input-binput-fastsearchquery-G-0']/descendant::div[@class= 'hint-body ng-scope']/div[1]"
    side_scrolling = "//b-pg-grid[@id='anor289-bpggrid-productsG']/descendant::div[@class='tbl']/following-sibling::div[2]/span/i"

    def fill_form(self, fast_search_input, fast_search_element,
                  quantity_input, quantity,
                  price_input, price,
                  side_scrolling,
                  margin_value_button, margin_value_input, margin_value,
                  vat_percent_input, vat_percent,
                  get_amount, get_margin_amount, get_vat_amount, get_total_amount):
        self.input_text_elem((By.XPATH, fast_search_input), (By.XPATH, fast_search_element))
        self.input_text((By.XPATH, quantity_input), quantity)
        self.input_text((By.XPATH, price_input), price)
        time.sleep(2)
        self.hover_and_hold((By.XPATH, side_scrolling), duration=3000)
        self.click((By.XPATH, margin_value_button))
        self.input_text((By.XPATH, margin_value_input), margin_value)
        self.input_text((By.XPATH, vat_percent_input), vat_percent)
        time.sleep(2)
        self.check_counts_and_calculations(get_amount, get_margin_amount, get_vat_amount, get_total_amount, quantity,
                                           price, margin_value, vat_percent)

    ##############################################################################
    quantity_input = "//input[@id= 'anor289-input-text-quantity-G-0']"
    price_input = "//input[@id= 'anor289-input-text-price-G-0']"
    margin_value_button = "//button[@id='anor289-button-changemarginpercent-G-0']"
    margin_value_input = "//input[@id='anor289-input-text-margin-G-0']"
    vat_percent_input = "//input[@id='anor289-input-text-vatpercent-G-0']"
    ##############################################################################

    get_amount = "//b-pg-grid[@id='anor289-bpggrid-productsG']/following-sibling::div/descendant::div[@class='sg-cell col-3 ng-binding'][1]"
    get_margin_amount = "//b-pg-grid[@id='anor289-bpggrid-productsG']/following-sibling::div/descendant::div[@class='sg-cell col-3 ng-binding'][2]"
    get_vat_amount = "//b-pg-grid[@id='anor289-bpggrid-productsG']/following-sibling::div/descendant::div[@class='sg-cell col-3 ng-binding'][4]"
    get_total_amount = "//b-pg-grid[@id='anor289-bpggrid-productsG']/following-sibling::div/descendant::div[@class='sg-cell col-2 ng-binding'][3]"

    def check_counts_and_calculations(self, get_amount, get_margin_amount, get_vat_amount, get_total_amount,
                                      quantity, price, margin_value, vat_percent):
        self.start_amount = int(quantity) * int(price)
        self.start_margin_amount = int(quantity) * int(margin_value)
        self.start_vat_amount = ((self.start_amount + self.start_margin_amount) * int(vat_percent)) / 100
        self.start_total_amount = self.start_amount + self.start_margin_amount + self.start_vat_amount

        finish_amount = self.check_count(get_amount)
        finish_margin_amount = self.check_count(get_margin_amount)
        finish_vat_amount = self.check_count(get_vat_amount)
        finish_total_amount = self.check_count(get_total_amount)

        try:
            assert self.start_amount == finish_amount, f"Expected amount: {self.start_amount}, Actual: {finish_amount}"
            print(f"Amount values match: {self.start_amount} == {finish_amount}")

            assert self.start_margin_amount == finish_margin_amount, f"Expected margin amount: {self.start_margin_amount}, Actual: {finish_margin_amount}"
            print(f"Margin amount values match: {self.start_margin_amount} == {finish_margin_amount}")

            assert self.start_vat_amount == finish_vat_amount, f"Expected VAT amount: {self.start_vat_amount}, Actual: {finish_vat_amount}"
            print(f"VAT amount values match: {self.start_vat_amount} == {finish_vat_amount}")

            assert self.start_total_amount == finish_total_amount, f"Expected total amount: {self.start_total_amount}, Actual: {finish_total_amount}"
            print(f"Total amount values match: {self.start_total_amount} == {finish_total_amount}")

            print("All values are correct")
        except AssertionError as e:
            print(f"Assertion Error: {str(e)}")
            self.take_screenshot("check_count_error")
            raise

    ##############################################################################
    def check_number(self):
        return {
            'start_amount': self.start_amount,
            'start_margin_amount': self.start_margin_amount,
            'start_vat_amount': self.start_vat_amount,
            'start_total_amount': self.start_total_amount
        }

    ##############################################################################
    next_step_button = "//div[@id='anor289-wizard-extracosts']"

    def click_button(self, next_step_button):
        self.click((By.XPATH, next_step_button))

    ##############################################################################