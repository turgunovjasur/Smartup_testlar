from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class ErrorMessage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    error_massage_xpath = (By.XPATH, '//div[@id="biruniAlertExtended"]//div[@class="modal-content"]//div[@class="modal-title"]//div[@class="ng-binding"]')

    def error_massage(self):
        full_text = self.get_text(self.error_massage_xpath)
        error_code = full_text.split('—')[0].strip()
        return error_code
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//div[@id="biruniAlertExtended"]//div[@class="modal-content"]//button[@class="close p-4 m-n4"]')

    def click_error_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
