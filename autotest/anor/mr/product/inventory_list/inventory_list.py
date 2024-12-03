from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class InventoryList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    # Header text: Inventory list
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list_header = (By.XPATH, "//button[@id='anor50-button-text-add']")

    def element_visible(self):
        return self.wait_for_element_visible(self.inventory_list_header)
    # ------------------------------------------------------------------------------------------------------------------
    # Toolbar: Add, Status, Delete many
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, "//button[@id='anor50-button-text-add']")

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    status_many_button = (By.XPATH, "id('anor50-button-change_state_many')/button")
    passive_many_button = (By.XPATH, "id('anor50-button-change_state_many')/div/a")
    click_status_yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_status_many_button(self):
        self.click(self.status_many_button)
        self.click(self.passive_many_button)
        self.click(self.click_status_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    delete_many_button = (By.XPATH, "id('anor50-button-delete_many')")
    click_delete_yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_delete_many_button(self):
        self.click(self.delete_many_button)
        self.click(self.click_delete_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Button: View, Edit, Inactive, Delete one
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, "//button[@id='anor50-button-view']")

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    edit_button = (By.XPATH, "id('anor50-button-edit')")

    def click_edit_button(self):
        self.click(self.edit_button)
    # ------------------------------------------------------------------------------------------------------------------
    status_one_button = (By.XPATH, "id('anor50-button-change_state')")
    click_yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_status_one_button(self):
        self.click(self.status_one_button)
        self.click(self.click_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    product_delete_one_button = (By.XPATH, "id('anor50-button-delete')")
    click_yes_delete_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_delete_one_button(self):
        self.click(self.product_delete_one_button)
        self.click(self.click_yes_delete_button)
    # ------------------------------------------------------------------------------------------------------------------
    set_price_button = (By.XPATH, '//button[@ng-click="set_price(row)"]')

    def click_set_price_button(self):
        self.click(self.set_price_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Button: First element, Checkbox
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list_first_elem = (By.XPATH, "(//div[@class='tbl-row']/div[3])[1]")

    def click_first_elem_button(self):
        self.click(self.inventory_list_first_elem)
    # ------------------------------------------------------------------------------------------------------------------
    checkbox_button = ".tbl-row:nth-child(1) span"

    def click_checkbox_button(self, checkbox_button):
        element = self.driver.find_element(By.CSS_SELECTOR, checkbox_button)
        self.driver.execute_script("arguments[0].click();", element)
    # ------------------------------------------------------------------------------------------------------------------
    # Button: Filter, Show all
    # ------------------------------------------------------------------------------------------------------------------
    filter_button = (By.XPATH, "//button[@ng-click='openFilter()']")

    def click_filter_button(self):
        self.click(self.filter_button)
    # ------------------------------------------------------------------------------------------------------------------
    show_all_button = (By.XPATH, "//button[@ng-click='a.bGridFilter.showAll()']")

    def click_show_all_button(self):
        self.click(self.show_all_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_and_click_checkbox(self, product_name):
        self.find_row_and_click(element_name=product_name)
    # ------------------------------------------------------------------------------------------------------------------
    set_price_button = (By.XPATH, "//button[@ng-click='set_price(row)']")

    def click_set_price_button(self):
        self.click(self.set_price_button)
    # ------------------------------------------------------------------------------------------------------------------
    navbar_button = (By.XPATH, "//ul[contains(@class,'breadcrumb')]/li[5]/a")

    def click_navbar_button(self):
        return self.click(self.navbar_button)
    # ------------------------------------------------------------------------------------------------------------------
