from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class ClientAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="save()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    radio_button = (By.XPATH, '(//label[@class="radio"])[2]/span')

    def click_radio_button(self):
        self.click(self.radio_button)
    # ------------------------------------------------------------------------------------------------------------------
    persons_input = (By.XPATH, '//b-input[@name="persons"]//input')
    person_options = (By.XPATH, '//b-input[@name="persons"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_name(self, person_name):
        self.click_options(self.persons_input, self.person_options, person_name)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
