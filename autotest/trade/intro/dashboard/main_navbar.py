from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class MainNavbar(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//span[text()='Основное']")

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    organization_button = (By.XPATH, "//span[text()='Организации']")

    def click_organization_button(self):
        self.click(self.organization_button)
    # ------------------------------------------------------------------------------------------------------------------
    company_button = (By.XPATH, "//span[text()='Компании']")

    def click_company_button(self):
        self.click(self.company_button)
    # ------------------------------------------------------------------------------------------------------------------
    user_button = (By.XPATH, "//span[text()='Пользователи']")

    def click_user_button(self):
        self.click(self.user_button)
    # ------------------------------------------------------------------------------------------------------------------
