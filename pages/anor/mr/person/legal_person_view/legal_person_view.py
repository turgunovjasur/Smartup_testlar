from selenium.webdriver.common.by import By
from pages.core.md.base_page import BasePage


class LegalPersonView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
    get_name = (By.XPATH, '//form[@name="form"]//div[@class="b-offcanvas-hide"]/span[1]')

    def get_person_name(self):
        return self.get_text(self.get_name)
    # ------------------------------------------------------------------------------------------------------------------

    def get_input_value(self, input_name):
        locator = (By.XPATH, f'//div[@class="card-body"]//t[text()="{input_name}"]/../../span[contains(@class,"form-view")]')
        return self.get_text(locator)
    # ------------------------------------------------------------------------------------------------------------------

    def get_card_value(self, card_name):
        locator = (By.XPATH, f'//div[@class="card-body pt-4"]//t[text()="{card_name}"]/../../span[contains(@class,"text-muted")]')
        return self.get_text(locator)
    # ------------------------------------------------------------------------------------------------------------------

    def click_navbar(self, navbar_name):
        locator = (By.XPATH, f'//ul[@role="tablist"]//span[contains(text(),"{navbar_name}")]')
        return self.click(locator)
    # ------------------------------------------------------------------------------------------------------------------
