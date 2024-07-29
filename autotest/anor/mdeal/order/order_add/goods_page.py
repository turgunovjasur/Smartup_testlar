from selenium.webdriver.common.by import By

from autotest.core.md.base_page import BasePage


class GoodsPage(BasePage):
    def element_visible(self, goods_page_header_xpath):
        self.wait_for_element_visible((By.XPATH, goods_page_header_xpath))

    def fill_form(self, name_input_xpath, name_elem_xpath, qty_input_xpath, qty):
        self.input_text_elem((By.XPATH, name_input_xpath), (By.XPATH, name_elem_xpath))
        self.input_text((By.XPATH, qty_input_xpath), qty)

    def click_button(self, goods_page_next_button_xpath):
        self.wait_and_click((By.XPATH, goods_page_next_button_xpath))