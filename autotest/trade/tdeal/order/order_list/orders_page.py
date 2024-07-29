import time

from autotest.core.md.base_page import BasePage

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OrdersPage(BasePage):
    def element_visible(self, order_page_header_xpath):
        self.wait_for_element_visible((By.XPATH, order_page_header_xpath))

    def check_count(self, count_xpath):
        wait = WebDriverWait(self.driver, 20)
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, count_xpath)))
            count_text = element.text.strip()
            if count_text:
                count = ''.join(filter(str.isdigit, count_text))
                return int(count) if count else 0
            else:
                print("Warn: the count element is empty")
                return 0
        except Exception as e:
            print(f"Check_count_error: {str(e)}")
            self.take_screenshot("check_count_error")
            return 0

    def click_button(self, create_button_xpath):
        time.sleep(5)
        self.wait_and_click((By.XPATH, create_button_xpath))
