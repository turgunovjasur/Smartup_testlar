from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class StocktakingView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, '//button[@ng-click="page.close()"]')

    def element_visible(self):
        self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------

    def get_input_value(self, input_name, clean=None):
        locator = (By.XPATH, f'//label[contains(.,"{input_name}")]/../span')
        return self.get_text(locator, clean=clean)
    # ------------------------------------------------------------------------------------------------------------------

    def click_navbar_button(self, navbar_name):
        locator = (By.XPATH, f'//div[contains(@class,"navi-item")]//t[contains(.,"{navbar_name}")]')
        self.click(locator)
    # ------------------------------------------------------------------------------------------------------------------
    search_input = (By.XPATH, '//b-pg-controller[@name="items0"]//input')

    def input_search(self, search_name):
        self.input_text(self.search_input, search_name)
    # ------------------------------------------------------------------------------------------------------------------

    def check_product(self, product_name):
        locator = (By.XPATH, f'//b-pg-grid[@name="items0"]//div[contains(text(),"{product_name}")]')
        self.wait_for_element(locator, wait_type="visibility")
    # ------------------------------------------------------------------------------------------------------------------

    def check_corr(self, templates_name="Прочие операционные доходы"):
        locator = (By.XPATH, f'//b-pg-grid[@name="corrs"]//div[contains(@class,"tbl-cell ng")]')
        options = self._wait_for_presence_all(locator)

        for option in options:
            if option.text.strip() == templates_name:
                self.logger.info(f"Corr topildi: '{templates_name}'")
                return True

        self.logger.warning(f"Corr topilmadi: '{templates_name}'")
        return False
    # ------------------------------------------------------------------------------------------------------------------
    