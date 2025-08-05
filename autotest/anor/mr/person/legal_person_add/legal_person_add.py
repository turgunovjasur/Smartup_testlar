import time
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class LegalPersonAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, '//input[@ng-model="d.name" and @ng-change="validateName()"]')

    def input_name(self, legal_person_name):
        self.input_text(self.name_input, legal_person_name)
    # ------------------------------------------------------------------------------------------------------------------
    short_name_input = (By.XPATH, '//input[@ng-model="d.short_name"]')

    def input_short_name(self, legal_person_short_name):
        self.input_text(self.short_name_input, legal_person_short_name)
    # ------------------------------------------------------------------------------------------------------------------
    state_switch = (By.XPATH, '//input[@ng-model="d.state"]')

    def switch_state(self, state):
        self.click_checkbox(self.state_switch, state=state)
    # ------------------------------------------------------------------------------------------------------------------
    main_phone_input = (By.XPATH, '//input[@ng-model="d.details.main_phone"]')

    def input_main_phone(self, main_phone):
        self.input_text(self.main_phone_input, main_phone)
    # ------------------------------------------------------------------------------------------------------------------
    telegram_input = (By.XPATH, '//input[@ng-model="d.details.telegram"]')

    def input_telegram(self, telegram):
        self.input_text(self.telegram_input, telegram)
    # ------------------------------------------------------------------------------------------------------------------
    email_input = (By.XPATH, '//input[@ng-model="d.email"]')

    def input_email(self, email):
        self.input_text(self.email_input, email)
    # ------------------------------------------------------------------------------------------------------------------
    address_input = (By.XPATH, '//textarea[@ng-model="d.details.address"]')

    def input_address(self, address):
        self.input_text(self.address_input, address)
    # ------------------------------------------------------------------------------------------------------------------
    post_address_input = (By.XPATH, '//textarea[@ng-model="d.details.post_address"]')

    def input_post_address(self, post_address):
        self.input_text(self.post_address_input, post_address)
    # ------------------------------------------------------------------------------------------------------------------
    tin_input = (By.XPATH, '//input[@ng-model="d.details.tin"]')

    def input_tin(self, tin):
        self.input_text(self.tin_input, tin)
    # ------------------------------------------------------------------------------------------------------------------
    cea_input = (By.XPATH, '//input[@ng-model="d.details.cea"]')

    def input_cea(self, cea):
        self.input_text(self.cea_input, cea)
    # ------------------------------------------------------------------------------------------------------------------
    vat_code_input = (By.XPATH, '//input[@ng-model="d.details.vat_code"]')

    def input_vat_code(self, vat_code):
        self.input_text(self.vat_code_input, vat_code)
    # ------------------------------------------------------------------------------------------------------------------
    lat_lng_button = (By.XPATH, '//button[@ng-click="selectLatLng(d.latlng, \'main\')"]')
    lat_lng_input = (By.XPATH, '//input[@ng-model="q.search_lat_lng"]')
    map_model_kind_button = (By.XPATH, '//button[@ng-click="saveLatLng(q.map_model_kind)"]')

    def input_latlng(self, lat_lng):
        self.click(self.lat_lng_button)
        self.input_text(self.lat_lng_input, lat_lng)
        self.click(self.map_model_kind_button)
        self.click(self.map_model_kind_button)
    # ------------------------------------------------------------------------------------------------------------------
    address_guide_input = (By.XPATH, '//textarea[@ng-model="d.details.address_guide"]')

    def input_address_guide(self, address_guide):
        self.input_text(self.address_guide_input, address_guide)
    # ------------------------------------------------------------------------------------------------------------------
    code_input = (By.XPATH, '//input[@ng-model="d.code"]')

    def input_code(self, code):
        self.input_text(self.code_input, code)
    # ------------------------------------------------------------------------------------------------------------------
    web_input = (By.XPATH, '//input[@ng-model="d.details.web"]')

    def input_web(self, web):
        self.input_text(self.web_input, web)
    # ------------------------------------------------------------------------------------------------------------------
    barcode_input = (By.XPATH, '//input[@ng-model="d.details.barcode"]')

    def input_barcode(self, barcode):
        self.input_text(self.barcode_input, barcode)
    # ------------------------------------------------------------------------------------------------------------------
    zip_code_input = (By.XPATH, '//input[@ng-model="d.details.zip_code"]')

    def input_zip_code(self, zip_code):
        self.input_text(self.zip_code_input, zip_code)
    # ------------------------------------------------------------------------------------------------------------------
    legal_persons_input = (By.XPATH, '//b-input[@name="legal_persons"]//input[@ng-model="d.parent_person_name"]')
    options_locator = (By.XPATH, '//b-input[@name="legal_persons"]//div[contains(@class,"hint-item")]//div[contains(@class,"form-row")]/div')

    def input_legal_persons(self, element):
        self.click_options(self.legal_persons_input, self.options_locator, element)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_save_button(self):
        self.click(self.save_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
