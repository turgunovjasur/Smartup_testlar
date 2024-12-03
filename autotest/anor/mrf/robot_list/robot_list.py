from time import time

from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class RobotList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="q.add_btn_dropdown.firstFn()"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, '//button[@ng-click="q.add_btn_dropdown.firstFn()"]')

    def click_add_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, element_name, checkbox=None):
        find_elems_name_xpath = (
            "//div[contains(@class, 'tbl')]//div[contains(@class, 'tbl-row')]"
            f"//div[contains(@class, 'tbl-cell') and normalize-space(text())='{element_name}']")

        start_time = time()
        timeout_duration = 20

        while time() - start_time < timeout_duration:
            try:
                # Sahifaning yuklanishini kutish
                self.wait.until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete")

                # Elementlarni kutish
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, find_elems_name_xpath)))

                elements = self.driver.find_elements(By.XPATH, find_elems_name_xpath)

                if elements:
                    target_element = elements[0]

                    # Elementgacha scroll
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", target_element)

                    # Element ko'rinishini kutish
                    WebDriverWait(self.driver, 5).until(
                        EC.visibility_of(target_element))

                    # Elementni bosish
                    target_element.click()
                    # print(f"'{element_name}' elementi topildi va bosildi.")

                    # Checkbox logikasi
                    if checkbox:
                        try:
                            parent_row = target_element.find_element(
                                By.XPATH, "./ancestor::div[contains(@class, 'tbl-row')]")
                            checkbox_elem = WebDriverWait(parent_row, 5).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, ".tbl-cell span")))
                            checkbox_elem.click()
                            print(f"'{element_name}' uchun checkbox bosildi.")
                        except Exception as e:
                            print(f"Checkbox bosishda xatolik: {str(e)}")

                    return True

                print(f"'{element_name}' elementi topilmadi, qayta urinish...")

            except StaleElementReferenceException:
                print("Element eskirdi, yangilanmoqda...")
            except Exception as e:
                print(f"Xatolik yuz berdi: {str(e)}")

        print(f"'{element_name}' elementi {timeout_duration} sekund ichida topilmadi.")
        self.take_screenshot(f"find_filial_row_{element_name}_error")
        return False
    # ------------------------------------------------------------------------------------------------------------------
    view_button = By.XPATH, '//button[@ng-click="view(row)"]'

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
