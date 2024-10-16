from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ReturnView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    return_header = (By.XPATH, "//li/a/span[contains(text(), 'Основная информация')]")

    def element_visible(self):
        assert "Основная информация" in self.get_text(self.return_header), "'ReturnView' page did not open!"
    # ------------------------------------------------------------------------------------------------------------------
    return_id = (By.XPATH, "(//div[@class='card-body']/div/div/div/div[@class='col-sm form-group'])[1]")
    order_id = (By.XPATH, "(//div[@class='card-body']/div/div/div/div[@class='col-sm form-group'])[5]")

    def get_elements(self):
        order_id = self.get_numeric_value(self.order_id)
        return_id = self.get_numeric_value(self.return_id)
        return order_id, return_id
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, "//button[@ng-click='page.close()']")

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
