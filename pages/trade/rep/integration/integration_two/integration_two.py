from datetime import datetime
from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class IntegrationTwo(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    show_setting_button = (By.XPATH, '//button[@ng-click="q.show_setting = true"]')

    def click_show_setting(self):
        self.click(self.show_setting_button)
    # ------------------------------------------------------------------------------------------------------------------
    generate_button = (By.XPATH, '//button[@ng-click="generate()"]')

    def click_generate(self):
        self._wait_for_all_loaders()
        self.click(self.generate_button)
    # ------------------------------------------------------------------------------------------------------------------
    date_input = (By.XPATH, '//input[@ng-model="d.date"]')

    def input_date(self):
        date = datetime.now().strftime("%d.%m.%Y")
        self.input_text(self.date_input, date)
    # ------------------------------------------------------------------------------------------------------------------
    biruniAlert = (By.XPATH, '//div[@id="biruniAlert" and @class="modal fade show"]')
    modal = (By.XPATH, '//div[@id="biruniAlert"]//div[@class="modal-content"]')
    cancel_modal_button = (By.XPATH, '//div[@id="biruniAlert"]//button[not(@aria-label="Close") and @data-dismiss="modal"]')

    def check_error_modal(self):
        if self.wait_for_element(self.modal, wait_type="visibility"):
            self.logger.info("Error Modal korindi")
            self.click(self.cancel_modal_button)
        else:
            self.logger.info("Modal korinmadi")
    # ------------------------------------------------------------------------------------------------------------------

    def click_exchange_mode(self, exchange_file):
        exchange_mode = (By.XPATH, f'(//input[@type="radio" and @ng-model="d.exchange_mode"]/following-sibling::span)[{exchange_file}]')
        self.click(exchange_mode)
    # ------------------------------------------------------------------------------------------------------------------
    # Setting
    # ------------------------------------------------------------------------------------------------------------------
    header_setting = (By.XPATH, '//button[@ng-click="q.show_setting = false"]')

    def element_visible_setting(self):
        return self.wait_for_element_visible(self.header_setting)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
    company_id_input = (By.XPATH, '//input[@ng-model="d.company_id"]')

    def input_company_id(self, company_id):
        self.input_text(self.company_id_input, company_id)
    # ------------------------------------------------------------------------------------------------------------------
    user_name_input = (By.XPATH, '//input[@ng-model="d.user_name"]')

    def input_user_name(self, user_name):
        self.input_text(self.user_name_input, user_name)
    # ------------------------------------------------------------------------------------------------------------------
    url_input = (By.XPATH, '//input[@ng-model="d.url"]')

    def input_url(self, url):
        self.input_text(self.url_input, url)
    # ------------------------------------------------------------------------------------------------------------------
    price_types_input = (By.XPATH, '//b-input[@name="price_types"]//input')
    price_type_options = (By.XPATH, '//b-input[@name="price_types"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]')

    def input_price_types(self, price_type_name):
        self.clear_element(self.price_types_input)
        self.click_options(self.price_types_input, self.price_type_options, price_type_name)
    # ------------------------------------------------------------------------------------------------------------------
    edit_person_button= (By.XPATH, '//input[@ng-model="d.edit_person"]')

    def click_edit_person(self):
        self.click_checkbox(self.edit_person_button, state=True)
    # ------------------------------------------------------------------------------------------------------------------
    ignore_updated_deals_button= (By.XPATH, '//input[@ng-model="d.ignore_updated_deals"]')

    def click_ignore_updated_deals(self):
        self.click_checkbox(self.ignore_updated_deals_button, state=True)
    # ------------------------------------------------------------------------------------------------------------------
    show_owner_person_code_button= (By.XPATH, '//input[@ng-model="d.show_owner_person_code"]')

    def click_show_owner_person_code(self):
        self.click_checkbox(self.show_owner_person_code_button, state=True)
    # ------------------------------------------------------------------------------------------------------------------
    send_all_deals_button= (By.XPATH, '//input[@ng-model="d.send_all_deals"]')

    def click_send_all_deals(self):
        self.click_checkbox(self.send_all_deals_button, state=True)
    # ------------------------------------------------------------------------------------------------------------------
