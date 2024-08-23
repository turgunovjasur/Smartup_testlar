from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class ExtraCostPage(BasePage):
    ##############################################################################
    extra_cost_page_header = "//div[@id='anor113-wizard_wrapper-main']"

    def element_visible(self, extra_cost_page_header):
        self.wait_for_element_visible((By.XPATH, extra_cost_page_header))

    ##############################################################################
    next_button = "//div[@id='anor113-wizard-finishing']"

    def click_button(self, next_button):
        self.click((By.XPATH, next_button))

    ##############################################################################