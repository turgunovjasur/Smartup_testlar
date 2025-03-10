from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class LegalPersonAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//input[@ng-model="d.name" and @ng-change="validateName()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, '//input[@ng-model="d.name" and @ng-change="validateName()"]')

    def input_name(self, legal_person_name):
        self.input_text(self.name_input, legal_person_name)
    # ------------------------------------------------------------------------------------------------------------------
    tin_input = (By.XPATH, '//input[@ng-model="d.details.tin"]')

    def input_tin(self, tin_number):
        self.input_text(self.tin_input, tin_number)
    # ------------------------------------------------------------------------------------------------------------------
    legal_persons_input = (By.XPATH, '//b-input[@name="legal_persons"]//input[@ng-model="d.parent_person_name"]')
    options_locator = (By.XPATH, '//b-input[@name="legal_persons"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def input_legal_persons(self, element):
        self.click_options(self.legal_persons_input, self.options_locator, element)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
