import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from .base_page import BasePage


class GoodsPage(BasePage):
    def fill_form(self, name_input_xpath, name_elem_xpath, qty_input_xpath, qty):
        self.new_wait_input((By.XPATH, name_input_xpath), (By.XPATH, name_elem_xpath))
        time.sleep(5)
        self.input_text((By.XPATH, qty_input_xpath), qty)

    def check_page(self, header_xpath, expected_text, error_message):
        wait = WebDriverWait(self.driver, 20)
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, header_xpath)))
            assert expected_text in element.text, f"{error_message} - {element.text}"
        except:
            self.take_screenshot("goods_page_error")
            raise

    def click_next_button(self, next_button_xpath):
        self.click_element((By.XPATH, next_button_xpath))


