from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ProductFileList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-if="fi.download_file"]/following-sibling::button')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-if="fi.download_file"]/following-sibling::button')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
