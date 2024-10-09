from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class OverloadIdView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = By.XPATH, "//div[@class='card-title']/h5/t"

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    overload_name = (By.XPATH, "id('anor1274-navbar-header-information')/div/span")

    def get_elements(self):
        return self.get_text(self.overload_name)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = By.XPATH, "id('anor1274-button-close')"

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
