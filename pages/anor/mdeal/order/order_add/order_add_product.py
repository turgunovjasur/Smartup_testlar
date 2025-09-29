import re
from selenium.webdriver.common.by import By
from pages.core.md.base_page import BasePage


class OrderAddProduct(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header_text = (By.XPATH, "//div/h3/t[contains(text(), 'ТМЦ')]")

    def element_visible(self):
        self.wait_for_element_visible(self.header_text)
    # ------------------------------------------------------------------------------------------------------------------
    setting_button = (By.XPATH, '//b-pg-controller[@name="goods_items"]//div[@role="group"]/button')
    setting_tbl_button = (By.XPATH, '//b-pg-controller[@name="goods_items"]//div[@role="group"]//a')

    def click_setting_button(self):
        self.click(self.setting_button)
        self.click(self.setting_tbl_button)
    # ------------------------------------------------------------------------------------------------------------------

    def input_name_product(self, product_name, warehouse_name, price_type_name, clear_input=False):
        if clear_input:
            self.clear_element(self.name_input)

        if self.click(self.name_input):
            element_list = self._wait_for_presence_all(self.name_options)

            for element in element_list:
                element_text = element.text
                parts = re.split(r'\s(?=[A-ZА-Я])', element_text, maxsplit=2)

                if (len(parts) == 3 and
                        parts[0].strip() == product_name and
                        parts[1].strip() == warehouse_name and
                        parts[2].strip() == price_type_name):
                    element.click()
                    break
    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, '//b-input[@id="anor279_input-b_input-product_name_goods0"]//div[@class="simple"]/input')
    name_options = (By.XPATH, '//b-input[@id="anor279_input-b_input-product_name_goods0"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div[1]')

    def input_name(self, product_name):
        self.click(self.name_input)
        element = self.wait_for_element_visible(self.name_options)
        element_text = element.text

        first_text = element_text.split()[0]
        assert first_text == product_name, f"Error: {first_text} != {product_name}"
        self.click(self.name_options)
    # ------------------------------------------------------------------------------------------------------------------
    quantity_input = (By.XPATH, "//input[@id='anor279_input-b_pg_col-quantity_0']")

    def input_quantity(self, product_quantity):
        self.input_text(self.quantity_input, product_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    # margin_value_input = (By.XPATH, '//div[@ng-model="item.margin_value"]//span[@ng-click="$select.activate()"]')
    margin_value_input = (By.XPATH, '//b-pg-grid//div[contains(@ng-model,".margin_value")]//span[@ng-click="$select.activate()"]')

    def click_percent_value_button(self, percent_value):
        self.click(self.margin_value_input)
        percent_value_button = (By.XPATH, f'//b-pg-grid//div[contains(@ng-model,".margin_value")]//div[contains(@class,"ui-select-choices-row")]/span[contains(text(),"{percent_value}")]')
        self.click(percent_value_button)
    # ------------------------------------------------------------------------------------------------------------------
    next_step_button = (By.XPATH, "//button[@id='anor279-button-next_step']")

    def click_next_step_button(self):
        self.click(self.next_step_button)
    # ------------------------------------------------------------------------------------------------------------------

    def click_nav_tablist_button(self, tablist_name):
        locator = (By.XPATH, f'//ul[@id="anor279-ul-nav_tablist"]/li//*[contains(text(),"{tablist_name}")]')
        self.click(locator)
    # ------------------------------------------------------------------------------------------------------------------
    action_checkbox_button = (By.XPATH, '//div[@id="actions"]//label[@class="switch"]')

    def click_action_checkbox_button(self):
        self.click(self.action_checkbox_button)
    # ------------------------------------------------------------------------------------------------------------------

    def get_action_name(self, action_name):
        action_name_locator = (By.XPATH, f'//div[@id="actions"]//div[@class="row"]//h4[contains(text(),"{action_name}")]')
        return self.get_text(action_name_locator)
    # ------------------------------------------------------------------------------------------------------------------
    select_button = (By.XPATH, '(//button[@id="anor279-button-select"])[1]')

    def click_select_button(self):
        self.click(self.select_button)
    # ------------------------------------------------------------------------------------------------------------------
    check_overload = (By.XPATH, "(//div[@id='overload']//div[@class='col-sm-15'])[1]")

    def overload_is_visible(self):
        element = self.wait_for_element_visible(self.check_overload)
        if element is None:
            print('Overload inactive!')
            return False
        else:
            print('Overload active!')
            return True
    # ------------------------------------------------------------------------------------------------------------------
