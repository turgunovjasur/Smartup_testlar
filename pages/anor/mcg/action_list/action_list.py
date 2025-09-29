from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ActionList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "id('anor717-button-add')")

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, "//button[@id='anor717-button-add']")

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    status_many_button = (By.XPATH, "id('anor717-button-change_state_many')")
    passive_many_button = (By.XPATH, "id('anor717-button-change_state_many')/following-sibling::div/a[1]")
    click_status_yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_status_many_button(self):
        self.click(self.status_many_button)
        self.click(self.passive_many_button)
        self.click(self.click_status_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    delete_many_button = (By.XPATH, "id('anor717-button-delete_many')")
    click_delete_yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_delete_many_button(self):
        self.click(self.delete_many_button)
        self.click(self. click_delete_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, "//button[@id='anor717-button-view']")

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    edit_button = (By.XPATH, "id('anor717-button-edit')")

    def click_edit_button(self):
        self.click(self.edit_button)
    # ------------------------------------------------------------------------------------------------------------------
    status_one_button = (By.XPATH, "id('anor717-button-change_status_one')")
    click_inactive_button = (By.XPATH, "id('anor717-button-change_status_one')/following-sibling::div/a[1]")
    click_yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_status_one_button(self):
        self.click(self.status_one_button)
        self.click(self.click_inactive_button)
        self.click(self.click_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    action_delete_one_button = (By.XPATH, "id('anor717-button-delete_one')")
    click_yes_delete_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_delete_one_button(self):
        self.click(self.action_delete_one_button)
        self.click(self.click_yes_delete_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, action_name):
        self.find_row_and_click(element_name=action_name)
    # ------------------------------------------------------------------------------------------------------------------
    filter_button = (By.XPATH, "//button[@ng-click='openFilter()']")

    def click_filter_button(self):
        self.click(self.filter_button)
    # ------------------------------------------------------------------------------------------------------------------
    show_all_button = (By.XPATH, "//button[@ng-click='a.bGridFilter.showAll()']")

    def click_show_all_button(self):
        self.click(self.show_all_button)
    # ------------------------------------------------------------------------------------------------------------------
