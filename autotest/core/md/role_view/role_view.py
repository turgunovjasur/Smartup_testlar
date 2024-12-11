from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class RoleView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//div[@class="card-title"]/h3/t')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    navbar_button = (By.XPATH, '(//div[@class="navi-item mb-2"])[3]/a')

    def click_navbar_button(self):
        self.wait_for_page_load()
        self.click(self.navbar_button)
    # ------------------------------------------------------------------------------------------------------------------
    get_text_role = (By.XPATH, '(//div[@class="card-body pt-4"]//span[text()])[1]')

    def check_text(self):
        return self.get_text(self.get_text_role)
    # ------------------------------------------------------------------------------------------------------------------
    detached_button = (By.XPATH, '//button[@ng-class="q.classDetach"]')

    def click_detached_button(self):
        self.click(self.detached_button)
    # ------------------------------------------------------------------------------------------------------------------
    checkbox_form = (By.XPATH, '//b-grid[@required="form, form_name, has_action, access_type"]//div[@class="tbl-header"]//label[@class="checkbox mt-0"]')

    def click_checkbox_form(self):
        self.click(self.checkbox_form)
    # ------------------------------------------------------------------------------------------------------------------
    dropdown_button = (By.XPATH, '//button[@class="btn btn-primary dropdown-toggle"]')
    access_all_button = (By.XPATH, '//button[@class="btn btn-primary dropdown-toggle"]/following-sibling::ul/a[1]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_access_all_button(self):
        self.click(self.dropdown_button)
        self.click(self.access_all_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
