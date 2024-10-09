import random
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class CreateOrderPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.number = 13
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//div/h3/t[contains(text(), 'Основное')]")

    def element_visible(self):
        self.wait_for_element_visible(self.header)

    # ------------------------------------------------------------------------------------------------------------------
    order_request_input = (By.XPATH, "(//div[@id='anor279-input-b_input-request_number']//input)[2]")
    room_input = (By.XPATH, "(//div[@id='anor279-input-b_input-room_name']//input)[2]")
    room_elem = (By.XPATH, "//div[@id='anor279-input-b_input-room_name']//div[@class='hint-body ng-scope']/div[1]")
    robot_input = (By.XPATH, "(//div[@id='anor279-input-b_input-robot_name']//input)[2]")
    robot_elem = (By.XPATH, "//div[@id='anor279-input-b_input-robot_name']//b-input//div[@class='hint-body ng-scope']/div[1]")

    def fill_form(self, timeout=2):
        self.number = random.randint(1, 9999)
        self.input_text(self.order_request_input, self.number)
        self.input_text_elem(self.room_input, self.room_elem, timeout=timeout)
        self.input_text_elem(self.robot_input, self.robot_elem, timeout=timeout)
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = (By.XPATH, "//button[@id='anor279-button-next_step']")

    def click_button(self,):
        self.click(self.next_step_button)
    # ------------------------------------------------------------------------------------------------------------------
