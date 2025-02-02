from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from autotest.core.md.base_page import BasePage


class DashboardPage(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    dashboard_header = (By.XPATH, "//div/h3[contains(text(), 'Trade')]")
    save_button_header = (By.XPATH, '//button[@ng-click="save()"]')

    def element_visible(self, timeout=None):
        try:
            if not self._wait_for_all_loaders():
                raise TimeoutException(f"Dashboard sahifasi yuklanishida xatolik")
            try:
                if self._wait_for_visibility(self.dashboard_header, timeout=timeout, error_massage=False):
                    self.logger.info("Dashboard sahifasida 'Trade' elementi tasdiqlandi")
                    return True
            except:
                if self._wait_for_visibility(self.dashboard_header, timeout=timeout, error_massage=False):
                    self.logger.info("ChangePassword sahifasida 'save_button' elementi tasdiqlandi")
                    return True

        except Exception:
            self.logger.error("❌ Dashboard tekshiruvi muvaffaqiyatsiz: 'header_text' elementi topilmadi")
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
            if self._wait_for_visibility(self.active_session_header, timeout=5):
                self.logger.info("‼️ Aktiv sessiya mavjud - uni o'chirish kerak.")
                return True

        except Exception:
            self.logger.info("5 sekund kutildi. Aktiv sessiya tekshiruvi yakunlandi. Sessiya mavjud emas.")
            return False

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
