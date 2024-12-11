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

    def click_checkboxes(self):
        for i in range(2, 29):
            checkbox = (By.XPATH, f'(//label/span)[{i}]')
            try:
                self.click(checkbox)
                # time.sleep(0.5)
            except Exception as e:
                print(f"Checkbox {i} da xatolik: {str(e)}")
                continue
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
