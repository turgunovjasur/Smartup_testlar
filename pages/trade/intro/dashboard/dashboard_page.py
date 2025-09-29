from selenium.webdriver.common.by import By
from pages.core.md.base_page import BasePage
from utils.exception import ElementVisibilityError


class DashboardPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    dashboard_header = (By.XPATH, "//div/h3[contains(text(), 'Trade')]")

    def element_visible_dashboard(self):
        self.wait_for_element_visible(self.dashboard_header)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def element_visible_change_password(self):
        self.wait_for_element_visible(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
    filial_list_button = (By.XPATH, '//div[contains(@class, "hover")]//div[@class="pt-3 px-2"]')

    def find_filial(self, filial_name):
        self.click(self.filial_list_button)
        self.find_row_and_click(element_name=filial_name,
                                xpath_pattern=f"//div[contains(@class, 'menus')]/li[contains(@class, 'filial-list')]/a[contains(text(), '{filial_name}')]")
    # ------------------------------------------------------------------------------------------------------------------
    # visible_session
    # ------------------------------------------------------------------------------------------------------------------
    active_session_header = (By.XPATH, "//h3/t[contains(text(),'Активные сеансы')]")

    def element_visible_session(self):
        self._wait_for_all_loaders()
        try:
            self.wait_for_element(self.active_session_header, timeout=0.5, wait_type="visibility", error_message=False)
            self.logger.info("Old sessiya available!")
            return True

        except ElementVisibilityError:
            self.logger.info(f"Old sessiya not available! Waited for 0.5 seconds.")
    # ------------------------------------------------------------------------------------------------------------------
    delete_session_button = (By.XPATH, "(//button[@class='btn btn-icon btn-danger'])[1]")

    def click_button_delete_session(self):
        self.click(self.delete_session_button)
        self.logger.info("Old session successfully deleted")
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
