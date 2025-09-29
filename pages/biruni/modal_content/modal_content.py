from selenium.webdriver.common.by import By
from pages.core.md.base_page import BasePage


class ModalContent(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    # biruniConfirm
    # ------------------------------------------------------------------------------------------------------------------

    def is_visible_biruni_confirm(self):
        locator = (By.XPATH, '//div[@id="biruniConfirm"]//div[@class="modal-body"]/h4')
        self.wait_for_element(locator, timeout=2, wait_type="visibility")
    # ------------------------------------------------------------------------------------------------------------------

    def get_biruni_confirm(self):
        locator = (By.XPATH, '//div[@id="biruniConfirm"]//div[@class="modal-body"]/h4')
        return self.get_text(locator)
    # ------------------------------------------------------------------------------------------------------------------

    def click_biruni_confirm_button(self, state):
        action = "Yes" if state else "No"
        locator = (By.XPATH, f'//div[@id="biruniConfirm"]//button[@ng-click="a.bConfirm.click{action}()"]')
        self.click(locator)
    # ------------------------------------------------------------------------------------------------------------------
    # biruniAlert
    # ------------------------------------------------------------------------------------------------------------------

    def is_visible_biruni_alert(self):
        locator = (By.XPATH, '//div[@id="biruniAlert"]//div[@class="modal-body"]/h4')
        try:
            self.wait_for_element(locator, timeout=2, wait_type="visibility")
        except Exception:
            pass
    # ------------------------------------------------------------------------------------------------------------------

    def get_biruni_alert(self):
        locator = (By.XPATH, '//div[@id="biruniAlert"]//div[@class="modal-body"]/h4')
        return self.get_text(locator)
    # ------------------------------------------------------------------------------------------------------------------

    def click_biruni_alert_close_button(self):
        locator = (By.XPATH, f'//div[@id="biruniAlert"]//button[contains(text(),"Закрыть")]')
        self.click(locator)
    # ------------------------------------------------------------------------------------------------------------------
    # error_massage
    # ------------------------------------------------------------------------------------------------------------------
    error_massage_xpath = (By.XPATH, '//div[@id="biruniAlertExtended"]//div[@class="modal-content"]//div[@class="modal-title"]//div[@class="ng-binding"]')

    def error_massage(self):
        try:
            full_text = self.get_text(self.error_massage_xpath)
            error_code = full_text.split('—')[0].strip()
            return error_code
        except Exception:
            self.logger.warning(f"error_massage not found!")
            return False
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//div[@id="biruniAlertExtended"]//div[@class="modal-content"]//button[@class="close p-4 m-n4"]')

    def click_error_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
