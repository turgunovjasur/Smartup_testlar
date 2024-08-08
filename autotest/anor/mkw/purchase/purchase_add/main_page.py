import time

from selenium.webdriver.common.by import By

from autotest.core.md.base_page import BasePage


class MainPage(BasePage):
    ##############################################################################
    main_page_header_xpath = "//div/descendant::div/h3/t[contains(text(), 'Основное')]"

    def element_visible(self, main_page_header_xpath):
        self.wait_for_element_visible((By.XPATH, main_page_header_xpath))

    ##############################################################################
    purchase_time = ""
    inventory_receipt_data = ""
    order = ""
    operation_template = ""
    vendor = "(//input[@placeholder= 'Поиск...'])[2]"
    vendor_elem_xpath = "//div[@id='anor289-inputs-binput-reftypes']/div/div/following-sibling::div[2]/div/div/b-input/div/div/following-sibling::div/div/div[1]"
    contract = ""
    payment_type = "//div[@id='anor289-inputs-binput-reftypes'][3]/descendant::input"
    payment_type_elem = "//div[@id='anor289-inputs-binput-reftypes'][3]/descendant::div[@ng-if='origin.kind == q.origin_kind_query']//div/div/following-sibling::div/div/div[1]"
    project = ""
    currency = ""
    invoice_no = "//div[@id='anor289-input-text-invoicenumber']/input"
    invoice_date = ""
    inventory_receipt = "//div[@id='anor289-input-switch-withinput']/label[2]/span"
    warehouse = "//div[@id='anor289-input-binput-warehouse']/b-input//input"
    warehouse_elem = "//div[@id='anor289-input-binput-warehouse']/b-input/div/div[2]/div/div[1]"
    input_extra_costs = "//div[@id='anor289-input-checkbox-extracostenabled']/label[2]/span"

    def fill_form(self, vendor, vendor_elem_xpath,
                  payment_type, payment_type_elem,
                  inventory_receipt,
                  warehouse, warehouse_elem,
                  input_extra_costs):
        self.input_text_elem((By.XPATH, vendor), (By.XPATH, vendor_elem_xpath))
        self.input_text_elem((By.XPATH, payment_type), (By.XPATH, payment_type_elem))
        self.click((By.XPATH, inventory_receipt))
        self.input_text_elem((By.XPATH, warehouse), (By.XPATH, warehouse_elem))
        self.click((By.XPATH, input_extra_costs))

    ##############################################################################
    main_page_next_button_xpath = "//div[@class= 'd-flex flex-column']/div/div/div/following-sibling::div"

    def click_button(self, main_page_next_button_xpath):
        self.wait_and_click((By.XPATH, main_page_next_button_xpath))
    ##############################################################################
