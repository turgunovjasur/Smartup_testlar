from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ReturnView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    return_header = (By.XPATH, "//li/a/span[contains(text(), 'Основная информация')]")

    def element_visible(self):
        return self.wait_for_element_visible(self.return_header)
    # ------------------------------------------------------------------------------------------------------------------
    get_quantity = (By.XPATH, '//b-pg-grid[@name="items0"]/following-sibling::div//t[contains(text(),"Общее количество")]/parent::div')
    get_margin = (By.XPATH, '//b-pg-grid[@name="items0"]/following-sibling::div//t[contains(text(), "скидки/наценки")]/parent::div')
    get_sum = (By.XPATH, '(//b-pg-grid[@name="items0"]/following-sibling::div//t[contains(text(), "Итого сумма")]/parent::div)[2]')

    def check_items(self):
        quantity = self.get_numeric_value(self.get_quantity)
        margin = self.get_numeric_value(self.get_margin)
        total_sum = self.get_numeric_value(self.get_sum)
        return quantity, margin, total_sum
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, "//button[@ng-click='page.close()']")

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
