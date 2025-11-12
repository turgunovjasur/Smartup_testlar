from selenium.webdriver.common.by import By
from pages.core.md.base_page import BasePage


class PriceTypeList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    list_header = (By.XPATH, "//a[text()='Типы оплат']")

    def element_visible(self):
        self.wait_for_element_visible(self.list_header)
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
    view_button = (By.XPATH, "//button[@id='anor182-button-view']")

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    setting_button = (By.XPATH, '//button[@ng-click="settings(row)"]')

    def click_setting_button(self):
        self.click(self.setting_button)
    # ------------------------------------------------------------------------------------------------------------------
    edit_button = (By.XPATH, '//button[@id="anor182-button-first_func"]')

    def click_edit_button(self):
        self.click(self.edit_button)
    # ------------------------------------------------------------------------------------------------------------------
    price_tag_button = (By.XPATH, '//button[@ng-click="priceTag(row)"]')

    def click_price_tag_button(self):
        self.click(self.price_tag_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, price_type_name):
        self.find_row_and_click(element_name=price_type_name)
    # ------------------------------------------------------------------------------------------------------------------
