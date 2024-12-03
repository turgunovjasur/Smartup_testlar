import time
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class CompanyAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//h5/t[contains(text(),'Основная информация')]")

    def element_visible(self):
        return self.wait_for_element_visible(self.header)

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    code_input = (By.XPATH, '//input[@ng-model="d.code"]')

    def input_code(self, code_company):
        self.input_text(self.code_input, code_company)

    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, '//input[@ng-model="d.name"]')

    def input_name(self, name_company):
        self.input_text(self.name_input, name_company)

    # ------------------------------------------------------------------------------------------------------------------
    plan_accounts_input = (By.XPATH, '(//b-input[@name="templates"]//input)[1]')
    plan_options = (
    By.XPATH, '(//b-input[@name="templates"])[1]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_plan_accounts(self, plan_account):
        self.click_options(self.plan_accounts_input, self.plan_options, plan_account)

    # ------------------------------------------------------------------------------------------------------------------
    bank_input = (By.XPATH, '(//b-input[@name="templates"]//input)[2]')
    bank_options = (
    By.XPATH, '(//b-input[@name="templates"])[2]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_bank(self, bank_name):
        self.click_options(self.bank_input, self.bank_options, bank_name)

    # ------------------------------------------------------------------------------------------------------------------

    def input_checkbox(self):
        for i in range(3, 11):
            try:
                checkbox = (By.XPATH, f'(//label[@class="checkbox mt-0"])[{i}]')
                self.click(checkbox)
            except:
                continue
    # ------------------------------------------------------------------------------------------------------------------

    save_button = (By.XPATH, '//button[@ng-click="save()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
        time.sleep(10)
    # ------------------------------------------------------------------------------------------------------------------
