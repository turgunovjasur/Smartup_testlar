from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class ReferenceNavbar(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    reference_navbar_header = "(//span[contains(text(), 'Справочники')])[3]"

    def element_visible(self, reference_navbar_header):
        self.wait_for_element_visible((By.XPATH, reference_navbar_header))
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    reference_button = "//span[text()='ТМЦ']"

    def click_button_reference(self, reference_button):
        self.click((By.XPATH, reference_button))
    # ------------------------------------------------------------------------------------------------------------------
    prices_button = "//span[text()='Цены']"

    def click_button_prices(self, prices_button):
        self.click((By.XPATH, prices_button))
    # ------------------------------------------------------------------------------------------------------------------
    services_button = "//span[text()='Услуги']"

    def click_button_services(self, services_button):
        self.click((By.XPATH, services_button))
    # ------------------------------------------------------------------------------------------------------------------
    action_button = "//li/a/span[contains(text(), 'Акции')]"

    def click_action_button(self, action_button):
        self.click((By.XPATH, action_button))
    # ------------------------------------------------------------------------------------------------------------------
    overload_button = "//li/a/span[contains(text(), 'Нагрузки')]"

    def click_overload_button(self, overload_button):
        self.click((By.XPATH, overload_button))
    # ------------------------------------------------------------------------------------------------------------------
