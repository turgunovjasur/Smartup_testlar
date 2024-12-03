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
    checkbox_text = (By.XPATH, '//form[@name="form"]//div[@class="form-row"][2]//span/tdev[@key]')

    def check_checkbox(self):
        element = self.driver.find_element(self.checkbox_text)
        try:
            key_value = element.get_attribute('key')
            return key_value.lower() == 'yes'
        except:
            return False
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
