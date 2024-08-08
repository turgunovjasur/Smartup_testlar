from selenium.webdriver.common.by import By

from autotest.core.md.base_page import BasePage


class ExtraCostPage(BasePage):
    ##############################################################################
    extra_cost_page_header_xpath = "//div/descendant::div/h3/t[contains(text(), 'Основное')]"

    def element_visible(self, extra_cost_page_header_xpath):
        self.wait_for_element_visible((By.XPATH, extra_cost_page_header_xpath))

    ##############################################################################
    finish_page_next_button_xpath = "//div[@id= 'anor289-wizard-finishing']"

    def click_button(self, finish_page_next_button_xpath, ):
        self.wait_and_click((By.XPATH, finish_page_next_button_xpath))

    ##############################################################################
