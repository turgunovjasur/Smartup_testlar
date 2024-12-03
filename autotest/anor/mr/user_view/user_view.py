import time
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class UserView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//h3/t[contains(text(),'Основная информация')]")

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    natural_person_text = (By.XPATH, '//div[@class="b-offcanvas-hide"]/span[1]')

    def check_natural_person_text(self):
        return self.get_text(self.natural_person_text)
    # ------------------------------------------------------------------------------------------------------------------

    def click_navbar_button(self, navbar_button):
        forms_button = (By.XPATH, f'(//div[@class="navi-item mb-2"]/a)[{navbar_button}]')
        self.click(forms_button)
    # ------------------------------------------------------------------------------------------------------------------

    def click_tablist_button(self, tablist_button):
        tablist_button = (By.XPATH, f'((//ul[@role="tablist"])[2]/li/a)[{tablist_button}]')
        self.click(tablist_button)
    # ------------------------------------------------------------------------------------------------------------------

    def click_detached_button(self, detached_button):
        detached_button = (By.XPATH, f'(//button[@ng-class="q.classDetach"])[{detached_button}]')
        self.click(detached_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Forms:
    # ------------------------------------------------------------------------------------------------------------------
    aria_expand_button = (By.XPATH, '//b-grid-controller[@name="form_table" or @name="other_table"]//button[@class="btn btn-default rounded-0 ng-binding"]')
    limit_button = (By.XPATH, '//b-grid-controller[@name="form_table" or @name="other_table"]//a[@ng-click="changeLimit(500)"]')
    checkbox_form = (By.XPATH, '//b-grid[@required="form, form_name, has_action, access_type"]//div[@class="tbl-header"]//label[@class="checkbox mt-0"]')
    attach_form = (By.XPATH, '//button[@ng-click="attachChecked()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_aria_expand(self):
        self.click(self.aria_expand_button)

    def click_limit(self):
        self.click(self.limit_button)
        time.sleep(2)

    def click_checkbox_form(self):
        # self.wait_for_element_visible(self.checkbox_form)
        self.click(self.checkbox_form)

    def click_attach_form(self):
        self.click(self.attach_form)

    def click_yes_button(self):
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------

    def attach_forms(self):
        self.click_aria_expand()
        self.click_limit()
        self.click_checkbox_form()
        self.click_attach_form()
        self.click_yes_button()
    # ------------------------------------------------------------------------------------------------------------------
    # check_text = (By.XPATH, '//b-grid[@name="other_table" or @name="form_table"]//div[contains(@class, "tbl")]//div[@class="tbl-row tbl-no-data-row"]')
    check_text = (By.XPATH, '//b-grid[@name="other_table" or @name="form_table"]//div[contains(@class, "tbl")]//div[@class="tbl-row"][1]')

    def text_check(self):
        return self.wait_for_element_visible(self.check_text)
    # ------------------------------------------------------------------------------------------------------------------
    # Organization:
    # ------------------------------------------------------------------------------------------------------------------
    checkbox_filial = (By.XPATH, '//b-grid[@required="filial_id, name"]//div[@class="tbl-header"]//label[@class="checkbox mt-0"]')

    def click_checkbox_filial(self):
        self.click(self.checkbox_filial)
    # ------------------------------------------------------------------------------------------------------------------
    attach_filial = (By.XPATH, '//button[@ng-click="attachMany()"]')

    def click_attach_filial(self):
        self.click(self.attach_filial)
    # ------------------------------------------------------------------------------------------------------------------

    def attach_filials(self):
        self.click_checkbox_filial()
        self.click_attach_filial()
        self.click_yes_button()
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
