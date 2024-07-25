import os

from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class BasePage:
    def __init__(self, driver, timeout=40):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click_element(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def input_text(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)
        element.click()

    def input_form_text(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        actions = ActionChains(self.driver)  # Elementni ko'rinadigan joyga olib kelish
        actions.move_to_element(element).perform()
        element.clear()
        element.send_keys(text, Keys.ENTER)

    def new_input(self, locator, text, elem):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)
        self.click_element(elem)

    def new_wait_input(self, locator, elem):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.send_keys(Keys.ENTER)
        self.wait.until(EC.element_to_be_clickable(elem))
        self.click_element(elem)

    def choice(self, locator, elem):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        self.click_element(element)

        second_element = self.wait.until(EC.visibility_of_element_located(elem))
        self.click_element(second_element)

    def get_text(self, locator):
        return self.find_element(locator).text

    def take_screenshot(self, name):
        # screenshots papkasini yaratish (agar mavjud bo'lmasa)
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        self.driver.save_screenshot(f"screenshots/{name}.png")
