from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class DashboardPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    dashboard_header = By.XPATH, "//div/h3[contains(text(), 'Trade')]"

    def element_visible(self, timeout=20):
        self.wait_for_element_visible(self.dashboard_header, timeout=timeout)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    error_massage = (By.XPATH, "//span[@id='error']")

    def wait_for_element(self, timeout=2):
        self.wait_for_element_visible(self.error_massage, timeout=timeout)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    hover_show_button = By.XPATH, "//div[@class='pt-3 px-2']"
    filial_button = By.XPATH, "//div[@class= 'menus']/child::li[2]/child::a[2]"

    def click_hover_show_button(self):
        self.click(self.hover_show_button)
        self.click(self.filial_button)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    active_session_header = By.XPATH, "//h3/t[contains(text(),'Активные сеансы')]"

    def element_visible_session(self, timeout=1):
        self.wait_for_element_visible(self.active_session_header, timeout=timeout)
    # ------------------------------------------------------------------------------------------------------------------
    delete_session_button = By.XPATH, "(//button[@class='btn btn-icon btn-danger'])[1]"

    def click_button_delete_session(self, timeout=2):
        self.click(self.delete_session_button, timeout=timeout)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    sales_button = By.XPATH, "//li/a/span[contains(text(), 'Продажа')]"

    def click_sales_button(self):
        self.click(self.sales_button)
    # ------------------------------------------------------------------------------------------------------------------
    warehouse_button = By.XPATH, "//ul/li[3]/a[@class='menu-link menu-toggle']"

    def click_warehouse_button(self):
        self.click(self.warehouse_button)
    # ------------------------------------------------------------------------------------------------------------------
    reference_button = By.XPATH, "//li/a/span[contains(text(), 'Справочники')]"

    def click_reference_button(self):
        self.click(self.reference_button)
    # ------------------------------------------------------------------------------------------------------------------
