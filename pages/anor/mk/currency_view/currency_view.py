from pages.core.md.base_page import BasePage
from selenium.webdriver.common.by import By


class CurrencyView(BasePage):
    # ------------------------------------------------------------------------------------------------------------------
    header = (By.XPATH, "//div[@class='card-title']/h5/t")

    def element_visible(self):
        return self.wait_for_element_visible(self.header)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def click_navbar_button(self, navbar_button):
        navbar = (By.XPATH, f"(//div[contains(@class,'navi navi-bolder')]//div[contains(@class,'navi-item')]/a)[{navbar_button}]")
        self.click(navbar)
    # ------------------------------------------------------------------------------------------------------------------
    add_rate_button = (By.XPATH, '//button[@ng-click="openAddRate()"]')

    def click_add_rate_button(self):
        self.click(self.add_rate_button)
    # ------------------------------------------------------------------------------------------------------------------
    exchange_rate_input = (By.XPATH, '//div[@class="modal-content"]//div[@class="form-group"]/input[@ng-model="p.data.rate"]')

    def input_exchange_rate_button(self, exchange_rate):
        self.input_text(self.exchange_rate_input, exchange_rate)
    # ------------------------------------------------------------------------------------------------------------------
    save_button = (By.XPATH, '//button[@ng-click="save()"]')

    def click_save_button(self):
        self.click(self.save_button)
    # ------------------------------------------------------------------------------------------------------------------
    get_row = (By.XPATH, '//div[@class="tbl"]//div[@class="tbl-row"]')

    def check_row(self):
        return self.wait_for_element_visible(self.get_row)
    # ------------------------------------------------------------------------------------------------------------------
    close_button = (By.XPATH, '//button[@ng-click="page.close()"]')

    def click_close_button(self):
        self.click(self.close_button)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    refresh_rate_button = (By.XPATH, '//button[@ng-click="refreshRate()"]')
    yes_button = (By.XPATH, '//button[@ng-click="a.bConfirm.clickYes()"]')

    def click_refresh_rate_button(self):
        self.click(self.refresh_rate_button)
        self.click(self.yes_button)
    # ------------------------------------------------------------------------------------------------------------------

    def get_currency_rate_with_xpath(self):
        """
        Jadvaldan 'Курс валют' ustunini XPATH yordamida aniqlab, qiymatini oladi.
        """

        # 1-QADAM: Headerlarni XPATH orqali olish
        # Ma'nosi: classida 'tbl-header-cell' so'zi qatnashgan barcha divlarni top
        xpath_headers = "//div[contains(@class, 'tbl-header')]//div[contains(@class, 'tbl-header-cell')]"
        headers = self._wait_for_presence_all((By.XPATH, xpath_headers))

        target_index = -1

        if headers:
            for index, header in enumerate(headers):
                # Header matnini tekshiramiz
                if "Курс валют" in header.text:
                    target_index = index
                    break

        if target_index == -1:
            self.logger.warning("'Курс валют' sarlavhasi topilmadi.")
            return None

        # 2-QADAM: 1-qatordagi kataklarni XPATH orqali olish
        # Ma'nosi: tbl-body ichidagi birinchi tbl-row ni top va uning ichidagi barcha div farzandlarini ol
        # Eslatma: XPath da indekslash [1] dan boshlanadi
        xpath_first_row_cells = "//div[contains(@class, 'tbl-body')]//div[contains(@class, 'tbl-row')][1]/div"
        cells = self._wait_for_presence_all((By.XPATH, xpath_first_row_cells))

        # 3-QADAM: Indeks bo'yicha qiymatni olish
        if cells and len(cells) > target_index:
            target_cell = cells[target_index]

            # Scroll qilamiz (BasePage funksiyasi)
            self._scroll_to_element(target_cell, (By.XPATH, xpath_first_row_cells))

            result_value = target_cell.text
            self.logger.info(f"Natija (XPath orqali): {result_value}")
            return result_value

        self.logger.error("Jadval kataklari topilmadi.")
        return None
    # ------------------------------------------------------------------------------------------------------------------
