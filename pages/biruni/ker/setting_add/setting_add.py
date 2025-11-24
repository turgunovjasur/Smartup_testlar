import time
from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class SettingAdd(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="save()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    form_name_input = (By.XPATH, '//input[@ng-model="d.form_name"]')
    options_form_name = (By.XPATH, '//b-input[@name="origin"]//div[contains(@class,"hint")]//div[contains(@class,"hint-item")]/div/div[1]')

    def input_form_name(self, form_name):
        self.click_options(self.form_name_input, self.options_form_name, form_name)
    # ------------------------------------------------------------------------------------------------------------------
    name_input = (By.XPATH, '//input[@ng-model="d.name"]')

    def input_template_name(self, template_name):
        self.input_text(self.name_input, template_name)
    # ------------------------------------------------------------------------------------------------------------------
    template_input = (By.XPATH, '//b-dropzone[@name="template"]//div[contains(@class,"d-flex")]')

    def click_template_input(self):
        self.click(self.template_input)
        time.sleep(2)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
    FILE_INPUT_LOCATOR = (By.CSS_SELECTOR, "input[type='file']")

    def upload_template_file(self, file_path):
        """Template faylini yuklash"""
        try:
            file_input = self.wait_for_element(self.FILE_INPUT_LOCATOR, wait_type="presence")

            # Agar element yashirilgan bo'lsa
            self.driver.execute_script("""
                arguments[0].style.display = 'block';
                arguments[0].style.visibility = 'visible';
                arguments[0].style.opacity = '1';
                arguments[0].style.height = 'auto';
                arguments[0].style.width = 'auto';
            """,
            file_input)

            file_input.send_keys(file_path)
            self.logger.info(f"[UPLOAD FILE]: {file_path}")

        except Exception as e:
            self.logger.error(f"[UPLOAD ERROR]: {e}")
            raise
    # ------------------------------------------------------------------------------------------------------------------
