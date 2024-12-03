from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class RoomList(BasePage):
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

    def find_row(self, room_name):
        self.find_row_and_click(element_name=room_name)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, '//button[@ng-click="view(row)"]')

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    attachment_button = (By.XPATH, '//button[@ng-click="attachment(row)"]')

    def click_attachment_button(self):
        self.click(self.attachment_button)
    # ------------------------------------------------------------------------------------------------------------------
