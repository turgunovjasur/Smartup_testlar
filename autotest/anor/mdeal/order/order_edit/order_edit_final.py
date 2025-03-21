from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage
from datetime import datetime, timedelta


class OrderEditFinal(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header_text = (By.XPATH, "//div/h3/t[contains(text(), 'ТМЦ')]")

    def element_visible(self):
        return self.wait_for_element_visible(self.header_text)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    payment_type_input = (By.XPATH, '//div[@id="anor279-inpu-b_input-payment_type"]//b-input[@name="payment_type"]//input')
    payment_options = (By.XPATH, '//div[@id="anor279-inpu-b_input-payment_type"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_payment_type(self, payment_type_name):
        self.click_options(self.payment_type_input, self.payment_options, payment_type_name)
    # ------------------------------------------------------------------------------------------------------------------
    status_input = (By.XPATH, "(//div[@id='anor279-ui_select-status']//span)[1]")
    status_options = (By.XPATH, '//div[@id="anor279-ui_select-status"]/div[@ng-model="d.status"]/ul/li/div[3]')

    def input_status(self):
        self.click(self.status_input)
        self.click(self.status_options)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, "//button[@id='anor279-button-next_step']")
    yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    error_massage_xpath = (By.XPATH, '//div[@id="biruniAlertExtended"]//div[@class="modal-content"]//div[@class="modal-title"]//div[@class="ng-binding"]')

    def error_massage(self):
        full_text = self.get_text(self.error_massage_xpath)
        error_code = full_text.split('—')[
            0].strip()
        return error_code
    # ------------------------------------------------------------------------------------------------------------------
    error_button = (By.XPATH, '//div[@id="biruniAlertExtended"]//div[@class="modal-content"]//button[@class="close p-4 m-n4"]')

    def click_error_button(self):
        self.click(self.error_button)
    # ------------------------------------------------------------------------------------------------------------------
