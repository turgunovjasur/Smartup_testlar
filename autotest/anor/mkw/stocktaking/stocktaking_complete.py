from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class StocktakingComplete(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="add()"]')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------

    def get_input_value(self, input_name, clean=None):
        locator = (By.XPATH, f'//label[contains(.,"{input_name}")]/../div[contains(@class,"form-view")]')
        return self.get_text(locator, clean=clean)
    # ------------------------------------------------------------------------------------------------------------------
    movements_button = (By.XPATH, '//a[@id="corrs_tab"]')

    def click_movements_button(self):
        self.click(self.movements_button)
    # ------------------------------------------------------------------------------------------------------------------
    add_template_button = (By.XPATH, '//button[@ng-click="addCorr()"]')

    def click_add_template_button(self):
        self.click(self.add_template_button)
    # ------------------------------------------------------------------------------------------------------------------
    corr_kind_radio_button = (By.XPATH, '(//input[@name="corr_kind1"])[2]/../span')

    def click_corr_kind_radio_button(self):
        self.click(self.corr_kind_radio_button)
    # ------------------------------------------------------------------------------------------------------------------

    def input_templates(self, template_name, index=1):
        templates_input = (By.XPATH, f'(//b-input[@name="corr_templates"]//input)[{index}]')
        options_template = (By.XPATH, f'(//b-input[@name="corr_templates"])[{index}]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

        self.click_options(templates_input, options_template, template_name)
    # ------------------------------------------------------------------------------------------------------------------

    def input_amount(self, product_amount, index=1):
        amount_input = (By.XPATH, f'(//input[@ng-model="corr.amount"])[{index}]')
        self.input_text(amount_input, product_amount)
    # ------------------------------------------------------------------------------------------------------------------
    finish_button = (By.XPATH, '//button[@ng-click="finish()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_finish_button(self):
        self.click(self.finish_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
