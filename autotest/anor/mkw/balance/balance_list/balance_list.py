from selenium.common import StaleElementReferenceException
from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class BalanceList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    balance_header = (By.XPATH, '//button[@ng-if="fi.detail"]')

    def element_visible(self):
        return self.wait_for_element_visible(self.balance_header)
    # ------------------------------------------------------------------------------------------------------------------

    def find_row(self, product_name):
        self.find_row_and_click(product_name)
    # ------------------------------------------------------------------------------------------------------------------
    detail_button = (By.XPATH, '//button[@ng-click="detailOne(row)"]')

    def click_detail_button(self):
        self.click(self.detail_button)
    # ------------------------------------------------------------------------------------------------------------------
    reload_button = (By.XPATH, '//button[@ng-click="reload()"]')

    def click_reload_button(self):
        self.click(self.reload_button)
    # ------------------------------------------------------------------------------------------------------------------
    get_balance_quantity = (By.XPATH, '//div[contains(@class, "tbl-row")]/div[@class="tbl-cell"][10]')

    def check_balance_quantity(self):
        return self.get_numeric_value(self.get_balance_quantity)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    count_number = (By.XPATH, "//div[@class='tbl-body']/div[@class='tbl-row'][3]/div[9]")

    def check_balance(self):
        return self.get_numeric_value(self.count_number)
    # ------------------------------------------------------------------------------------------------------------------
    list_balance = (By.XPATH, "//div[@class='tbl-body']//div[@class='tbl-row']//div[@class='tbl-cell'][3]")
    name_elem = "test_life_cycle"

    def check_list_balance(self, elem_name):
        elem_name_str = str(elem_name).strip()

        for _ in range(3):  # 3 marta takrorlash
            try:
                elements = self.driver.find_elements(*self.list_balance)
                found = False

                for elem in elements:
                    element_text = elem.text.strip()

                    if element_text == elem_name_str:
                        # Row elementini topamiz
                        row = elem.find_element(By.XPATH, './ancestor::div[@class="tbl-row"]')
                        all_cells = row.find_elements(By.XPATH, './/div[@class="tbl-cell"]')

                        # Barcha cell'larning textlarini qaytarish
                        cell_texts = [cell.text.strip() for cell in all_cells]

                        found = True
                        return cell_texts  # Natijani qaytarish

                if found:
                    break  # Agar topilsa, siklni to'xtatish

            except StaleElementReferenceException:
                print("Stale element topildi, qayta qidirish.")
                continue  # Qayta urinib ko'rish
            except Exception as e:
                print(f"Failed to process element due to error: {e}")

        print(f"Element '{elem_name}' topilmadi! Balans ro'yxatida.")
        return None  # Yoki bo'sh list qaytarish
    # ------------------------------------------------------------------------------------------------------------------
