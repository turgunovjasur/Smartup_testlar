import time
import pyautogui
from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class SalesWork(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    show_setting_button = (By.XPATH, '//button[@ng-click="q.show_setting = true"]')

    def click_show_setting(self):
        self.click(self.show_setting_button)
    # ------------------------------------------------------------------------------------------------------------------
    generate_button = (By.XPATH, '//button[@ng-click="generate()"]')

    def click_generate(self):
        self.click(self.generate_button)
    # ------------------------------------------------------------------------------------------------------------------
    def click_enter_windows(self):
        pyautogui.press('enter')
        self.logger.info("Enter bosildi!")
    # ------------------------------------------------------------------------------------------------------------------
    def input_file_name_windows(self, file_name):
        integer = f'{file_name}'
        for init in integer:
            pyautogui.write(init)
            time.sleep(0.1)
        self.logger.info(f"File name kiritildi: {file_name}")
    # ------------------------------------------------------------------------------------------------------------------
    # Setting
    # ------------------------------------------------------------------------------------------------------------------
    header_setting = (By.XPATH, '//button[@ng-click="q.show_setting = false"]')

    def element_visible_setting(self):
        return self.wait_for_element_visible(self.header_setting)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
