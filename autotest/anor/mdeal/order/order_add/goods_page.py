import time
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class GoodsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.number = None
    # ------------------------------------------------------------------------------------------------------------------
    header_text = (By.XPATH, "//div/h3/t[contains(text(), 'ТМЦ')]")

    def element_visible(self):
        self.wait_for_element_visible(self.header_text)
    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, "(//b-input[@id='anor279_input-b_input-product_name_goods0']//input)[1]")
    name_elem = (By.XPATH, "//b-input[@id='anor279_input-b_input-product_name_goods0']//div[@class='hint-body ng-scope']/div[1]")
    quantity_input = (By.XPATH, "//input[@id='anor279_input-b_pg_col-quantity_0']")

    def fill_form(self, number):
        self.input_text_elem(self.name_input, self.name_elem)
        time.sleep(0.5)
        self.input_text(self.quantity_input, number)
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = (By.XPATH, "//button[@id='anor279-button-next_step']")

    def click_button(self):
        self.click(self.next_step_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Action
    # ------------------------------------------------------------------------------------------------------------------
    action_button = (By.XPATH, "//ul[@id='anor279-ul-nav_tablist']/li[7]/a")

    def click_action_button(self):
        self.click(self.action_button)
    # ------------------------------------------------------------------------------------------------------------------
    check_action = (By.XPATH, "//div[@id='actions']//label[@class='py-3 px-4']")

    def action_is_visible(self):
        element = self.wait_for_element_visible(self.check_action, timeout=2)
        if element is None:
            print('Action inactive!')
        else:
            print('Action active!')
    # ------------------------------------------------------------------------------------------------------------------
    # Overload
    # ------------------------------------------------------------------------------------------------------------------
    overload_button = (By.XPATH, "//ul[@id='anor279-ul-nav_tablist']/li[5]/a")

    def click_overload_button(self):
        self.click(self.overload_button)
    # ------------------------------------------------------------------------------------------------------------------
    check_overload = (By.XPATH, "(//div[@id='overload']//div[@class='col-sm-15'])[1]")

    def overload_is_visible(self):
        element = self.wait_for_element_visible(self.check_overload, timeout=2)
        if element is None:
            print('Overload inactive!')
        else:
            print('Overload active!')
    # ------------------------------------------------------------------------------------------------------------------
