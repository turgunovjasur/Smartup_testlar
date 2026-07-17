import time
from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class SystemSetting(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//div[@class="card-title"]//t[contains(text(), "Основное")]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------

    def click_navbar_button(self, navbar_name):
        button = (By.XPATH, f'//div[contains(@class,"navi navi-bolder")]//span/t[contains(text(),"{navbar_name}")]')
        self.click(button)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    order_header = (By.XPATH, '//div[@class="card-title"]/h5/t[contains(text(), "Заказы")]')

    def element_visible_order(self):
        self.wait_for_element_visible(self.order_header)
    # ------------------------------------------------------------------------------------------------------------------
    # Consignment
    # ------------------------------------------------------------------------------------------------------------------
    consignment_checkbox = (By.XPATH, '//input[@ng-model="d.consignment_allow"]/../input')

    def checkbox_consignment(self, state):
        return self.click_checkbox(self.consignment_checkbox, state)
    # ------------------------------------------------------------------------------------------------------------------
    consignment_day_limit_input = (By.XPATH, '//input[@ng-model="d.consignment_day_limit"]')

    def input_consignment_day_limit(self, day_limit):
        self.input_text(self.consignment_day_limit_input, day_limit)
    # ------------------------------------------------------------------------------------------------------------------
    # Prepayment
    # ------------------------------------------------------------------------------------------------------------------
    prepayment_checkbox = (By.XPATH, '//input[@ng-model="d.deal_booked_payment_allow"]/../input')

    def checkbox_prepayment(self, state):
        return self.click_checkbox(self.prepayment_checkbox, state)
    # ------------------------------------------------------------------------------------------------------------------
    prepayment_input = (By.XPATH, '//div[@ng-model="d.deal_booked_payment_allow_by_status"]')

    def input_prepayment(self, status_name):
        self.click(self.prepayment_input)

        options_prepayment = (By.XPATH, f'//div[@ng-model="d.deal_booked_payment_allow_by_status"]//div[@role="option"]/span[contains(text(),"{status_name}")]')
        self.click(options_prepayment)
    # ------------------------------------------------------------------------------------------------------------------
    prepayment_min_percent_input = (By.XPATH, '//input[@ng-model="d.deal_booked_payment_min_percent"]')

    def input_prepayment_min_percent(self, payment_min_percent):
        self.input_text(self.prepayment_min_percent_input, payment_min_percent)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//b-subpage[@name="deal"]//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
        time.sleep(0.5)
    # ------------------------------------------------------------------------------------------------------------------
