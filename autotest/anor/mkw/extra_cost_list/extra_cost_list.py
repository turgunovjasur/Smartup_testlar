from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By

from utils.exception import ElementNotClickableError, ElementInteractionError


class ExtraCostList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="add()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="add()"]')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, '//button[@ng-click="view(row)"]')

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    separate_button = (By.XPATH, '//button[@ng-click="seperate(row)"]')

    def click_separate_button(self):
        self.click(self.separate_button)
    # ------------------------------------------------------------------------------------------------------------------
    post_one_button = (By.XPATH, '//button[@ng-click="postOne(row)"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_post_one_button(self):
        self.click(self.post_one_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, note_text):
        try:
            self.find_row_and_click(element_name=note_text)
            return True
        except (ElementNotClickableError, ElementInteractionError) as e:
            self.logger.warning(f"'note_text' row not found! Error: {e}")
            return False
    # ------------------------------------------------------------------------------------------------------------------
