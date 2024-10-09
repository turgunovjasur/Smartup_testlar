from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class FinalPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    payment_type_input = (By.XPATH, "(//div[@id='anor279-inpu-b_input-payment_type']//input)[2]")
    payment_elem = (By.XPATH, "//div[@id='anor279-inpu-b_input-payment_type']//div[@class='hint-body ng-scope']/div[1]")
    status_input = (By.XPATH, "(//div[@id='anor279-ui_select-status']//span)[1]")
    status_elem = (By.XPATH, "//div[@id='ui-select-choices-row-2-0']/span")

    def fill_form(self):
        self.input_text_elem(self.payment_type_input, self.payment_elem)
        self.input_text_elem(self.status_input, self.status_elem)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, "//button[@id='anor279-button-next_step']")
    yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
