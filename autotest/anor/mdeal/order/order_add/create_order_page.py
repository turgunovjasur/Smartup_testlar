import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from autotest.core.md.base_page import BasePage


class CreateOrderPage(BasePage):
    def fill_form(self, room, robot, client, room_xpath, room_elem_xpath,
                  robot_xpath, robot_elem_xpath, client_xpath, client_elem_xpath):
        self.new_input((By.XPATH, room_xpath), room, (By.XPATH, room_elem_xpath))
        self.new_input((By.XPATH, robot_xpath), robot, (By.XPATH, robot_elem_xpath))
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


