from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class BalanceList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    balance_header = (By.XPATH, "//ul/li/a[contains(text(), 'Настройки сроков годности')]")

    def element_visible(self):
        assert "Настройки сроков годности" in self.get_text(self.balance_header), "'Balance' page did not open!"
    # ------------------------------------------------------------------------------------------------------------------
    count_number = (By.XPATH, "//div[@class='tbl-body']/div[@class='tbl-row'][3]/div[9]")

    def check_balance(self):
        return self.get_numeric_value(self.count_number)
    # ------------------------------------------------------------------------------------------------------------------
