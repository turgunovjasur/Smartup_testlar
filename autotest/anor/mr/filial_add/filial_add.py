from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class FilialAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="save()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, '//input[@ng-model="d.name"]')

    def input_name(self, filial_name):
        self.input_text(self.name_input, filial_name)
    # ------------------------------------------------------------------------------------------------------------------
    base_currency_name_input = (By.XPATH, '//b-input[@name="currencies"]//input')
    currency_options = (By.XPATH, '//b-input[@name="currencies"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def input_base_currency_name(self, base_currency_cod):
        self.click(self.base_currency_name_input)
        self.click_options(self.base_currency_name_input, self.currency_options, base_currency_cod)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    person_name_input = (By.XPATH, '//b-input[@name="legal_persons"]//input')
    person_options = (By.XPATH, '//b-input[@name="legal_persons"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_person_name(self, legal_person_name):
        self.click_options(self.person_name_input, self.person_options, legal_person_name)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//b-input[@model="d.person_name"]//div/a[@ng-click="_$bInput.onAddClick()"]')

    def input_add_person_name(self):
        self.click(self.person_name_input)
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
