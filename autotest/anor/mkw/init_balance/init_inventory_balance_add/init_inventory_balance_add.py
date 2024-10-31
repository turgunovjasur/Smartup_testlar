import time

from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class InitInventoryBalanceAdd(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    # ------------------------------------------------------------------------------------------------------------------
    balance_number_input = (By.XPATH, '//input[@ng-model="d.balance_number"]')

    def input_balance_number(self, balance_number):
        self.input_text(self.balance_number_input, balance_number)
    # ------------------------------------------------------------------------------------------------------------------
    warehouse_name_input = (By.XPATH, '//input[@ng-model="d.warehouse_name"]')
    warehouse_elem = (By.XPATH, '//b-input[@model="d.warehouse_name | name"]//div[@class="hint-body ng-scope"]/div[2]')

    def input_warehouse_name(self):
        self.input_text_elem(self.warehouse_name_input, self.warehouse_elem)
    # ------------------------------------------------------------------------------------------------------------------
    product_name_input = (By.XPATH, '//input[@ng-model="item.product_name"]')
    product_elem = (By.XPATH, '//b-input[@model="item.product_name"]//div[@class="hint-body ng-scope"]/div[1]')

    def input_product_name(self):
        self.input_text_elem(self.product_name_input, self.product_elem)
    # ------------------------------------------------------------------------------------------------------------------
    card_code_input = (By.XPATH, '(//input[@ng-model="item.card_code"])[1]')

    def input_card_code(self, card_code):
        self.input_text(self.card_code_input, card_code)
    # ------------------------------------------------------------------------------------------------------------------
    quantity_input = (By.XPATH, '(//input[@ng-model="item.quantity"])[1]')

    def input_quantity(self, quantity):
        self.input_text(self.quantity_input, quantity)
    # ------------------------------------------------------------------------------------------------------------------
    price_input = (By.XPATH, '(//input[@ng-model="item.price"])[1]')

    def input_price(self, price):
        self.input_text(self.price_input, price)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-if="fi.save"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
        time.sleep(2)
    # ------------------------------------------------------------------------------------------------------------------
    reload_button = (By.XPATH, '//button[@ng-click="reload()"]')

    def click_reload_button(self):
        self.click(self.reload_button)
    # ------------------------------------------------------------------------------------------------------------------
    list_elements = (By.XPATH, "//div[@class='tbl-body']//div[@class='tbl-row']//div[@class='tbl-cell'][1]")

    def check_list_balance(self, elem_name):
        elements = self.driver.find_elements(*self.list_elements)
        found = False
        elem_name_str = str(elem_name).strip()

        for elem in elements:
            element_text = elem.text.strip()
            # print(f"Element number: {element_text}")

            if element_text == elem_name_str:
                elem.click()
                print(f"Clicked element: {element_text}")
                found = True
                break

        if not found:
            print("Element not found! in inventory balance list")
    # ------------------------------------------------------------------------------------------------------------------
    post_one_button = (By.XPATH, '//button[@ng-click="postOne(row)"]')
    yes_post_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_post_one_button(self):
        self.click(self.post_one_button)
        self.click(self.yes_post_button)
    # ------------------------------------------------------------------------------------------------------------------
