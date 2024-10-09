from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class InputList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    input_list_header = (By.XPATH, "//div[@id='kt_content']/descendant::h6")

    def element_visible(self):
        self.wait_for_element_visible(self.input_list_header)
    # ------------------------------------------------------------------------------------------------------------------
    create_button = (By.XPATH, "//button[@id='anor113-button-add']")

    def click_button(self):
        self.click(self.create_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Input_id
    # ------------------------------------------------------------------------------------------------------------------
    date_button = (By.XPATH, "//div[contains(text(), 'Время')]")

    def click_2x(self):
        self.click_multiple_time(self.date_button, click_count=2, delay=1)
        # ------------------------------------------------------------------------------------------------------------------
    first_element = (By.XPATH, "//div[@class='tbl-row'][1]/div[3]")
    view_button = (By.XPATH, "//button[@id='anor113-button-view']")

    def fill_form(self):
        self.click(self.first_element)
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
