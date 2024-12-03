from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class UserAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="save()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, '//input[@ng-model="d.name"]')

    def input_name(self, user_full_name):
        self.input_text(self.name_input, user_full_name)
    # ------------------------------------------------------------------------------------------------------------------
    login_input = (By.XPATH, '//input[@ng-model="d.login"]')

    def input_login(self, login):
        self.input_text(self.login_input, login)
    # ------------------------------------------------------------------------------------------------------------------
    password_input = (By.XPATH, '//input[@ng-model="d.password"]')

    def input_password(self, password):
        self.input_text(self.password_input, password)
    # ------------------------------------------------------------------------------------------------------------------
    mouse_down_button = (By.XPATH, '//input[@id="new_password"]/following-sibling::div/button')

    def click_mouse_down_button(self):
        self.click(self.mouse_down_button)
    # ------------------------------------------------------------------------------------------------------------------
    roles_input = (By.XPATH, '//b-input[@name="roles"]//input')
    roles_options = (By.XPATH, '//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_role(self, role_name):
        self.click_options(self.roles_input, self.roles_options, role_name)
    # ------------------------------------------------------------------------------------------------------------------
    robot_input = (By.XPATH, '//b-input[@name="robot"]//input')
    robot_options = (By.XPATH, '//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_robot(self, robot_name):
        self.click_options(self.robot_input, self.robot_options, robot_name)
    # ------------------------------------------------------------------------------------------------------------------
    person_name_input = (By.XPATH, '//b-input[@name="persons"]//input')
    options = (By.XPATH, '//b-input[@name="persons"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_person_name(self, natural_person_name):
        self.click_options(self.person_name_input, self.options, natural_person_name)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//b-input[@model="d.person_name"]//div/a[@ng-click="_$bInput.onAddClick()"]')

    def input_add_person_name(self):
        self.click(self.person_name_input)
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
