from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class OrderRequestAddMain(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="nextStep()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = (By.XPATH, '//button[@ng-click="nextStep()"]')

    def click_next_step_button(self):
        self.click(self.next_step_button)
    # ------------------------------------------------------------------------------------------------------------------
    rooms_input = (By.XPATH, '//b-input[@name="rooms"]//input')
    options_room = (By.XPATH, '//b-input[@name="rooms"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def click_rooms_input(self, room_name):
        self.clear_element(self.rooms_input)
        self.click_options(self.rooms_input, self.options_room, room_name)
    # ------------------------------------------------------------------------------------------------------------------
    robots_input = (By.XPATH, '//b-input[@name="robots"]//input')
    options_robot = (By.XPATH, '//b-input[@name="robots"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def click_robots_input(self, robot_name):
        self.clear_element(self.robots_input)
        self.click_options(self.robots_input, self.options_robot, robot_name)
    # ------------------------------------------------------------------------------------------------------------------
    persons_input = (By.XPATH, '//b-input[@name="persons"]//input')
    options_person = (By.XPATH, '//b-input[@name="persons"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def click_persons_input(self, client_name):
        self.clear_element(self.persons_input)
        self.click_options(self.persons_input, self.options_person, client_name)
    # ------------------------------------------------------------------------------------------------------------------
