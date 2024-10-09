import time

from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ActionList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, driver):
        super().__init__(driver)
    # ------------------------------------------------------------------------------------------------------------------
    # Header text: Action list
    # ------------------------------------------------------------------------------------------------------------------
    header = By.XPATH, "id('anor717-button-add')"

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # Toolbar: Add, Status, Delete many
    # ------------------------------------------------------------------------------------------------------------------
    add_button = By.XPATH, "id('anor717-button-add')"

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    status_many_button = By.XPATH, "id('anor717-button-change_state_many')"
    passive_many_button = By.XPATH, "id('anor717-button-change_state_many')/following-sibling::div/a[1]"
    click_status_yes_button = By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_status_many_button(self):
        self.click(self.status_many_button)
        self.click(self.passive_many_button)
        self.click(self.click_status_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    delete_many_button = By.XPATH, "id('anor717-button-delete_many')"
    click_delete_yes_button = By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_delete_many_button(self):
        self.click(self.delete_many_button)
        self.click(self. click_delete_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Button: View, Edit, Inactive, Delete one
    # ------------------------------------------------------------------------------------------------------------------
    view_button = By.XPATH, "id('anor717-button-view')"

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    edit_button = By.XPATH, "id('anor717-button-edit')"

    def click_edit_button(self):
        self.click(self.edit_button)
    # ------------------------------------------------------------------------------------------------------------------
    status_one_button = By.XPATH, "id('anor717-button-change_status_one')"
    click_inactive_button = By.XPATH, "id('anor717-button-change_status_one')/following-sibling::div/a[1]"
    click_yes_button = By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_status_one_button(self):
        self.click(self.status_one_button)
        self.click(self.click_inactive_button)
        self.click(self.click_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    action_delete_one_button = By.XPATH, "id('anor717-button-delete_one')"
    click_yes_delete_button = By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_delete_one_button(self):
        self.click(self.action_delete_one_button)
        self.click(self.click_yes_delete_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Button: First element, Checkbox
    # ------------------------------------------------------------------------------------------------------------------
    action_list_first_elem = By.XPATH, "(//div[@class='tbl-row']/div[3])[1]"

    def click_first_elem_button(self):
        time.sleep(2)
        self.click(self.action_list_first_elem)
    # ------------------------------------------------------------------------------------------------------------------
    checkbox_button = ".tbl-row:nth-child(1) span"

    def click_checkbox_button(self, checkbox_button):
        time.sleep(2)
        element = self.driver.find_element(By.CSS_SELECTOR, checkbox_button)
        self.driver.execute_script("arguments[0].click();", element)
    # ------------------------------------------------------------------------------------------------------------------
    # Button: Filter, Show all
    # ------------------------------------------------------------------------------------------------------------------
    filter_button = By.XPATH, "//button[@ng-click='openFilter()']"

    def click_filter_button(self):
        time.sleep(2)
        self.click(self.filter_button)

    # ------------------------------------------------------------------------------------------------------------------
    show_all_button = By.XPATH, "//button[@ng-click='a.bGridFilter.showAll()']"

    def click_show_all_button(self):
        self.click(self.show_all_button)
    # ------------------------------------------------------------------------------------------------------------------
