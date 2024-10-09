from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class OrderView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//div[@class='card-title']/h5/t")

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    order_id = (By.XPATH, "(//div[@class='card-body']/div/div/div/div[@class='col-sm'])[1]")

    def get_elements(self):
        return self.get_numeric_value(self.order_id)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, "//button[@id='trade82-button-close']")

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
