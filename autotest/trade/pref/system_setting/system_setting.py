import time

from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class SystemSetting(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//div[@class="card-title"]//t[contains(text(), "Основное")]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------

    def click_navbar_button(self, navbar_button):
        """Navbarda joylashgan buttonlar tartibi"""
        button = (By.XPATH, f'(//div[@class="navi navi-bolder navi-hover navi-active navi-link-rounded"]/div/a)[{navbar_button}]')
        self.click(button)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    order_header = (By.XPATH, '//div[@class="card-title"]/h5/t[contains(text(), "Заказы")]')

    def element_visible_order(self):
        return self.wait_for_element_visible(self.order_header)
    # ------------------------------------------------------------------------------------------------------------------
    consignment_checkbox_text = (By.XPATH, '//input[@type="checkbox" and @ng-model="d.consignment_allow"]/following-sibling::span/t')

    def check_checkbox_text(self):
        text = self.get_text(self.consignment_checkbox_text)
        return text.lower() == 'да'
    # ------------------------------------------------------------------------------------------------------------------
    consignment_checkbox = (By.XPATH, '//input[@type="checkbox" and @ng-model="d.consignment_allow"]/following-sibling::span')

    def click_checkbox_consignment(self):
        self.click(self.consignment_checkbox)
    # ------------------------------------------------------------------------------------------------------------------
    consignment_day_limit_input = (By.XPATH, '//input[@ng-model="d.consignment_day_limit"]')

    def input_consignment_day_limit(self, day_limit):
        self.input_text(self.consignment_day_limit_input, day_limit)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//b-subpage[@name="deal"]//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
        time.sleep(0.5)
    # ------------------------------------------------------------------------------------------------------------------
