from datetime import datetime, timedelta
from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class OrderAttachData(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    delivery_date_checkbox = (By.XPATH, '//input[@ng-model="d.delivery_date_changed"]/following-sibling::span')
    delivery_date_input = (By.XPATH, '//input[@ng-model="d.delivery_date"]')

    def click_delivery_date_checkbox(self, days):
        self.click_checkbox(self.delivery_date_checkbox)

        value = self.input_text(self.delivery_date_input, get_value=True)
        input_date = datetime.strptime(value, "%d.%m.%Y")
        new_date = input_date + timedelta(days=days)
        new_date_str = new_date.strftime("%d.%m.%Y")

        self.input_text(self.delivery_date_input, new_date_str)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
