from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class CompanyView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//h5/t[contains(text(),'Информация')]")

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    company_text = (By.XPATH, '//div[@class="b-offcanvas-hide"]/span[1]')

    def check_filial_text(self):
        return self.get_text(self.company_text)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
    navbar_button = (By.XPATH, '//div[@class="navi-item mb-2"][3]/a')

    def click_navbar_button(self):
        self.click(self.navbar_button)
    # ------------------------------------------------------------------------------------------------------------------
    checkbox_1 = (By.XPATH, '(//div[@class="col-sm-12"]//input[@type="checkbox"]/following-sibling::span)[1]')
    checkbox_3 = (By.XPATH, '(//div[@class="col-sm-12"]//input[@type="checkbox"]/following-sibling::span)[3]')

    def click_checkbox(self):
        self.click(self.checkbox_1)
        self.click(self.checkbox_3)
    # ------------------------------------------------------------------------------------------------------------------
