from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class OverloadIdEdit(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = By.XPATH, "(//div/h6)[1]"

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    name_input = By.XPATH, "id('anor724-input-text-name')/input"

    def input_name(self, name_elem):
        self.input_text(self.name_input, name_elem)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = By.XPATH, "id('anor724-button-save')"
    yes_button = By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
