import time

from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class SalesModal(BasePage):
    def check_modal(self, header_xpath, expected_text, error_message):
        assert expected_text in self.get_text((By.XPATH, header_xpath)), error_message

    def click_button(self, button_xpath):
        time.sleep(2)
        self.click_element((By.XPATH, button_xpath))
