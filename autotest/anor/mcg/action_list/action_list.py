from time import time
from selenium.common import StaleElementReferenceException
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
    add_button = By.XPATH, "//button[@id='anor717-button-add']"

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    status_many_button = By.XPATH, "id('anor717-button-change_state_many')"
    passive_many_button = By.XPATH, "id('anor717-button-change_state_many')/following-sibling::div/a[1]"
    click_status_yes_button = By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_status_many_button(self):
        self.click_circle(self.status_many_button)
        self.click(self.passive_many_button)
        self.click(self.click_status_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    delete_many_button = By.XPATH, "id('anor717-button-delete_many')"
    click_delete_yes_button = By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_delete_many_button(self):
        self.click_circle(self.delete_many_button)
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
        self.click_circle(self.status_one_button)
        self.click(self.click_inactive_button)
        self.click(self.click_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    action_delete_one_button = By.XPATH, "id('anor717-button-delete_one')"
    click_yes_delete_button = By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']"

    def click_delete_one_button(self):
        self.click_circle(self.action_delete_one_button)
        self.click(self.click_yes_delete_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Button: First element, Checkbox
    # ------------------------------------------------------------------------------------------------------------------
    action_list_first_elem = By.XPATH, "(//div[@class='tbl-row']/div[3])[1]"

    def click_first_elem_button(self):
        self.click_circle(self.action_list_first_elem)
    # ------------------------------------------------------------------------------------------------------------------
    checkbox_button = ".tbl-row:nth-child(1) span"

    def click_checkbox_button(self, checkbox_button):
        element = self.driver.find_element(By.CSS_SELECTOR, checkbox_button)
        self.driver.execute_script("arguments[0].click();", element)
    # ------------------------------------------------------------------------------------------------------------------
    # Button: Filter, Show all
    # ------------------------------------------------------------------------------------------------------------------
    filter_button = By.XPATH, "//button[@ng-click='openFilter()']"

    def click_filter_button(self):
        self.click_circle(self.filter_button)
    # ------------------------------------------------------------------------------------------------------------------
    show_all_button = By.XPATH, "//button[@ng-click='a.bGridFilter.showAll()']"

    def click_show_all_button(self):
        self.click_circle(self.show_all_button)
    # ------------------------------------------------------------------------------------------------------------------
    row_button = (By.CSS_SELECTOR, ".tbl-header-cell:nth-child(2) > .tbl-header-txt")

    def click_row_button(self):
        element = self.find_element(self.row_button)
        self.driver.execute_script("arguments[0].click();", element)
    # ------------------------------------------------------------------------------------------------------------------

    def find_and_click_checkbox(self, element_name, checkbox=False):
        find_elems_name_xpath = "//div[@class='tbl-body']//div[@class='tbl-row']//div[@class='tbl-cell'][1]"

        start_time = time()
        timeout_duration = 20

        while time() - start_time < timeout_duration:
            try:
                elements = self.driver.find_elements(By.XPATH, find_elems_name_xpath)
                # print("Element list:")

                found = False
                for elem in elements:
                    # print(f"Element text: {elem.text.strip()}")

                    if elem.text.strip() == element_name:
                        found = True
                        self.click(elem)
                        # print(f"'{element_name}' item found and pressed.")

                        # Checkbox
                        if checkbox:
                            parent_row = elem.find_element(By.XPATH, "./ancestor::div[contains(@class, 'tbl-row')]")
                            try:
                                checkbox_span = parent_row.find_element(By.CSS_SELECTOR, ".tbl-cell span")
                                self.driver.execute_script("arguments[0].click();", checkbox_span)
                                # print(f"'{element_name}' checkbox pressed.")
                            except StaleElementReferenceException:
                                print(f"'{element_name}' for checkbox stale element reference.")
                        return

                if not found:
                    print(f"'{element_name}' item not found, wanted again...")

            except StaleElementReferenceException:
                print("StaleElementReferenceException, elements updated...")

        print(f"'{element_name}' item not found, search deadline.")
    # ------------------------------------------------------------------------------------------------------------------
