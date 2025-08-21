from utils.logger import get_test_name, configure_logging


class Assertions:
    """Assertion metodlari (Page Object API orqali)"""

    # ==================================================================================================================

    def __init__(self, page, timeout=10):
        """
        page: BasePage yoki shunga o‘xshash obyekt bo‘lishi shart:
              - wait_for_element_visible(locator, timeout?) -> WebElement
              - wait_for_element_invisible(locator, timeout?) -> bool (ixtiyoriy, bo'lmasa BasePage'da bor metoddan foydalanasiz)
              - get_text(locator, ...) -> str (ixtiyoriy)
              - logger, driver property’lari
        """
        self.page = page
        self.driver = page.driver
        self.logger = getattr(page, "logger", configure_logging(get_test_name()))
        self.timeout = timeout

    # ==================================================================================================================

    @staticmethod
    def assert_equals(actual, expected, message=""):
        """Qiymatlar tengligini tekshirish"""

        error_msg = f"{message}: Expected '{expected}', but got '{actual}'" if message else f"Expected '{expected}', but got '{actual}'"
        assert actual == expected, error_msg

    # ==================================================================================================================

    @staticmethod
    def assert_not_equals(actual, expected, message=""):
        """Qiymatlar teng emasligini tekshirish"""

        error_msg = f"{message}: Values should not be equal, but both are '{actual}'" if message else f"Values should not be equal, but both are '{actual}'"
        assert actual != expected, error_msg

    # ==================================================================================================================

    @staticmethod
    def assert_contains(container, item, message=""):
        """Element ichida boshqa element borligini tekshirish"""

        error_msg = f"{message}: '{item}' not found in '{container}'" if message else f"'{item}' not found in '{container}'"
        assert item in container, error_msg

    # ==================================================================================================================

    @staticmethod
    def assert_not_contains(container, item, message=""):
        """Element ichida boshqa element yo'qligini tekshirish"""

        error_msg = f"{message}: '{item}' found in '{container}' but should not be" if message else f"'{item}' found in '{container}' but should not be"
        assert item not in container, error_msg

    # ==================================================================================================================

    @staticmethod
    def assert_true(condition, message=""):
        """Shart to'g'riligini tekshirish"""

        error_msg = f"{message}: Condition is False" if message else "Condition is False"
        assert condition, error_msg

    # ==================================================================================================================

    @staticmethod
    def assert_false(condition, message=""):
        """Shart noto'g'riligini tekshirish"""

        error_msg = f"{message}: Condition is True but should be False" if message else "Condition is True but should be False"
        assert not condition, error_msg

    # ==================================================================================================================

    @staticmethod
    def assert_greater_than(actual, expected, message=""):
        """Qiymat kattaligini tekshirish"""

        error_msg = f"{message}: {actual} is not greater than {expected}" if message else f"{actual} is not greater than {expected}"
        assert actual > expected, error_msg

    # ==================================================================================================================

    @staticmethod
    def assert_less_than(actual, expected, message=""):
        """Qiymat kichikligini tekshirish"""

        error_msg = f"{message}: {actual} is not less than {expected}" if message else f"{actual} is not less than {expected}"
        assert actual < expected, error_msg

    # ==================================================================================================================

    @staticmethod
    def assert_greater_equal(actual, expected, message=""):
        """Qiymat katta yoki tengligini tekshirish"""

        error_msg = f"{message}: {actual} is not greater than or equal to {expected}" if message else f"{actual} is not greater than or equal to {expected}"
        assert actual >= expected, error_msg

    # ==================================================================================================================

    @staticmethod
    def assert_less_equal(actual, expected, message=""):
        """Qiymat kichik yoki tengligini tekshirish"""

        error_msg = f"{message}: {actual} is not less than or equal to {expected}" if message else f"{actual} is not less than or equal to {expected}"
        assert actual <= expected, error_msg

    # ==================================================================================================================

    @staticmethod
    def assert_is_none(value, message=""):
        """Qiymat None ekanligini tekshirish"""

        error_msg = f"{message}: Value is not None, got '{value}'" if message else f"Value is not None, got '{value}'"
        assert value is None, error_msg

    # ==================================================================================================================

    @staticmethod
    def assert_is_not_none(value, message=""):
        """Qiymat None emasligini tekshirish"""

        error_msg = f"{message}: Value is None" if message else "Value is None"
        assert value is not None, error_msg

    # ==================================================================================================================

    @staticmethod
    def assert_empty(container, message=""):
        """Konteyner bo'shligini tekshirish"""

        error_msg = f"{message}: Container is not empty, got '{container}'" if message else f"Container is not empty, got '{container}'"
        assert len(container) == 0, error_msg

    # ==================================================================================================================

    @staticmethod
    def assert_not_empty(container, message=""):
        """Konteyner bo'sh emasligini tekshirish"""

        error_msg = f"{message}: Container is empty" if message else "Container is empty"
        assert len(container) > 0, error_msg

    # ==================================================================================================================

    def assert_element_visible(self, locator, message=""):
        """Element ko'rinishini tekshirish"""

        try:
            self.page._wait_for_all_loaders()
            element = self.page.wait_for_element(locator, wait_type="visibility")
            is_visible = element.is_displayed()
            error_msg = f"{message}: Element is not visible" if message else "Element is not visible"
            assert is_visible, error_msg
        except Exception as e:
            error_msg = f"{message}: Element not found or not visible - {str(e)}" if message else f"Element not found or not visible - {str(e)}"
            assert False, error_msg

    # ==================================================================================================================

    def assert_element_not_visible(self, locator, message=""):
        """Element ko'rinmasligini tekshirish"""

        try:
            element = self.page.wait_for_element(locator, wait_type="visibility")
            is_visible = element.is_displayed()
            error_msg = f"{message}: Element is visible but should not be" if message else "Element is visible but should not be"
            assert not is_visible, error_msg
        except Exception:
            # Element topilmagan bo'lsa, bu yaxshi
            pass

    # ==================================================================================================================

    def assert_element_text_equals(self, locator, expected_text, message=""):
        """Element matni tengligini tekshirish"""

        try:
            element = self.page.wait_for_element(locator, wait_type="visibility")
            actual_text = element.text.strip()
            error_msg = f"{message}: Expected text '{expected_text}', but got '{actual_text}'" if message else f"Expected text '{expected_text}', but got '{actual_text}'"
            assert actual_text == expected_text, error_msg
        except Exception as e:
            error_msg = f"{message}: Element not found or text not readable - {str(e)}" if message else f"Element not found or text not readable - {str(e)}"
            assert False, error_msg

    # ==================================================================================================================

    def assert_element_contains_text(self, locator, expected_text, message=""):
        """Element matni ichida boshqa matn borligini tekshirish"""

        try:
            element = self.page.wait_for_element(locator, wait_type="visibility")
            actual_text = element.text.strip()
            error_msg = f"{message}: Text '{expected_text}' not found in '{actual_text}'" if message else f"Text '{expected_text}' not found in '{actual_text}'"
            assert expected_text in actual_text, error_msg
        except Exception as e:
            error_msg = f"{message}: Element not found or text not readable - {str(e)}" if message else f"Element not found or text not readable - {str(e)}"
            assert False, error_msg

    # ==================================================================================================================

    def assert_url_contains(self, expected_url_part, message=""):
        """URL ichida ma'lum qism borligini tekshirish"""

        current_url = self.driver.current_url
        error_msg = f"{message}: URL '{current_url}' does not contain '{expected_url_part}'" if message else f"URL '{current_url}' does not contain '{expected_url_part}'"
        assert expected_url_part in current_url, error_msg

    # ==================================================================================================================

    def assert_url_equals(self, expected_url, message=""):
        """URL to'liq tengligini tekshirish"""

        current_url = self.driver.current_url
        error_msg = f"{message}: Expected URL '{expected_url}', but got '{current_url}'" if message else f"Expected URL '{expected_url}', but got '{current_url}'"
        assert current_url == expected_url, error_msg

    # ==================================================================================================================

class SoftAssertions:
    """Soft assertion uchun klass - barcha xatolarni to'plab, oxirida ko'rsatadi"""

    def __init__(self):
        self.errors = []

    # ==================================================================================================================

    def assert_equals(self, actual, expected, message=""):
        """Qiymatlar tengligini tekshirish (soft)"""
        try:
            Assertions.assert_equals(actual, expected, message)
        except AssertionError as e:
            self.errors.append(str(e))

    # ==================================================================================================================

    def assert_true(self, condition, message=""):
        """Shart to'g'riligini tekshirish (soft)"""
        try:
            Assertions.assert_true(condition, message)
        except AssertionError as e:
            self.errors.append(str(e))

    # ==================================================================================================================

    def assert_element_visible(self, driver, locator, message=""):
        """Element ko'rinishini tekshirish (soft)"""
        try:
            assertions = Assertions(driver)
            assertions.assert_element_visible(locator, message)
        except AssertionError as e:
            self.errors.append(str(e))

    # ==================================================================================================================

    def assert_all(self):
        """Barcha xatolarni ko'rsatish"""
        if self.errors:
            error_message = "\n".join(self.errors)
            raise AssertionError(f"Multiple assertion failures:\n{error_message}")

    # ==================================================================================================================

    def clear_errors(self):
        """Xatolarni tozalash"""
        self.errors.clear()

    # ==================================================================================================================
