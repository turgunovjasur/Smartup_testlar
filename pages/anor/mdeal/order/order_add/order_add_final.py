from selenium.webdriver.common.by import By
from pages.core.md.base_page import BasePage
from datetime import datetime, timedelta


class OrderAddFinal(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//div[@id="anor279-order-step-info"]/div[@ng-click="goToStep(2)" and @data-wizard-state="current"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------

    def get_input_value(self, input_name):
        locator = (By.XPATH, f'//form[@name="step2"]//t[contains(text(),"{input_name}")]/../../span')
        return self.input_text(locator, get_value=True)
    # ------------------------------------------------------------------------------------------------------------------
    booked_payment_allowed_input = (By.XPATH, '//div[contains(@ng-show, "booked_payment_allowed")]//t[contains(text(),"Баланс клиента")]/ancestor::label/following-sibling::span')

    def get_booked_payment_allowed(self):
        return self.get_numeric_value(self.booked_payment_allowed_input)
    # ------------------------------------------------------------------------------------------------------------------
    booked_payment_percentage_input = (By.XPATH, '//div[contains(@ng-show, "booked_payment_allowed")]//t[contains(text(),"Минимальный процент предоплаты")]/ancestor::label/following-sibling::span')

    def get_booked_payment_percentage(self):
        return self.get_numeric_value(self.booked_payment_percentage_input)
    # ------------------------------------------------------------------------------------------------------------------
    payment_type_input = (By.XPATH, '//div[@id="anor279-inpu-b_input-payment_type"]//b-input[@name="payment_type"]//input')
    payment_options = (By.XPATH, '//div[@id="anor279-inpu-b_input-payment_type"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_payment_type(self, payment_type_name):
        self.click_options(self.payment_type_input, self.payment_options, payment_type_name)
    # ------------------------------------------------------------------------------------------------------------------
    get_total_amount = (By.XPATH, "//t[text()='ИТОГО']/parent::label/following-sibling::span")

    def check_total_amount(self):
        return self.get_numeric_value(self.get_total_amount)
    # ------------------------------------------------------------------------------------------------------------------
    consignment_date_input = (By.XPATH, '//div[@class="mb-4 ng-scope"]//input[@ng-model="item.consignment_date"]')
    consignment_amount_input = (By.XPATH, '//div[@class="mb-4 ng-scope"]//input[@ng-model="item.consignment_amount"]')
    consignment_amount_button = (By.XPATH, '//button[@ng-click="setConsignmentAmount(item)"]')

    def input_consignment_date(self, add_days, consignment_amount):
        """Joriy sanaga `add_days` kun qo'shib, uni kiritish."""

        # Sana hisoblash
        future_date = (datetime.now() + timedelta(days=add_days)).strftime("%d.%m.%Y")

        self.input_text(self.consignment_date_input, future_date)
        self.input_text(self.consignment_amount_input, consignment_amount)
    # ------------------------------------------------------------------------------------------------------------------
    status_input = (By.XPATH, "(//div[@id='anor279-ui_select-status']//span)[1]")

    # def input_status(self, status=1):
    #     self.click(self.status_input)
    #     status_options = (By.XPATH, f'//div[@id="anor279-ui_select-status"]//div[@role="option"][{status}]')
    #     self.click(status_options)

    def input_status_2(self, status_name):
        self.click(self.status_input)
        status_options = (By.XPATH, f'//div[@id="anor279-ui_select-status"]//div[@role="option"]//span[normalize-space(.)="{status_name}"]')
        self.click(status_options)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, "//button[@id='anor279-button-next_step']")
    yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    booked_payment_amount_input = (By.XPATH, '//input[@ng-model="d.booked_payment_amount"]')

    def input_booked_payment_amount(self, prepayment_amount):
        self.input_text(self.booked_payment_amount_input, prepayment_amount, check=True)
    # ------------------------------------------------------------------------------------------------------------------
    prev_step_button = (By.XPATH, '//button[@id="anor279-button-prev_step"]')

    def click_prev_step_button(self):
        self.click(self.prev_step_button)
    # ------------------------------------------------------------------------------------------------------------------
    setting_button = (By.XPATH, '//b-pg-controller[@name="goods_items_view"]//div[@role="group"]/button')
    setting_tbl_button = (By.XPATH, '//b-pg-controller[@name="goods_items_view"]//div[@role="group"]//a')

    def click_setting_button(self):
        self.click(self.setting_button)
        self.click(self.setting_tbl_button)
    # ------------------------------------------------------------------------------------------------------------------
    margin_value_input = (By.XPATH, '//div[@ng-model="d.margin_value"]//span[@ng-click="$select.activate()"]')

    def input_margin_value(self, margin):
        self.click(self.margin_value_input)

        option = (By.XPATH, f'//div[@ng-model="d.margin_value"]//div[@role="option"]/span[contains(text(),"{margin}")]')
        self.click(option)
    # ------------------------------------------------------------------------------------------------------------------
