from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class InventoryPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    inventory_page_header = (By.XPATH, "//div/descendant::div/h3/t[contains(text(), 'Основное')]")

    def element_visible(self):
        self.wait_for_element_visible(self.inventory_page_header)
    # ------------------------------------------------------------------------------------------------------------------
    fast_search_input = By.XPATH, "//b-input[@id= 'anor289-input-binput-fastsearchquery-G-0']/descendant::input[@placeholder= 'Поиск...']"
    fast_search_element = By.XPATH, "//div[@class= 'tbl-cell']/b-input[@id= 'anor289-input-binput-fastsearchquery-G-0']/descendant::div[@class= 'hint-body ng-scope']/div[1]"
    quantity_input = By.XPATH, "//input[@id= 'anor289-input-text-quantity-G-0']"
    price_input = By.XPATH, "//input[@id= 'anor289-input-text-price-G-0']"
    side_scrolling = By.XPATH, "//b-pg-grid[@id='anor289-bpggrid-productsG']/descendant::div[@class='tbl']/following-sibling::div[2]/span/i"
    margin_value_button = By.XPATH, "//button[@id='anor289-button-changemarginpercent-G-0']"
    margin_value_input = By.XPATH, "//input[@id='anor289-input-text-margin-G-0']"
    vat_percent_input = By.XPATH, "//input[@id='anor289-input-text-vatpercent-G-0']"

    def fill_form(self, quantity, price, margin_value, vat_percent):
        self.input_text_elem(self.fast_search_input, self.fast_search_element)
        self.input_text(self.quantity_input, quantity)
        self.input_text(self.price_input, price)
        self.hover_and_hold(self.side_scrolling, duration=3000)
        self.click(self.margin_value_button)
        self.input_text(self.margin_value_input, margin_value)
        self.input_text(self.vat_percent_input, vat_percent)
    # ------------------------------------------------------------------------------------------------------------------
    get_amount = By.XPATH, "//b-pg-grid[@id='anor289-bpggrid-productsG']/following-sibling::div/descendant::div[@class='sg-cell col-3 ng-binding'][1]"
    get_margin_amount = By.XPATH, "//b-pg-grid[@id='anor289-bpggrid-productsG']/following-sibling::div/descendant::div[@class='sg-cell col-3 ng-binding'][2]"
    get_vat_amount = By.XPATH, "//b-pg-grid[@id='anor289-bpggrid-productsG']/following-sibling::div/descendant::div[@class='sg-cell col-3 ng-binding'][4]"
    get_total_amount = By.XPATH, "//b-pg-grid[@id='anor289-bpggrid-productsG']/following-sibling::div/descendant::div[@class='sg-cell col-2 ng-binding'][3]"
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = By.XPATH, "//div[@id='anor289-wizard-extracosts']"

    def click_button(self):
        self.click(self.next_step_button)
    # ------------------------------------------------------------------------------------------------------------------
