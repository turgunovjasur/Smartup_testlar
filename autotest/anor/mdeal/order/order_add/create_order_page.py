from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class OrderAddMain(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//button[@id='anor279-button-next_step']")

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    rooms_input = (By.XPATH, "//div[@id='anor279-input-b_input-room_name']//input")
    options_room = (By.XPATH, '//div[@id="anor279-input-b_input-room_name"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def click_rooms_input(self, room_name):
        self.clear_element(self.rooms_input)
        self.click_options(self.rooms_input, self.options_room, room_name)
    # ------------------------------------------------------------------------------------------------------------------
    robots_input = (By.XPATH, '//div[@id="anor279-input-b_input-robot_name"]//b-input[@name="robots"]//input')
    options_robot = (By.XPATH, '//div[@id="anor279-input-b_input-robot_name"]//b-input[@name="robots"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def click_robots_input(self, robot_name):
        self.clear_element(self.robots_input)
        self.click_options(self.robots_input, self.options_robot, robot_name)
    # ------------------------------------------------------------------------------------------------------------------
    persons_input = (By.XPATH, '//div[@id="anor279-input-b_input-person_name"]//b-input[@name="persons"]//input')
    options_person = (By.XPATH, '//b-input[@name="persons"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def click_persons_input(self, client_name):
        self.clear_element(self.persons_input)
        self.click_options(self.persons_input, self.options_person, client_name)
    # ------------------------------------------------------------------------------------------------------------------
    contract_input = (By.XPATH, '//div[@id="anor279-input-b_input-contract_name"]//b-input[@name="contracts"]//input')
    options_contract = (By.XPATH, '//div[@id="anor279-input-b_input-contract_name"]//b-input[@name="contracts"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def click_contract_input(self, contract_name):
        self.clear_element(self.contract_input)
        self.click_options(self.contract_input, self.options_contract, contract_name)
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = (By.XPATH, "//button[@id='anor279-button-next_step']")

    def click_next_step_button(self,):
        self.click(self.next_step_button)
    # ------------------------------------------------------------------------------------------------------------------
