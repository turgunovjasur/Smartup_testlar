from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class FilialView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//h5/t[contains(text(),'Основная информация')]")

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    filial_text = (By.XPATH, '//div[@class="b-offcanvas-hide"]/span[1]')

    def check_filial_text(self):
        return self.get_text(self.filial_text)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
    navbar_button = (By.XPATH, '//div[contains(@class, "navi navi-bolder")]/div/a[@ng-if="fi.filial_projects"]')

    def click_navbar_button(self):
        self.click(self.navbar_button)
    # ------------------------------------------------------------------------------------------------------------------
    project_checkbox = (By.XPATH, '//b-subpage[@name="filial_projects"]//div[@class="card-header"]//span')

    def click_project_checkbox(self):
        self.click(self.project_checkbox)
        self.click(self.project_checkbox)
    # ------------------------------------------------------------------------------------------------------------------
    checkbox_save_button = (By.XPATH, '//button[@ng-click="checkSave()"]')

    def click_checkbox_button(self):
        for number in range(1, 14):
            checkbox_button = (By.XPATH, f'(//b-subpage[@name="filial_projects"]//div[@class="row"]//span)[{number}]')
            self.click(checkbox_button)
        self.click(self.checkbox_save_button)

    # ------------------------------------------------------------------------------------------------------------------
    close_button = By.XPATH, '//button[@ng-click="page.close()"]'

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
