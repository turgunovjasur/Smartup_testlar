import time
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class PriceTypeList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    # Header text: Inventory list
    # ------------------------------------------------------------------------------------------------------------------
    list_header = "//a[text()='Типы оплат']"

    def element_visible(self, list_header):
        self.wait_for_element_visible((By.XPATH, list_header))
    # ------------------------------------------------------------------------------------------------------------------
    # Toolbar: Add, Status, Delete many
    # ------------------------------------------------------------------------------------------------------------------
    add_button = "id('anor182-button-add')"

    def click_add_button(self, add_button):
        self.click((By.XPATH, add_button))
    # ------------------------------------------------------------------------------------------------------------------
    status_many_button = "id('anor182-button-change_state_many')"
    passive_many_button = "id('anor182-button-change_state_many')/following-sibling::div"
    click_status_yes_button = "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_status_many_button(self, status_button, passive_many_button, click_status_yes_button, timeout=1):
        self.click((By.XPATH, status_button), timeout)
        self.click((By.XPATH, passive_many_button), timeout)
        self.click((By.XPATH, click_status_yes_button), timeout)
    # ------------------------------------------------------------------------------------------------------------------
    delete_many_button = "id('anor182-button-delete_many')"
    click_delete_yes_button = "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_delete_many_button(self, delete_many_button, click_delete_yes_button):
        self.click((By.XPATH, delete_many_button))
        self.click((By.XPATH, click_delete_yes_button))
    # ------------------------------------------------------------------------------------------------------------------
    # Button: View, Edit, Inactive, Delete one
    # ------------------------------------------------------------------------------------------------------------------
    view_button = "id('anor182-button-view')"

    def click_view_button(self, view_button):
        self.click((By.XPATH, view_button))
    # ------------------------------------------------------------------------------------------------------------------
    edit_button = "id('anor182-button-first_func')"

    def click_edit_button(self, edit_button):
        self.click((By.XPATH, edit_button))
    # ------------------------------------------------------------------------------------------------------------------
    status_one_button = "id('anor182-button-change_state')"
    click_yes_button = "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_status_one_button(self, status_one_button, click_yes_button):
        self.click((By.XPATH, status_one_button))
        self.click((By.XPATH, click_yes_button))
    # ------------------------------------------------------------------------------------------------------------------
    product_delete_one_button = "id('anor182-button-delete_one')"
    click_yes_delete_button = "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_delete_one_button(self, product_delete_one_button, click_yes_delete_button):
        self.click((By.XPATH, product_delete_one_button))
        self.click((By.XPATH, click_yes_delete_button))
    # ------------------------------------------------------------------------------------------------------------------
    # Button: First element, Checkbox
    # ------------------------------------------------------------------------------------------------------------------
    list_first_elem = "//div[@class='tbl-row'][1]/div[3]"

    def click_first_elem_button(self, list_first_elem):
        self.click((By.XPATH, list_first_elem))
    # ------------------------------------------------------------------------------------------------------------------
    code_button = ".tbl-header-cell:nth-child(2) > .tbl-header-txt"

    def click_code_button(self, code_button):
        element = self.driver.find_element(By.CSS_SELECTOR, code_button)
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(1)
    # ------------------------------------------------------------------------------------------------------------------
    checkbox_button = ".tbl-row:nth-child(1) span"

    def click_checkbox_button(self, checkbox_button):
        element = self.driver.find_element(By.CSS_SELECTOR, checkbox_button)
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(1)
    # ------------------------------------------------------------------------------------------------------------------
    # Button: Filter, Show all
    # ------------------------------------------------------------------------------------------------------------------
    filter_button = "//button[@ng-click='openFilter()']"

    def click_filter_button(self, filter_button, timeout=2):
        self.click((By.XPATH, filter_button), timeout)
    # ------------------------------------------------------------------------------------------------------------------
    show_all_button = "//button[@ng-click='a.bGridFilter.showAll()']"

    def click_show_all_button(self, show_all_button):
        self.click((By.XPATH, show_all_button))
    # ------------------------------------------------------------------------------------------------------------------
