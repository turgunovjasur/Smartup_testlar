from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class MainPage(BasePage):
    ##############################################################################
    main_page_header = "//div[@id='anor289-wizard-main']"

    def element_visible(self, main_page_header):
        self.wait_for_element_visible((By.XPATH, main_page_header))

    ##############################################################################
    ref_types_input = "//div[@id='anor289-inputs-binput-reftypes']//input"
    ref_types_element = "//div[@id='anor289-inputs-binput-reftypes']//div[@class='hint-item ng-scope active']"
    payment_type_input = "//div[@id='anor289-inputs-binput-reftypes'][3]/descendant::input"
    payment_type_element = "//div[@id='anor289-inputs-binput-reftypes'][3]/descendant::div[@ng-if='origin.kind == q.origin_kind_query']//div/div/following-sibling::div/div"
    invoice_number_button = "//div[@id='anor289-input-text-invoicenumber']/input"
    with_input_input = "//div[@id='anor289-input-switch-withinput']/label[2]/span"
    warehouse_input = "//div[@id='anor289-input-binput-warehouse']/b-input//input"
    warehouse_element = "//div[@id='anor289-input-binput-warehouse']/b-input/div/div[2]/div/div[2]"
    with_extra_costs_button = "//div[@id='anor289-input-checkbox-extracostenabled']/label[2]/span"

    def fill_form(self, ref_types_input, ref_types_element,
                  payment_type_input, payment_type_element,
                  with_input_input,
                  warehouse_input, warehouse_element,
                  with_extra_costs_button):
        self.input_text_elem((By.XPATH, ref_types_input), (By.XPATH, ref_types_element))
        self.input_text_elem((By.XPATH, payment_type_input), (By.XPATH, payment_type_element))
        self.click((By.XPATH, with_input_input))
        self.input_text_elem((By.XPATH, warehouse_input), (By.XPATH, warehouse_element))
        self.click((By.XPATH, with_extra_costs_button))

    ##############################################################################
    next_step_button = "//div[@class= 'd-flex flex-column']/div/div/div/following-sibling::div"

    def click_button(self, next_step_button):
        self.click((By.XPATH, next_step_button))

    ##############################################################################