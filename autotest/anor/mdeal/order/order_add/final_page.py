from selenium.webdriver.common.by import By

from autotest.core.md.base_page import BasePage


class FinalPage(BasePage):
    ##############################################################################
    payment_type_input_xpath = '//*[@id="kt_content"]/div[2]/div/b-page/div/div/div/div/div/form[3]/div/div[' \
                               '2]/div/div/div[2]/b-input/div/div[1]/div/input'
    payment_elem_xpath = '//*[@id="kt_content"]/div[2]/div/b-page/div/div/div/div/div/form[3]/div/div[2]/div/div/div[' \
                         '2]/b-input/div/div[2]/div[1]/div/div'
    status_input_xpath = "(//div/span[@class = 'btn btn-default form-control ui-select-toggle'])[3]"
    status_elem_xpath = '//*[@id="ui-select-choices-row-1-0"]/span'

    def fill_form(self, payment_type_input_xpath, payment_elem_xpath,
                  status_input_xpath, status_elem_xpath):
        self.input_text_elem((By.XPATH, payment_type_input_xpath), (By.XPATH, payment_elem_xpath))
        self.input_text_elem((By.XPATH, status_input_xpath), (By.XPATH, status_elem_xpath))

    ##############################################################################
    save_button_xpath = "//span/t[contains(text(), 'Сохранить')]"
    yes_button_xpath = "//div/button[contains(text(), 'да')]"

    def click_save_button(self, save_button_xpath, yes_button_xpath):
        self.click((By.XPATH, save_button_xpath))
        self.click((By.XPATH, yes_button_xpath))
    ##############################################################################
