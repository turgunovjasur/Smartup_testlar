from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class ReferenceNavbar(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = By.XPATH, "(//span[contains(text(), 'Справочники')])[3]"

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    inventories_button = By.XPATH, "//span[text()='ТМЦ']"

    def click_button_inventories(self):
        self.click(self.inventories_button)
    # ------------------------------------------------------------------------------------------------------------------
    prices_button = By.XPATH, "//span[text()='Цены']"

    def click_button_prices(self):
        self.click(self.prices_button)
    # ------------------------------------------------------------------------------------------------------------------
    services_button = By.XPATH, "//span[text()='Услуги']"

    def click_button_services(self):
        self.click(self.services_button)
    # ------------------------------------------------------------------------------------------------------------------
    action_button = By.XPATH, "//li/a/span[contains(text(), 'Акции')]"

    def click_action_button(self):
        self.click(self.action_button)
    # ------------------------------------------------------------------------------------------------------------------
    overload_button = By.XPATH, "//li/a/span[contains(text(), 'Нагрузки')]"

    def click_overload_button(self):
        self.click(self.overload_button)
    # ------------------------------------------------------------------------------------------------------------------
