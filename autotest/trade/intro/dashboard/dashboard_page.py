from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage
from utils.exception import ElementInteractionError, LoaderTimeoutError


class DashboardPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    dashboard_header = (By.XPATH, "//div/h3[contains(text(), 'Trade')]")
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def element_visible(self):
        try:
            self._wait_for_all_loaders(log_text='Dashboard or ChangePassword')

            if self._wait_for_visibility(self.dashboard_header, timeout=10, error_message=False):
                self.logger.info("Dashboard Page: Successfully opened")
                return True
        except LoaderTimeoutError:
            raise
        except ElementInteractionError:
            pass

        try:
            if self._wait_for_visibility(self.save_button, timeout=10, error_message=False):
                self.logger.info("Dashboard Page (ChangePassword): Successfully opened")
                return True
        except ElementInteractionError:
            pass

        self.logger.error("Dashboard Page: Verification failed - elements not found")
        return False
    # ------------------------------------------------------------------------------------------------------------------
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
        try:
            self._wait_for_all_loaders(log_text='Dashboard Page')

            if self._wait_for_visibility(self.active_session_header, timeout=5, error_message=False):
                self.logger.info("‼️Old sessiya available!")
                return True

        except LoaderTimeoutError:
            raise

        except ElementInteractionError:
            self.logger.info("Old sessiya not available! Waited for 5 seconds.")
            return False

    # ------------------------------------------------------------------------------------------------------------------
    delete_session_button = (By.XPATH, "(//button[@class='btn btn-icon btn-danger'])[1]")

    def click_button_delete_session(self):
        try:
            if self.click(self.delete_session_button):
                self.logger.info("Old session successfully deleted")

        except ElementInteractionError:
            self.logger.error("Unexpected error: -> while deleting the old session")
            raise
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
