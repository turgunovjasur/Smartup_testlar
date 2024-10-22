from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ActionIdView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = By.XPATH, "//div[@class='card-title']/h5/t"

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    action_name = (By.XPATH, "id('anor1199-action_information')/div/span[1]")

    def get_elements(self):
        return self.get_text(self.action_name)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = By.XPATH, "//button[@id='anor1199-button-close']"

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
