from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class LegalPersonView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//div[@class="card-title"]/h3/t')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
    text = (By.XPATH, '//form[@name="form"]//div[@class="b-offcanvas-hide"]/span[1]')

    def check_text(self):
        return self.get_text(self.text)
    # ------------------------------------------------------------------------------------------------------------------
