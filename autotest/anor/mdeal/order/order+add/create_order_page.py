import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from .base_page import BasePage


class CreateOrderPage(BasePage):
    def fill_form(self, workspace, staff_unit, client, workspace_xpath, workspace_elem_xpath,
                  staff_unit_xpath, staff_unit_elem_xpath, client_xpath, client_elem_xpath):
        self.new_input((By.XPATH, workspace_xpath), workspace, (By.XPATH, workspace_elem_xpath))
        self.new_input((By.XPATH, staff_unit_xpath), staff_unit, (By.XPATH, staff_unit_elem_xpath))
        self.new_input((By.XPATH, client_xpath), client, (By.XPATH, client_elem_xpath))

    def check_page(self, header_xpath, expected_text, error_message):
        wait = WebDriverWait(self.driver, 20)
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, header_xpath)))
            assert expected_text in element.text, f"{error_message} - {element.text}"
        except:
            self.take_screenshot("create_order_page_error")
            raise

    def click_next_button(self, button_xpath):
        time.sleep(2)
        self.click_element((By.XPATH, button_xpath))


