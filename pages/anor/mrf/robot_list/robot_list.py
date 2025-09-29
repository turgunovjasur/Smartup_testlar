from selenium.webdriver.common.by import By
from pages.core.md.base_page import BasePage


class RobotList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="q.add_btn_dropdown.firstFn()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="q.add_btn_dropdown.firstFn()"]')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, robot_name):
        self.find_row_and_click(element_name=robot_name)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = By.XPATH, '//button[@ng-click="view(row)"]'

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
