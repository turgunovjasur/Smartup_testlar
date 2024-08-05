from selenium.webdriver.common.by import By

from autotest.core.md.base_page import BasePage


class CreateOrderPage(BasePage):
    ##############################################################################
    create_order_header_xpath = "//div/h3/t[contains(text(), 'Основное')]"

    def element_visible(self, create_order_header_xpath):
        self.wait_for_element_visible((By.XPATH, create_order_header_xpath))

    ##############################################################################
    order_request = '1'
    order_request_xpath = "(//div/input[@placeholder = 'Поиск...'])[1]"
    room_xpath = "(//div/input[@placeholder='Поиск...'])[2]"
    robot_xpath = "(//div/input[@placeholder='Поиск...'])[3]"
    client_xpath = "(//div/input[@placeholder='Поиск...'])[4]"
    room_elem_xpath = '//*[@id="kt_content"]/div[2]/div/b-page/div/div/div/div/div/form[1]/div/div/div[3]/b-input/div/div[2]/div[1]/div[8]'
    robot_elem_xpath = '//*[@id="kt_content"]/div[2]/div/b-page/div/div/div/div/div/form[1]/div/div/div[4]/div[1]/b-input/div/div[2]/div[2]/div[1]'
    client_elem_xpath = '//*[@id="kt_content"]/div[2]/div/b-page/div/div/div/div/div/form[1]/div/div/div[5]/b-input/div/div[2]/div[2]/div[1]'

    def fill_form(self, order_request, order_request_xpath, room_xpath, robot_xpath, client_xpath,
                  room_elem, robot_elem, client_elem):
        self.input_text((By.XPATH, order_request_xpath), order_request)
        self.input_text_elem((By.XPATH, room_xpath), (By.XPATH, room_elem))
        self.input_text_elem((By.XPATH, robot_xpath), (By.XPATH, robot_elem))
        self.input_text_elem((By.XPATH, client_xpath), (By.XPATH, client_elem))

    ##############################################################################
    create_order_next_button_xpath = "//span/t[contains(text(), 'Далее')]"

    def click_button(self, create_order_next_button_xpath):
        self.wait_and_click((By.XPATH, create_order_next_button_xpath))
    ##############################################################################
