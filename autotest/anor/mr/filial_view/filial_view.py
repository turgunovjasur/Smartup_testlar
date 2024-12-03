from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class FilialView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//h5/t[contains(text(),'Основная информация')]")

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    filial_text = By.XPATH, '//div[@class="b-offcanvas-hide"]/span[1]'

    def check_filial_text(self):
        return self.get_text(self.filial_text)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = By.XPATH, '//button[@ng-click="save()"]'

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = By.XPATH, '//button[@ng-click="page.close()"]'

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
