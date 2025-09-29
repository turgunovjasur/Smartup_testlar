import time
from selenium.webdriver.common.by import By
from pages.core.md.base_page import BasePage


class FilialView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//h5/t[contains(text(),'Основная информация')]")

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    filial_text = (By.XPATH, '//div[@class="b-offcanvas-hide"]/span[1]')

    def check_filial_text(self):
        return self.get_text(self.filial_text)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="checkSave()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
    navbar_button = (By.XPATH, '//div[contains(@class, "navi navi-bolder")]/div/a[@ng-if="fi.filial_projects"]')

    def click_navbar_button(self):
        self.click(self.navbar_button)
    # ------------------------------------------------------------------------------------------------------------------
    project_trade_checkbox = (By.XPATH, '//b-subpage[@name="filial_projects"]//div[@class="card-header"]//span[text()="trade"]/ancestor::label/input[@type="checkbox"]')
    project_anor_checkbox = (By.XPATH, '//b-subpage[@name="filial_projects"]//div[@class="card-header"]//span[text()="anor"]/ancestor::label/input[@type="checkbox"]')

    def click_project_checkbox(self):
        try:
            self.click_checkbox(self.project_anor_checkbox, state=False)
        except Exception as e:
            self.logger.warning(f"Anor proectni ochirishda xatolik: {str(e)}")
        self.click_checkbox(self.project_trade_checkbox, state=True)
    # ------------------------------------------------------------------------------------------------------------------
    def click_checkbox_button(self):
        xpath_string = '//span[text()="trade"]/ancestor::div[@class="card-header"]/following-sibling::div//span'
        checkboxes = self._wait_for_presence_all((By.XPATH, xpath_string))
        checkbox_quantity = len(checkboxes)

        for i in range(1, checkbox_quantity + 1):
            input_xpath = f'({xpath_string})[{i}]/ancestor::label/input[@type="checkbox"]'
            try:
                time.sleep(0.1)
                self.click_checkbox((By.XPATH, input_xpath), state=True)
            except Exception as e:
                self.logger.warning(f"Checkbox {i} da xatolik: {str(e)}")
                continue
    # ------------------------------------------------------------------------------------------------------------------
    close_button = By.XPATH, '//button[@ng-click="page.close()"]'

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------