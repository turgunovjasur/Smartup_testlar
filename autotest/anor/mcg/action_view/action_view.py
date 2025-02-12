from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ActionIdView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = By.XPATH, '//button[@id="anor1199-button-close"]'

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    get_action_name = (By.XPATH, '//div[@id="anor1199-action_information"]//span[1]')

    def get_elements(self):
        return self.get_text(self.get_action_name)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = By.XPATH, "//button[@id='anor1199-button-close']"

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
