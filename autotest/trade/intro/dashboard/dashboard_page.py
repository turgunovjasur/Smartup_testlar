from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DashboardPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    dashboard_header = (By.XPATH, "//div/h3[contains(text(), 'Trade')]")

    def element_visible(self, timeout=None):
        return self.wait_for_element_visible(self.dashboard_header, timeout=timeout)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    error_massage = (By.XPATH, "//span[@id='error']")

    def wait_for_element_error(self, timeout=2):
        self.wait_for_element_visible(self.error_massage, timeout=timeout)
    # ------------------------------------------------------------------------------------------------------------------
    filial_list_button = (By.XPATH, '//div[contains(@class, "hover")]//div[@class="pt-3 px-2"]')

    def find_filial(self, filial_name):
        self.click(self.filial_list_button)
        self.find_row_and_click(element_name="filial_name",
                                xpath_pattern=f"//div[contains(@class, 'menus')]/li[contains(@class, 'filial-list')]/a[contains(text(), '{filial_name}')]")
    # ------------------------------------------------------------------------------------------------------------------
    # visible_session
    # ------------------------------------------------------------------------------------------------------------------
    active_session_header = (By.XPATH, "//h3/t[contains(text(),'Активные сеансы')]")

    def element_visible_session(self):
        """Agar active_session_header ko'rinsa, delete_session_button ni bosish."""

        try:
            element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.delete_session_button))
            element.click()
            self.logger.info("Aktiv sessiya topildi va o'chirildi.")
        except TimeoutException:
            self.logger.info("Aktiv sessiya yo'q.")
    # ------------------------------------------------------------------------------------------------------------------
    delete_session_button = (By.XPATH, "(//button[@class='btn btn-icon btn-danger'])[1]")

    def click_button_delete_session(self):
        self.click(self.delete_session_button)
    # ------------------------------------------------------------------------------------------------------------------
    # navbar buttons
    # ------------------------------------------------------------------------------------------------------------------
    main_button = (By.XPATH, "//li/a/span[contains(text(), 'Главное')]")

    def click_main_button(self):
        self.click(self.main_button)
    # ------------------------------------------------------------------------------------------------------------------
    sales_button = (By.XPATH, "//li/a/span[contains(text(), 'Продажа')]")

    def click_sales_button(self):
        self.click(self.sales_button)
    # ------------------------------------------------------------------------------------------------------------------
    warehouse_button = (By.XPATH, "//ul/li[3]/a[@class='menu-link menu-toggle']")

    def click_warehouse_button(self):
        self.click(self.warehouse_button)
    # ------------------------------------------------------------------------------------------------------------------
    reference_button = (By.XPATH, "//li/a/span[contains(text(), 'Справочники')]")

    def click_reference_button(self):
        self.click(self.reference_button)
    # ------------------------------------------------------------------------------------------------------------------
