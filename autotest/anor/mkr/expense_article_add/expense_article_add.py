from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ExpenseArticleAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '(//button[@ng-click="page.close()"])[2]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, '//input[@ng-model="d.name"]')

    def input_name(self, expense_article_name):
        self.input_text(self.name_input, expense_article_name)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '(//button[@ng-click="save()"])[2]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------

