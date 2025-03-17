from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class PriceTypeList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    list_header = (By.XPATH, "//a[text()='Типы оплат']")

    def element_visible(self):
        return self.wait_for_element_visible(self.list_header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, "//button[@id='anor182-button-add']")

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    add_dropdown_button = (By.XPATH, "//button[@id='anor182-button-add']/following-sibling::button")
    attachment_button = (By.XPATH, '//button[@id="anor182-button-add"]/following-sibling::div/a[1]')

    def click_add_dropdown_button(self):
        self.click(self.add_dropdown_button)
        self.click(self.attachment_button)
    # ------------------------------------------------------------------------------------------------------------------
    status_many_button = (By.XPATH, "id('anor182-button-change_state_many')")
    passive_many_button = (By.XPATH, "id('anor182-button-change_state_many')/following-sibling::div")
    click_status_yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_status_many_button(self):
        self.click(self.status_many_button)
        self.click(self.passive_many_button)
        self.click(self.click_status_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    delete_many_button = (By.XPATH, "id('anor182-button-delete_many')")
    click_delete_yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_delete_many_button(self):
        self.click(self.delete_many_button)
        self.click(self.click_delete_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, "//button[@id='anor182-button-view']")

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    edit_button = (By.XPATH, '//button[@id="anor182-button-first_func"]')

    def click_edit_button(self):
        self.click(self.edit_button)
    # ------------------------------------------------------------------------------------------------------------------
    price_tag_button = (By.XPATH, '//button[@ng-click="priceTag(row)"]')

    def click_price_tag_button(self):
        self.click(self.price_tag_button)
    # ------------------------------------------------------------------------------------------------------------------
    status_one_button = (By.XPATH, "id('anor182-button-change_state')")
    click_yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_status_one_button(self):
        self.click(self.status_one_button)
        self.click(self.click_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    product_delete_one_button = (By.XPATH, "id('anor182-button-delete_one')")
    click_yes_delete_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_delete_one_button(self):
        self.click(self.product_delete_one_button)
        self.click(self.click_yes_delete_button)
    # ------------------------------------------------------------------------------------------------------------------
    list_first_elem = (By.XPATH, "//div[@class='tbl-row'][1]/div[3]")

    def click_first_elem_button(self):
        self.click(self.list_first_elem)
    # ------------------------------------------------------------------------------------------------------------------
    code_button = By.CSS_SELECTOR, ".tbl-header-cell:nth-child(2) > .tbl-header-txt"

    def click_code_button(self):
        element = self.wait_for_element_visible(self.code_button)
        self.driver.execute_script("arguments[0].click();", element)
    # ------------------------------------------------------------------------------------------------------------------
    checkbox_button = ".tbl-row:nth-child(1) span"

    def click_checkbox_button(self, checkbox_button):
        element = self.driver.find_element(By.CSS_SELECTOR, checkbox_button)
        self.driver.execute_script("arguments[0].click();", element)
    # ------------------------------------------------------------------------------------------------------------------
    filter_button = (By.XPATH, "//button[@ng-click='openFilter()']")

    def click_filter_button(self):
        self.click(self.filter_button)
    # ------------------------------------------------------------------------------------------------------------------
    show_all_button = (By.XPATH, "//button[@ng-click='a.bGridFilter.showAll()']")

    def click_show_all_button(self):
        self.click(self.show_all_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, price_type_name):
        self.find_row_and_click(element_name=price_type_name)
    # ------------------------------------------------------------------------------------------------------------------
