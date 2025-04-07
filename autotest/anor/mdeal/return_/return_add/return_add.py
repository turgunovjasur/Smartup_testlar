from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class ReturnAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    return_header = (By.XPATH, "//div/h3/t[contains(text(), 'Основная информация')]")

    def element_visible(self):
        return self.wait_for_element_visible(self.return_header)
    # ------------------------------------------------------------------------------------------------------------------
    order_deals_input = (By.XPATH, '//b-input[@name="order_deals"]//input')
    order_deals_options = (By.XPATH, '//b-input[@name="order_deals"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def input_order_deals(self, client_name):
        self.click_options(self.order_deals_input, self.order_deals_options, client_name)
    # ------------------------------------------------------------------------------------------------------------------
    room_input = (By.XPATH, '//b-input[@name="rooms"]//input')
    room_options = (By.XPATH, '//b-input[@name="rooms"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_room(self, room_name):
        self.clear_element(self.room_input)
        self.click_options(self.room_input, self.room_options, room_name)
    # ------------------------------------------------------------------------------------------------------------------
    robot_input = (By.XPATH, '//b-input[@name="robots"]//input')
    robot_options = (By.XPATH, '//b-input[@name="robots"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div[1]')

    def input_robot(self, robot_name):
        self.clear_element(self.robot_input)
        self.click_options(self.robot_input, self.robot_options, robot_name)
    # ------------------------------------------------------------------------------------------------------------------
    warehouse_input = (By.XPATH, '//b-input[@name="warehouses"]//input')
    warehouse_options = (By.XPATH, '//b-input[@name="warehouses"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def input_warehouse(self, warehouse_name):
        self.click_options(self.warehouse_input, self.warehouse_options, warehouse_name)
    # ------------------------------------------------------------------------------------------------------------------
    sub_filial_input = (By.XPATH, '//b-input[@name="subfilials"]//input')
    sub_filial_options = (By.XPATH, '//b-input[@name="subfilials"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_sub_filial(self, sub_filial_name):
        self.click_options(self.sub_filial_input, self.sub_filial_options, sub_filial_name)
    # ------------------------------------------------------------------------------------------------------------------
    persons_input = (By.XPATH, '//b-input[@name="persons"]//input')
    persons_options = (By.XPATH, '//b-input[@name="persons"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div[1]')

    def input_persons(self, client_name):
        self.click_options(self.persons_input, self.persons_options, client_name)
    # ------------------------------------------------------------------------------------------------------------------
    currencies_input = (By.XPATH, '//b-input[@name="currencies"]//input')
    currency_options = (By.XPATH, '//b-input[@name="currencies"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def input_currencies(self, currency_name):
        self.clear_element(self.currencies_input)
        self.click_options(self.currencies_input, self.currency_options, currency_name)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    inventory_products_input = (By.XPATH, '//b-input[@name="inventory_products"]//input')
    inventory_products_options = (By.XPATH, '//b-input[@name="inventory_products"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_inventory_products(self, product_name):
        self.click_options(self.inventory_products_input, self.inventory_products_options, product_name)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_quantity_input = (By.XPATH, '//b-pg-grid[@name="items"]//input[@ng-model="item.quantity"]')

    def input_inventory_quantity(self, product_quantity):
        self.input_text(self.inventory_quantity_input, product_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_price_input = (By.XPATH, '//b-pg-grid[@name="items"]//input[@ng-model="item.price"]')

    def input_inventory_price(self, product_price):
        self.input_text(self.inventory_price_input, product_price)
    # ------------------------------------------------------------------------------------------------------------------
    margin_value_input = (By.XPATH, '//b-pg-grid[@name="items"]//div[@ng-model="item.margin_value"]//span[@ng-click="$select.activate()"]')
    margin_value = (By.XPATH, '(//b-pg-grid[@name="items"]//span[contains(@class,"ui-select-choices-row-inner")])[2]')

    def click_margin_value(self):
        self.click(self.margin_value_input)
        self.click(self.margin_value)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    payment_types_input = (By.XPATH, '//b-input[@name="payment_types"]//input')
    payment_types_options = (By.XPATH, '//b-input[@name="payment_types"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_payment_types(self, payment_type_name):
        self.click_options(self.payment_types_input, self.payment_types_options, payment_type_name)
    # ------------------------------------------------------------------------------------------------------------------
    expeditors_input = (By.XPATH, '//b-input[@name="expeditors"]//input')
    expeditors_options = (By.XPATH, '//b-input[@name="expeditors"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_expeditors(self, expeditor_name):
        self.click_options(self.expeditors_input, self.expeditors_options, expeditor_name)
    # ------------------------------------------------------------------------------------------------------------------
    contracts_input = (By.XPATH, '//b-input[@name="contracts"]//input')
    contracts_options = (By.XPATH, '//b-input[@name="contracts"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_contracts(self, contract_name):
        self.click_options(self.contracts_input, self.contracts_options, contract_name)
    # ------------------------------------------------------------------------------------------------------------------
    note_input = (By.XPATH, '//form[@name="step2"]//textarea[@ng-model="d.note"]')

    def input_note(self, text):
        self.input_text(self.note_input, text)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    status_input = (By.XPATH, '//form[@name="step3"]//div[@ng-model="d.status"]')

    def input_status(self, status=1):
        self.click(self.status_input)
        status_options = (By.XPATH, f'//form[@name="step3"]//div[@ng-model="d.status"]//div[@role="option"][{status}]')
        self.click(status_options)
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = (By.XPATH, '//button[@ng-click="nextStep()"]')
    save_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_next_step_button(self, save_button=False):
        self.click(self.next_step_button)
        if save_button:
            self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
