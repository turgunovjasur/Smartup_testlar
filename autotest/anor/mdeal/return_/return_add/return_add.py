from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ReturnAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    return_header = (By.XPATH, "//div/h3/t[contains(text(), 'Основная информация')]")

    def element_visible(self):
        assert "Основная информация" in self.get_text(self.return_header), "'Return' page did not open!"
    # ------------------------------------------------------------------------------------------------------------------
    warehouse_input = (By.XPATH, "(//div[@class='b-input'])[5]//input")
    warehouse_elem = (By.XPATH, "(//div[@class='b-input'])[5]//div[@class='hint-body ng-scope']/div[1]")

    def input_warehouse(self):
        self.input_text_elem(self.warehouse_input, self.warehouse_elem)
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = (By.XPATH, "//button[@b-hotkey='finish']")
    save_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")
    quantity_return = (By.XPATH, "//div[@id='view_items']/b-pg-grid//div[@class='tbl-row ng-scope']/div[6]")

    def next_step_and_get_quantity(self):
        self.click_multiple_time(self.next_step_button, click_count=3, delay=1)
        return self.get_numeric_value(self.quantity_return)
    # ------------------------------------------------------------------------------------------------------------------

    def click_finish_button(self):
        self.click(self.next_step_button)
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
