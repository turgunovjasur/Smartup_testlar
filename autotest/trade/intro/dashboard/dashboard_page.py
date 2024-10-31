from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class DashboardPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    dashboard_header = By.XPATH, "//div/h3[contains(text(), 'Trade')]"

    def element_visible(self, timeout=5):
        self.wait_for_element_visible(self.dashboard_header, timeout=timeout)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    error_massage = (By.XPATH, "//span[@id='error']")

    def wait_for_element_error(self, timeout=2):
        self.wait_for_element_visible(self.error_massage, timeout=timeout)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # hover_show_button = By.XPATH, "//div[@class='pt-3 px-2']"
    # filial_button = By.XPATH, "//div[@class= 'menus']/child::li[2]/child::a[2]"
    #
    # def click_hover_show_button(self):
    #     self.click(self.hover_show_button)
    #     self.click(self.filial_button)
    # ------------------------------------------------------------------------------------------------------------------
    hover_show_button = By.XPATH, "//div[@class='pt-3 px-2']"
    filial_lists = By.XPATH, '//li[@class="filial-list rounded-0"]/a'
    filial_button = By.XPATH, "//div[@class= 'menus']/child::li[2]/child::a[2]"

    def click_hover_show_button(self, filial_name=None):
        self.click(self.hover_show_button)
        if filial_name is None:
            self.click(self.filial_button)

        if filial_name:
            filial_lists = self.driver.find_elements(*self.filial_lists)
            found = False
            filial_name_str = str(filial_name).strip()

            for filial in filial_lists:
                filial_name = filial.text.strip()
                print(f"Filial text: {filial_name}")

                if filial_name == filial_name_str:
                    filial.click()
                    print(f"Clicked filial: {filial_name}")
                    found = True
                    break

            if not found:
                print("Filial not found!")
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    active_session_header = By.XPATH, "//h3/t[contains(text(),'Активные сеансы')]"

    def element_visible_session(self, timeout=5):
        self.wait_for_element_visible(self.active_session_header, timeout=timeout)
    # ------------------------------------------------------------------------------------------------------------------
    delete_session_button = (By.XPATH, "(//button[@class='btn btn-icon btn-danger'])[1]")

    def click_button_delete_session(self, timeout=1):
        self.click(self.delete_session_button, timeout=timeout)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    sales_button = (By.XPATH, "//li/a/span[contains(text(), 'Продажа')]")

    def click_sales_button(self):
        self.click(self.sales_button)
    # ------------------------------------------------------------------------------------------------------------------
    warehouse_button = (By.XPATH, "//ul/li[3]/a[@class='menu-link menu-toggle']")

    def click_warehouse_button(self):
        self.click(self.warehouse_button)
    # ------------------------------------------------------------------------------------------------------------------
    reference_button = By.XPATH, "//li/a/span[contains(text(), 'Справочники')]"

    def click_reference_button(self):
        self.click(self.reference_button)
    # ------------------------------------------------------------------------------------------------------------------
