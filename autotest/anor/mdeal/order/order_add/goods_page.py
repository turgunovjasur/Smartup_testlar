from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class OrderAddProduct(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header_text = (By.XPATH, "//div/h3/t[contains(text(), 'ТМЦ')]")

    def element_visible(self):
        return self.wait_for_element_visible(self.header_text)
    # ------------------------------------------------------------------------------------------------------------------
    product_text = (By.XPATH, '//b-input[@id="anor279_input-b_input-product_name_goods0"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div[1]')

    def get_product_text(self):
        """Sahifadagi mahsulot nomini olish"""
        self.click(self.name_input)
        full_text = self.get_text(self.product_text)
        return full_text.split()[0]
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
    next_step_button = (By.XPATH, "//button[@id='anor279-button-next_step']")

    def click_next_step_button(self):
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
            return False
        else:
            print('Action active!')
            return True
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
            return False
        else:
            print('Overload active!')
            return True
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory
    # ------------------------------------------------------------------------------------------------------------------
    inventory_button = (By.XPATH, "//ul[@id='anor279-ul-nav_tablist']/li[1]/a")

    def click_inventory_button(self):
        self.click(self.inventory_button)
    # ------------------------------------------------------------------------------------------------------------------
