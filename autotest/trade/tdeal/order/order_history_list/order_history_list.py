import time
from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class OrdersHistoryList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header_text = (By.XPATH, "(//div/h6/span)[1]")

    def element_visible(self):
        self.wait_for_element_visible(self.header_text)
    # ------------------------------------------------------------------------------------------------------------------
    order_history_info = (By.XPATH, "//b-grid//div[@class='tbl-body']/div/i")

    def check_history(self, timeout=2):
        return self.find_element(self.order_history_info, timeout=timeout)
    # ------------------------------------------------------------------------------------------------------------------
    list_first_elem = (By.XPATH, "(//div[@class='tbl-row']/div[2])[1]")

    def click_first_elem_button(self):
        time.sleep(2)
        self.click(self.list_first_elem)
    # ------------------------------------------------------------------------------------------------------------------
    # payment_type
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, "//button[@id='trade83-button-view']")

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    # payment_type
    # ------------------------------------------------------------------------------------------------------------------
    change_payment_type_button = (By.XPATH, "//button[@id='trade83-button-change_payment_type']")
    header_pyment_type = (By.XPATH, "(//div/h6/span)[1]")
    # ------------------------------------------------------------------------------------------------------------------
    pyment_type_delete = (By.XPATH, "//b-input[@id='trade83-input-b_input-payment_type_name']//span[@class='icon-right']")
    # ------------------------------------------------------------------------------------------------------------------
    pyment_type_input = (By.XPATH, "//b-input[@id='trade83-input-b_input-payment_type_name']//input")
    pyment_type_elem = (By.XPATH, "//b-input[@id='trade83-input-b_input-payment_type_name']//div[@class='hint-body ng-scope']/div[2]")
    # ------------------------------------------------------------------------------------------------------------------
    save_pyment_type_button = (By.XPATH, "//button[@id='trade83-button-save_payment_type']")

    def click_change_payment_type_button(self):
        self.click(self.change_payment_type_button)
        self.wait_for_element_visible(self.header_pyment_type)
        self.click(self.pyment_type_delete)
        self.input_text_elem(self.pyment_type_input, self.pyment_type_elem)
        self.click(self.save_pyment_type_button)
    # ------------------------------------------------------------------------------------------------------------------
    # change_sub-filial
    # ------------------------------------------------------------------------------------------------------------------
    change_subfilial_button = (By.XPATH, "//button[@id='trade83-button-change_subfilial']")
    change_subfilial_input = (By.XPATH, "//b-input[@id='trade83-input-b_input_subfilial_name']//input")
    save_subfilial_button = (By.XPATH, "//button[@id='trade83-button-save_subfilial']")

    def click_change_subfilial_button(self):
        self.click(self.change_subfilial_button)
        self.input_text(self.change_subfilial_input, 'proect-1')
        self.click(self.save_subfilial_button)
    # -----------------------------------------------------------------------------------------------------------------
    # change_status_one
    # -----------------------------------------------------------------------------------------------------------------
    change_status_one_button = (By.XPATH, "//button[@id='trade83-button-change_status_one']")
    save_status_one_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_change_status_one_button(self):
        self.click(self.change_status_one_button)
        self.click(self.save_status_one_button)
    # -----------------------------------------------------------------------------------------------------------------
    count_number = (By.XPATH, "//div[@id='trade83-sg_header-info']//div[@class='sg-sub-row ng-scope']/div[1]")
    count_info = (By.XPATH, "//div[@id='trade83-sg_header-info']")

    def check_order_history(self):
        if self.find_element(self.count_info, timeout=2):
            return self.get_numeric_value(self.count_number)
        else:
            return 0
    # -----------------------------------------------------------------------------------------------------------------
    return_button = (By.XPATH, "//button[@id='trade83-button-return_deal']")

    def click_return_button(self):
        self.click(self.return_button)
    # -----------------------------------------------------------------------------------------------------------------
