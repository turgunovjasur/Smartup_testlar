import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from autotest.core.md.base_page import BasePage


class DashboardPage(BasePage):
    def check_page(self, header_xpath, expected_text, error_message):
        wait = WebDriverWait(self.driver, 20)
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, header_xpath)))
            assert expected_text in element.text, error_message
        except:
            self.take_screenshot("dashboard_page_error")
            raise

    def click_button(self, button_xpath):
        time.sleep(5)
        self.click_element((By.XPATH, button_xpath))


