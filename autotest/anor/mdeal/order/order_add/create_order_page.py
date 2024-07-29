from selenium.webdriver.common.by import By

from autotest.core.md.base_page import BasePage


class CreateOrderPage(BasePage):

    def element_visible(self, create_order_header_xpath):
        self.wait_for_element_visible((By.XPATH, create_order_header_xpath))

    def fill_form(self, order_request, order_request_xpath, room_xpath, robot_xpath, client_xpath,
                  room_elem, robot_elem, client_elem):
        self.input_text((By.XPATH, order_request_xpath), order_request)
        self.input_text_elem((By.XPATH, room_xpath), (By.XPATH, room_elem))
        self.input_text_elem((By.XPATH, robot_xpath), (By.XPATH, robot_elem))
        self.input_text_elem((By.XPATH, client_xpath), (By.XPATH, client_elem))

    def click_button(self, create_order_next_button_xpath):
        self.wait_and_click((By.XPATH, create_order_next_button_xpath))