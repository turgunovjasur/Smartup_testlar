import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from autotest.core.md.base_page import BasePage


class OrdersPage(BasePage):
    def check_page(self, header_xpath, expected_text, error_message):
        wait = WebDriverWait(self.driver, 20)
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, header_xpath)))
            assert expected_text in element.text, error_message
        except:
            self.take_screenshot("Order_page_error")
            raise

    def check_count(self, count_xpath):
        wait = WebDriverWait(self.driver, 20)
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, count_xpath)))
            count_text = element.text.strip()
            if count_text:
                count = ''.join(filter(str.isdigit, count_text))
                return int(count) if count else 0
            else:
                print("Warn: hisoblash elementi bo'sh")
                return 0
        except Exception as e:
            print(f"Check_count-dagi xato: {str(e)}")
            self.take_screenshot("check_count_error")
            return 0

    def click_create_button(self, button_xpath):
        time.sleep(2)
        self.click_element((By.XPATH, button_xpath))


