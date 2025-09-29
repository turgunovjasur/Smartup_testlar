from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ReturnOrder(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="save()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    get_client_name = (By.XPATH, '//form[@name="form"]//div[@class="card-body"]//t[contains(text(), "Клиент")]/ancestor::label/following-sibling::span')

    def check_client_name(self):
        return self.get_text(self.get_client_name)
    # ------------------------------------------------------------------------------------------------------------------
    get_total_price = (By.XPATH, '//form[@name="form"]//div[@class="card-body"]//t[contains(text(), "Сумма заказа")]/ancestor::label/following-sibling::span')

    def check_total_price(self):
        return self.get_text(self.get_total_price)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    return_all_button = (By.XPATH, '//button[@ng-click="returnAll(row)"]')

    def click_return_all_button(self):
        self.click(self.return_all_button)
    # ------------------------------------------------------------------------------------------------------------------
