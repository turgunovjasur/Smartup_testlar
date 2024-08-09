import time

from selenium.webdriver.common.by import By

from autotest.core.md.base_page import BasePage


class InventoryPage(BasePage):
    ##############################################################################
    inventory_page_header_xpath = "//div/descendant::div/h3/t[contains(text(), 'Основное')]"

    def element_visible(self, inventory_page_header_xpath):
        self.wait_for_element_visible((By.XPATH, inventory_page_header_xpath))

    ##############################################################################
    inventory_input = "//b-input[@id= 'anor289-input-binput-fastsearchquery-G-0']/descendant::input[@placeholder= 'Поиск...']"
    inventory = "//div[@class= 'tbl-cell']/b-input[@id= 'anor289-input-binput-fastsearchquery-G-0']/descendant::div[@class= 'hint-body ng-scope']/div[1]"

    qty_input = "//input[@id= 'anor289-input-text-quantity-G-0']"
    qty = "10"

    price_input = "//input[@id= 'anor289-input-text-price-G-0']"
    price = "120000"

    vat_input = "//input[@id='anor289-input-text-vatpercent-G-0']"
    vat = "12"

    margin_vat = "//button[@id='anor289-button-changemarginpercent-G-0']"
    margin_value_input = "//input[@id='anor289-input-text-margin-G-0']"
    margin_value = "20"

    count_xpath = "//b-pg-grid[@id='anor289-bpggrid-productsG']/following-sibling::div/descendant::div[@class='sg-cell col-3 ng-binding'][1]"
    margin_count_xpath = "//b-pg-grid[@id='anor289-bpggrid-productsG']/following-sibling::div/descendant::div[@class='sg-cell col-3 ng-binding'][2]"
    total_amount_xpath = "//b-pg-grid[@id='anor289-bpggrid-productsG']/following-sibling::div/descendant::div[@class='sg-cell col-2 ng-binding'][3]"
    vat_amount_xpath = "//b-pg-grid[@id='anor289-bpggrid-productsG']/following-sibling::div/descendant::div[@class='sg-cell col-3 ng-binding'][4]"

    side_scrolling_xpath = "//b-pg-grid[@id='anor289-bpggrid-productsG']/descendant::div[@class='tbl']/following-sibling::div[2]/span/i"

    def fill_form(self, inventory_input, inventory,
                  qty_input, qty,
                  price_input, price,
                  side_scrolling_xpath,
                  margin_vat, margin_value_input, margin_value,
                  vat_input, vat,
                  count_xpath, margin_count_xpath, total_amount_xpath, vat_amount_xpath):
        self.input_text_elem((By.XPATH, inventory_input), (By.XPATH, inventory))
        self.input_text((By.XPATH, qty_input), qty)
        self.input_text((By.XPATH, price_input), price)
        time.sleep(2)
        self.hover_and_hold((By.XPATH, side_scrolling_xpath), duration=3000)
        self.wait_and_click((By.XPATH, margin_vat))
        self.input_text((By.XPATH, margin_value_input), margin_value)
        self.input_text((By.XPATH, vat_input), vat)
        time.sleep(2)
        self.check_counts_and_calculations(count_xpath, margin_count_xpath, vat_amount_xpath, total_amount_xpath,
                                           qty, price, vat, margin_value)

    ##############################################################################

    def check_counts_and_calculations(self, count_xpath, margin_count_xpath, vat_amount_xpath, total_amount_xpath,
                                      qty, price, vat, margin_value):
        # Kutilyotgan qiymatlarni hisoblash
        amount = int(qty) * int(price)
        margin_amount = int(qty) * int(margin_value)
        vat_amount = ((int(qty) * int(price)) + (int(qty) * int(margin_value))) * int(vat) / 100
        total_amount = (int(qty) * int(price)) + (int(qty) * int(margin_value)) + int(vat_amount)

        # Har bir qiymatni olish va solishtirish
        actual_amount = self.get_element_value(count_xpath, as_int=True)
        actual_margin_amount = self.get_element_value(margin_count_xpath, as_int=True)
        actual_vat_amount = self.get_element_value(vat_amount_xpath, as_int=True)
        actual_total_amount = self.get_element_value(total_amount_xpath, as_int=True)

        expected_values = [amount, margin_amount, total_amount, vat_amount]
        actual_values = [actual_amount, actual_margin_amount, actual_vat_amount, actual_total_amount]
        labels = ["Amount", "Margin Amount", "VAT Amount", "Total Amount"]

        for label, expected, actual in zip(labels, expected_values, actual_values):
            if expected == actual:
                print(f"{label} tekshiruvi muvaffaqiyatli o'tdi: {actual}")
            else:
                print(f"{label} tekshiruvi muvaffaqiyatsiz: Kutilyotgan {expected}, ammo mavjud {actual}")

        return all([expected == actual for expected, actual in zip(expected_values, actual_values)])

    ##############################################################################
    extra_cost_page_next_button_xpath = "//div[@id='anor289-wizard-extracosts']"

    def click_button(self, extra_cost_page_next_button_xpath):
        self.wait_and_click((By.XPATH, extra_cost_page_next_button_xpath))
    ##############################################################################

