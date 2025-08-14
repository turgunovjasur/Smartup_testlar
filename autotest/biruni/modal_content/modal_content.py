from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class ModalContent(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    modal_content = (By.XPATH, '//div[@id="biruniConfirm"]//div[@class="modal-body"]/h4')

    def get_modal_content(self):
        return self.get_text(self.modal_content)
    # ------------------------------------------------------------------------------------------------------------------

    def click_modal_button(self, state):
        action = "Yes" if state else "No"
        locator = (By.XPATH, f'//div[@id="biruniConfirm"]//button[@ng-click="a.bConfirm.click{action}()"]')
        self.click(locator)
    # ------------------------------------------------------------------------------------------------------------------
