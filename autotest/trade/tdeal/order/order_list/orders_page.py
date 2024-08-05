from autotest.core.md.base_page import BasePage

from selenium.webdriver.common.by import By


class OrdersPage(BasePage):
    ##############################################################################
    order_page_header_xpath = "//ul/li/a[contains(text(), 'Опросники')]"

    def element_visible(self, order_page_header_xpath):
        self.wait_for_element_visible((By.XPATH, order_page_header_xpath))

    ##############################################################################
    count_xpath = "//div[contains(@class, 'sg-cell') and contains(@class, 'col-sm-4') and contains(@class, " \
                  "'ng-binding')]"

    def check_count(self, count_xpath):
        try:
            element = self.wait_for_element_visible((By.XPATH, count_xpath), timeout=20)
            if element:
                count_text = element.text.strip()
                if count_text:
                    count = ''.join(filter(str.isdigit, count_text))
                    return int(count) if count else 0
                else:
                    print("Warn: the count element is empty")
                    return 0
            else:
                print("Warn: count element not found")
                return 0
        except Exception as e:
            print(f"Check_count_error: {str(e)}")
            self.take_screenshot("check_count_error")
            return 0

    ##############################################################################
    create_button_xpath = "//div/button[contains(text(), 'Создать')]"

    def click_button(self, create_button_xpath):
        self.wait_and_click((By.XPATH, create_button_xpath))
    ##############################################################################
