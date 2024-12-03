from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class RoomAttachment(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------

    def click_navbar_button(self, navbar_button):
        find_button = (By.XPATH, f'(//div[@class="navi navi-bolder navi-hover navi-active navi-link-rounded"]/div/a)[{navbar_button}]')
        self.click(find_button)
    # ------------------------------------------------------------------------------------------------------------------

    def click_detach_button(self, detach_button):
        find_button = (By.XPATH, f'(//button[@ng-class="q.classDetach"])[{detach_button}]')
        self.click(find_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, element_name):
        self.find_row_and_click(element_name)
    # ------------------------------------------------------------------------------------------------------------------
    checkbox_all = (By.XPATH, '(//b-grid[@name="table_payment_type"]//label)[1]')

    def click_checkbox_all(self, attach_button):
        attach_button = (By.XPATH, f'(//button[@ng-click="attachMany()"])[{attach_button}]')
        self.click(self.checkbox_all)
        self.click(attach_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_attach_button(self, attach_button):
        find_button = (By.XPATH, f'(//b-grid)[{attach_button}]//button[@ng-click="attachOne(row)"]')
        self.click(find_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
