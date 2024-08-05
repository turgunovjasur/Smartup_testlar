from selenium.webdriver.common.by import By

from autotest.core.md.base_page import BasePage


class GoodsPage(BasePage):
    ##############################################################################
    goods_page_header_xpath = "//div/h3/t[contains(text(), 'ТМЦ')]"

    def element_visible(self, goods_page_header_xpath):
        self.wait_for_element_visible((By.XPATH, goods_page_header_xpath))

    ##############################################################################
    name_input_xpath = "(//div/input[@placeholder='Поиск...'])[8]"
    name_elem_xpath = '/html/body/div[3]/div/div/div[2]/div[2]/div/b-page/div/div/div/div/div/form[2]/div/div/div/div[1]/div[2]/b-pg-grid/div/div/div[1]/div[2]/div[1]/div[1]/div/b-input/div/div[2]/div[2]/div[1]'
    qty_input_xpath = "(//div/input[@ng-if='item.product_id'])[1]"
    qty = '3'

    def fill_form(self, name_input_xpath, name_elem_xpath, qty_input_xpath, qty):
        self.input_text_elem((By.XPATH, name_input_xpath), (By.XPATH, name_elem_xpath))
        self.input_text((By.XPATH, qty_input_xpath), qty)

    ##############################################################################
    goods_page_next_button_xpath = "//span/t[contains(text(), 'Далее')]"

    def click_button(self, goods_page_next_button_xpath):
        self.wait_and_click((By.XPATH, goods_page_next_button_xpath))
##############################################################################
