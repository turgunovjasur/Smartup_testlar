from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class ExtraCostPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    extra_cost_page_header = (By.XPATH, "//div/descendant::div/h3/t[contains(text(), 'Основное')]")

    def element_visible(self):
        self.wait_for_element_visible(self.extra_cost_page_header)
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = (By.XPATH, "//div[@id= 'anor289-wizard-finishing']")

    def click_button(self):
        self.click(self.next_step_button)
    # ------------------------------------------------------------------------------------------------------------------
