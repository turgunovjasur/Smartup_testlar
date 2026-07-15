import time
from pages.core.md.base_page import BasePage
from selenium.webdriver import Keys
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
    # TEMPORARY DELIVERY DATE PERMISSION — START
    # Dev checkboxni default ishlaydigan qilgach, ushbu blokni o‘chirish mumkin.
    # ------------------------------------------------------------------------------------------------------------------
    delivery_date_permission_header = (
        By.XPATH,
        '//h6/t[contains(text(), "Права на изменение даты отгрузки")]',
    )
    delivery_date_permission_create_button = (
        By.XPATH,
        '//button[@ng-click="openCreateDeliveryDateRuleModal()"]',
    )
    delivery_date_permission_modal = (
        By.XPATH,
        '//div[contains(@class,"delivery_date_change_rule_modal") and contains(@class,"show")]'
        '//h5[contains(.,"Права на изменение даты отгрузки")]',
    )
    delivery_date_permission_role_input = (
        By.XPATH,
        '//div[contains(@class,"delivery_date_change_rule_modal") and contains(@class,"show")]'
        '//b-input[@model="q.ddcgRule.roles"]//input',
    )
    delivery_date_permission_access_input = (
        By.XPATH,
        '//div[contains(@class,"delivery_date_change_rule_modal") and contains(@class,"show")]'
        '//*[@ng-model="q.ddcgRule.grantOpt"]//span[@ng-click="$select.activate()"]',
    )
    delivery_date_permission_add_button = (
        By.XPATH,
        '//div[contains(@class,"delivery_date_change_rule_modal") and contains(@class,"show")]'
        '//button[normalize-space(.)="Добавить"]',
    )

    def element_visible_delivery_date_permission(self):
        self.wait_for_element_visible(self.delivery_date_permission_header)

    def _delivery_date_permission_row(self, role_name, access_name=""):
        access_condition = (
            f' and ./div[normalize-space(.)="{access_name}"]'
            if access_name else ""
        )
        return (
            By.XPATH,
            '//h6[t[contains(text(),"Права на изменение даты отгрузки")]]'
            '/ancestor::div[contains(concat(" ",normalize-space(@class)," ")," card ")][1]'
            '//div[contains(@class,"tbl-row") '
            f'and ./div[normalize-space(.)="{role_name}"]{access_condition}]',
        )

    def has_delivery_date_permission(self, role_name, access_name):
        locator = self._delivery_date_permission_row(role_name, access_name)
        return any(element.is_displayed() for element in self.driver.find_elements(*locator))

    def click_create_delivery_date_permission(self):
        self.click(self.delivery_date_permission_create_button)
        self.wait_for_element_visible(self.delivery_date_permission_modal)

    def input_delivery_date_permission_role(self, role_name):
        self.click(self.delivery_date_permission_role_input)
        role_option = (
            By.XPATH,
            '//div[contains(@class,"delivery_date_change_rule_modal") and contains(@class,"show")]'
            '//b-input[@model="q.ddcgRule.roles"]//div[contains(@class,"hint-item")]'
            f'[normalize-space(.)="{role_name}"]',
        )
        self.click(role_option)

        role_input = self.wait_for_element(self.delivery_date_permission_role_input, wait_type="presence")
        role_input.send_keys(Keys.TAB)

    def input_delivery_date_permission_access(self, access_name):
        self.click(self.delivery_date_permission_access_input)
        access_option = (
            By.XPATH,
            '//div[contains(@class,"delivery_date_change_rule_modal") and contains(@class,"show")]'
            '//*[@ng-model="q.ddcgRule.grantOpt"]//div[@role="option"]'
            f'/span[normalize-space(.)="{access_name}"]',
        )
        self.click(access_option)

    def click_add_delivery_date_permission(self):
        self.click(self.delivery_date_permission_add_button)

    def wait_for_delivery_date_permission(self, role_name, access_name):
        return self.wait_for_element_visible(
            self._delivery_date_permission_row(role_name, access_name)
        )
    # TEMPORARY DELIVERY DATE PERMISSION — END
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//b-subpage[@name="deal"]//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
        time.sleep(0.5)
    # ------------------------------------------------------------------------------------------------------------------
