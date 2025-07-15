from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class WriteOffExpense(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------

    def get_input_value(self, input_name):
        locator = (By.XPATH, f'//label[contains(.,"{input_name}")]/../span')
        return self.get_text(locator)
    # ------------------------------------------------------------------------------------------------------------------
    corr_templates_input = (By.XPATH, '//b-input[@name="corr_templates"]//input')
    options_corr_template = (By.XPATH, '//b-input[@name="corr_templates"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_corr_templates(self, corr_template_name):
        self.click_options(self.corr_templates_input, self.options_corr_template, corr_template_name)
    # ------------------------------------------------------------------------------------------------------------------
    origins_input = (By.XPATH, '(//b-input[@name="origins"])[1]//input')
    options_origin = (By.XPATH, '(//b-input[@name="origins"])[1]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_origins(self, origin_name):
        try:
            self.click_options(self.origins_input, self.options_origin, origin_name)
        except Exception as e:
            self.logger.warning(f"Expense_article not found! {e}")
    # ------------------------------------------------------------------------------------------------------------------
    payment_type_input = (By.XPATH, '(//b-input[@name="origins"])[3]//input')
    options_payment_type = (By.XPATH, '(//b-input[@name="origins"])[3]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_payment_type(self, payment_type):
        self.click_options(self.payment_type_input, self.options_payment_type, payment_type)
    # ------------------------------------------------------------------------------------------------------------------
    currencies_input = (By.XPATH, '//b-input[@name="currencies"]//input')
    options_currencies = (By.XPATH, '//b-input[@name="currencies"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_currencies(self, currencies_name):
        self.click_options(self.currencies_input, self.options_currencies, currencies_name)

    def get_input_currencies(self):
        return self.input_text(self.currencies_input, get_value=True)
        # return self.get_text(self.currencies_input)
    # ------------------------------------------------------------------------------------------------------------------
    expense_amount_input = (By.XPATH, '//input[@ng-model="expense.amount"]')

    def input_expense_amount(self, expense_amount):
        self.input_text(self.expense_amount_input, expense_amount)
    # ------------------------------------------------------------------------------------------------------------------
    complete_button = (By.XPATH, '//button[@ng-click="complete()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_complete_button(self):
        self.click(self.complete_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
