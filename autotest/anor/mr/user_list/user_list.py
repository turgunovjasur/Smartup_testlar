from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class UserList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="fi.add()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="fi.add()"]')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    reload_button = (By.XPATH, '//button[@ng-click="reload()"]')

    def click_reload_button(self):
        self.click(self.reload_button)
    # ------------------------------------------------------------------------------------------------------------------
    find_elems_name_xpath = (By.XPATH, '(//div[@class="tbl"]/div[2]/div/div[2])[1]')

    def find_natural_person_row(self, natural_person_name):
        self.find_row_and_click(element_name=natural_person_name)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = By.XPATH, '//button[@ng-click="view(row)"]'

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    roles_button = By.XPATH, '//li/a[@ng-click="a.openSibling(fs.url)" and contains(text(), \'Роли\')]'

    def click_roles_button(self):
        self.click(self.roles_button)
    # ------------------------------------------------------------------------------------------------------------------
