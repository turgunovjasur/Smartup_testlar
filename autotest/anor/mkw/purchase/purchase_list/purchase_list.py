from time import time
from selenium.common import StaleElementReferenceException
from autotest.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class PurchaseList(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    purchase_list_header = (By.XPATH, "//div/ul/li/a[contains(text(), 'Поступления ТМЦ на склад')]")

    def element_visible(self):
        self.wait_for_element_visible(self.purchase_list_header)
    # ------------------------------------------------------------------------------------------------------------------
    add_button = (By.XPATH, "//button[@id='anor288-button-add']")

    def click_button(self):
        self.click(self.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    # purchase_id
    # ------------------------------------------------------------------------------------------------------------------
    barcode_button = (By.XPATH, "//div[contains(text(), 'Штрих-код')]")

    def click_2x(self):
        self.click_multiple_time(self.barcode_button, click_count=2, delay=1)
    # ------------------------------------------------------------------------------------------------------------------
    first_list_purchase = (By.XPATH, "//b-grid[@id='anor288-bgrid-table']//div[@class='tbl-row']/div[2]")

    def click_row_list(self):
        self.click(self.first_list_purchase)
    # ------------------------------------------------------------------------------------------------------------------
    view_button = (By.XPATH, "//button[@id='anor288-button-view']")

    def click_view_button(self):
        self.click(self.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    status_one_button = (By.XPATH, "//button[@id='anor288-button-changestatus']")
    status_draft_button = (By.XPATH, "//div[@id='statusDropDown']//div[@class='card-body p-0']/a[1]")
    status_yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_status_one_button(self):
        self.click(self.status_one_button)
        self.click(self.status_draft_button)
        self.click(self.status_yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    delete_one_button = (By.XPATH, "//button[@id='anor288-button-delete']")
    delete_yes_button = (By.XPATH, "//button[@ng-click='a.bConfirm.clickYes()']")

    def click_delete_one_button(self):
        self.click(self.delete_one_button)
        self.click(self.delete_yes_button)
    # ------------------------------------------------------------------------------------------------------------------

    def find_and_click_checkbox(self, element_name, checkbox=False):
        find_elems_name_xpath = "//div[@class='tbl-body']//div[@class='tbl-row']//div[@class='tbl-cell'][3]"

        start_time = time()
        timeout_duration = 10

        while time() - start_time < timeout_duration:
            try:
                elements = self.driver.find_elements(By.XPATH, find_elems_name_xpath)
                print("Element list:")

                found = False
                for elem in elements:
                    print(f"Element text: {elem.text.strip()}")

                    if elem.text.strip() == element_name:
                        found = True
                        self.click(elem)
                        self.click(elem)
                        print(f"'{element_name}' item found and pressed.")

                        # Checkbox
                        if checkbox:
                            parent_row = elem.find_element(By.XPATH, "./ancestor::div[contains(@class, 'tbl-row')]")
                            try:
                                checkbox_span = parent_row.find_element(By.CSS_SELECTOR, ".tbl-cell span")
                                self.driver.execute_script("arguments[0].click();", checkbox_span)
                                print(f"'{element_name}' checkbox pressed.")
                            except StaleElementReferenceException:
                                print(f"'{element_name}' for checkbox stale element reference.")
                        return

                if not found:
                    print(f"'{element_name}' item not found, wanted again...")

            except StaleElementReferenceException:
                print("StaleElementReferenceException, elements updated...")

        print(f"'{element_name}' item not found, search deadline.")
    # ------------------------------------------------------------------------------------------------------------------
