from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ServicesList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    # Header text: List
    # ------------------------------------------------------------------------------------------------------------------
    list_header = "id('anor50-button-add')"

    def element_visible(self, list_header):
        self.wait_for_element_visible((By.XPATH, list_header))
    # ------------------------------------------------------------------------------------------------------------------
    # Toolbar: Add, Status, Delete many
    # ------------------------------------------------------------------------------------------------------------------
    add_button = "id('anor50-button-add')"

    def click_add_button(self, add_button):
        self.click((By.XPATH, add_button))
    # ------------------------------------------------------------------------------------------------------------------
    status_many_button = "id('anor50-button-change_state_many')"
    passive_many_button = "id('anor50-button-change_state_many')/following-sibling::div"
    status_yes_button = "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_status_many_button(self, status_button, passive_many_button, status_yes_button):
        self.click((By.XPATH, status_button))
        self.click((By.XPATH, passive_many_button))
        self.click((By.XPATH, status_yes_button))
    # ------------------------------------------------------------------------------------------------------------------
    delete_many_button = "id('anor50-button-delete_many')"
    delete_yes_button = "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_delete_many_button(self, delete_many_button, delete_yes_button):
        self.click((By.XPATH, delete_many_button))
        self.click((By.XPATH, delete_yes_button))
    # ------------------------------------------------------------------------------------------------------------------
    # Button: View, Edit, Inactive, Delete one
    # ------------------------------------------------------------------------------------------------------------------
    view_button = "id('anor50-button-view')"

    def click_view_button(self, view_button):
        self.click((By.XPATH, view_button))
    # ------------------------------------------------------------------------------------------------------------------
    edit_button = "id('anor50-button-edit')"

    def click_edit_button(self, edit_button):
        self.click((By.XPATH, edit_button))
    # ------------------------------------------------------------------------------------------------------------------
    status_one_button = "id('anor50-button-change_state_one')"
    click_yes_button = "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_status_one_button(self, change_state_button, click_yes_button):
        self.click((By.XPATH, change_state_button))
        self.click((By.XPATH, click_yes_button))
    # ------------------------------------------------------------------------------------------------------------------
    product_delete_one_button = "id('anor50-button-delete_one')"
    click_yes_delete_button = "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_delete_one_button(self, product_delete_one_button, click_yes_delete_button):
        self.click((By.XPATH, product_delete_one_button))
        self.click((By.XPATH, click_yes_delete_button))
    # ------------------------------------------------------------------------------------------------------------------
    # Button: First element, Checkbox
    # ------------------------------------------------------------------------------------------------------------------
    list_first_elem = "id('anor50-b_grid-table')//div[@class='tbl-row']/div[2]"

    def click_first_elem_button(self, list_first_elem):
        self.click((By.XPATH, list_first_elem))
    # ------------------------------------------------------------------------------------------------------------------
    checkbox_button = ".tbl-cell span"

    def click_checkbox_button(self, checkbox_button):
        element = self.driver.find_element(By.CSS_SELECTOR, checkbox_button)
        self.driver.execute_script("arguments[0].click();", element)
    # ------------------------------------------------------------------------------------------------------------------
    # Button: Filter, Show all
    # ------------------------------------------------------------------------------------------------------------------
    filter_button = "//button[@ng-click='openFilter()']"

    def click_filter_button(self, filter_button, timeout=20):
        self.click((By.XPATH, filter_button), timeout)
    # ------------------------------------------------------------------------------------------------------------------
    show_all_header = "id('biruniGridFilterModalLabel')"
    show_all_button = "//button[@ng-click='a.bGridFilter.showAll()']"

    def click_show_all_button(self, show_all_button, show_all_header, timeout=20):
        self.wait_for_element_visible((By.XPATH, show_all_header))
        self.click((By.XPATH, show_all_button), timeout)
    # ------------------------------------------------------------------------------------------------------------------
