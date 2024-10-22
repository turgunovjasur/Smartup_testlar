from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class MainPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    main_page_header = By.XPATH, "//div[@id='anor289-wizard-main']"

    def element_visible(self):
        self.wait_for_element_visible(self.main_page_header)
    # ------------------------------------------------------------------------------------------------------------------
    order_number_input = By.XPATH, "//input[@ng-model='d.order_number']"

    ref_types_input = By.XPATH, "//div[@id='anor289-inputs-binput-reftypes']//input"
    ref_types_element = By.XPATH, "//div[@id='anor289-inputs-binput-reftypes']//div[@class='hint-item ng-scope active']"
    payment_type_input = By.XPATH, "//div[@id='anor289-inputs-binput-reftypes'][3]/descendant::input"
    payment_type_element = By.XPATH, "//div[@id='anor289-inputs-binput-reftypes'][3]/descendant::div[@ng-if='origin.kind == q.origin_kind_query']//div/div/following-sibling::div/div"
    invoice_number_button = By.XPATH, "//div[@id='anor289-input-text-invoicenumber']/input"
    with_input_input = By.XPATH, "//div[@id='anor289-input-switch-withinput']/label[2]/span"
    warehouse_input = By.XPATH, "//div[@id='anor289-input-binput-warehouse']/b-input//input"
    warehouse_element = By.XPATH, "//div[@id='anor289-input-binput-warehouse']/b-input/div/div[2]/div/div[2]"
    with_extra_costs_button = By.XPATH, "//div[@id='anor289-input-checkbox-extracostenabled']/label[2]/span"

    def fill_form(self, order_number):
        self.input_text(self.order_number_input, order_number)
        self.input_text_elem(self.ref_types_input, self.ref_types_element)
        self.input_text_elem(self.payment_type_input, self.payment_type_element)
        self.click(self.with_input_input)
        self.input_text_elem(self.warehouse_input, self.warehouse_element)
        self.click(self.with_extra_costs_button)
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = By.XPATH, "//div[@class= 'd-flex flex-column']/div/div/div/following-sibling::div"

    def click_button(self):
        self.click(self.next_step_button)
    # ------------------------------------------------------------------------------------------------------------------
