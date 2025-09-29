from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class SalesWork(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    select_template_button = (By.XPATH, "//button[@ng-click='selectTemplate()']")

    def click_select_template(self):
        self.click(self.select_template_button)
    # ------------------------------------------------------------------------------------------------------------------
    generate_button = (By.XPATH, '//button[@ng-click="generate()"]')

    def click_generate(self):
        self.click(self.generate_button)
    # ------------------------------------------------------------------------------------------------------------------
    templates_input = (By.XPATH, '//b-input[@name="templates"]//input')

    def input_templates(self):
        return self.input_text(self.templates_input, get_value=True)
    # ------------------------------------------------------------------------------------------------------------------
