import time
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class RoleEdit(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="save()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    checkbox_text = (By.XPATH, '(//label/span)[2]/t')

    def check_checkbox(self):
        text = self.get_text(self.checkbox_text)
        return text.lower() == 'да'
    # ------------------------------------------------------------------------------------------------------------------
    checkboxes = (By.XPATH, '//div[contains(@class,"mb-4")]//label/span')

    def checkbox_quantity(self):
        checkboxes = self._wait_for_presence_all(self.checkboxes)
        self.logger.info(f"Checkboxlar soni: {len(checkboxes)}")
    # ------------------------------------------------------------------------------------------------------------------

    def click_checkboxes(self):
        xpath_string = '//div[contains(@class,"mb-4")]//label/span'
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
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
