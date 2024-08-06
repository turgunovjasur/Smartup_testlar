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
    # vendor_elem_xpath = '"UZUM TEZKOR" MCHJ XK'
    contract = ""
    payment_type = ""
    project = ""
    currency = ""
    invoice_no = ""
    invoice_date = ""
    inventory_receipt = ""
    input_extra_costs = ""

    def fill_form(self, vendor, vendor_elem_xpath):
        self.input_text_elem((By.XPATH, vendor), (By.XPATH, vendor_elem_xpath))
        # time.sleep(2)
        # self.extra_click_after_selection(vendor_elem_xpath)
        # time.sleep(2)


    ##############################################################################
    main_page_next_button_xpath = "//div[@class= 'd-flex flex-column']/div/div/div/following-sibling::div"

    def click_button(self, main_page_next_button_xpath):
        self.wait_and_click((By.XPATH, main_page_next_button_xpath))
    ##############################################################################
