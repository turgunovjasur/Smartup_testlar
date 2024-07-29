import os
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10

    def find_element(self, locator):
        """Berilgan lokator bo'yicha elementni topadi."""

        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        """Berilgan lokator bo'yicha barcha elementlarni topadi."""

        return self.driver.find_elements(*locator)

    def click(self, locator):
        """Berilgan lokator bo'yicha elementni topib, unga bosadi."""

        self.find_element(locator).click()

    def send_keys(self, locator, text):
        """Berilgan lokator bo'yicha elementni topib, unga matn kiritadi."""

        self.find_element(locator).send_keys(text)

    def clear_and_send_keys(self, locator, text):
        """Berilgan lokator bo'yicha elementni topib,
        uni tozalaydi va yangi matn kiritadi."""

        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def is_element_present(self, locator):
        """Berilgan lokator bo'yicha element mavjudligini tekshiradi."""

        try:
            self.find_element(locator)
            return True
        except NoSuchElementException:
            return False

    def wait_for_element_clickable(self, locator):
        """Berilgan lokator bo'yicha element bosiladigan holatga kelishini kutadi."""
        time.sleep(1)
        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            print(f"Element bosilmaydigan holatda qoldi: {locator}")
            return None

    def wait_for_element_visible(self, locator):
        """Berilgan lokator bo'yicha element ko'rinishini kutadi."""

        try:
            return WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            print(f"Element ko'rinmadi: {locator}")
            return None

    def get_text(self, locator):
        """Berilgan lokator bo'yicha element matnini oladi."""

        return self.find_element(locator).text

    def get_attribute(self, locator, attribute):
        """
        Berilgan lokator bo'yicha element atributini oladi.

        :param locator: Element lokatori (tuple ko'rinishida: (By.XPATH, "xpath"))
        :param attribute: Olinishi kerak bo'lgan atribut nomi
        :return: Atribut qiymati
        """
        return self.find_element(locator).get_attribute(attribute)

    # Katta funksiyalar
    def input_text(self, locator, text):
        self.wait_for_element_clickable(locator)
        self.find_element(locator)
        self.clear_and_send_keys(locator, text)
        self.click(locator)

    def input_text_elem(self, locator, elem_locator):
        self.wait_for_element_clickable(locator)
        self.click(locator)
        time.sleep(2)
        self.wait_for_element_clickable(elem_locator)
        self.click(elem_locator)
        time.sleep(1)

    def wait_and_click(self, locator):
        self.wait_for_element_clickable(locator)
        self.find_element(locator)
        time.sleep(1)
        self.click(locator)

    def take_screenshot(self, name):
        # create screenshot fayle (agar mavjud bo'lmasa)
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        self.driver.save_screenshot(f"screenshots/{name}.png")


