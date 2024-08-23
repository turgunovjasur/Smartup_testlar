from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class ExtraCostPage(BasePage):
    ##############################################################################
    extra_cost_page_header = "//div/descendant::div/h3/t[contains(text(), 'Основное')]"

    def element_visible(self, extra_cost_page_header):
        self.wait_for_element_visible((By.XPATH, extra_cost_page_header))

    ##############################################################################
    next_step_button = "//div[@id= 'anor289-wizard-finishing']"

    def click_button(self, next_step_button, ):
        self.click((By.XPATH, next_step_button))

    ##############################################################################