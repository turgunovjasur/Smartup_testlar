import pytest
from autotest.anor.mk.currency_list.currency_list import CurrencyList
from autotest.anor.mk.currency_view.currency_view import CurrencyView
from autotest.core.md.base_page import BasePage
from tests.test_base.test_base import login_user
from utils.driver_setup import driver
from tests.conftest import test_data


def test_currency_add(driver, test_data):
    """Test adding a currency exchange rate"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_currency_add")

    # Test data
    currency_name = "Доллар США"
    exchange_rate = 10_000

    try:
        # Login
        login_user(driver, test_data, url='anor/mk/currency_list')

        # Open Currency List
        currency_list = CurrencyList(driver)
        assert currency_list.element_visible(), "CurrencyList not open!"
        currency_list.find_row(currency_name)
        currency_list.click_view_button()

        # Open Currency View
        currency_view = CurrencyView(driver)
        assert currency_view.element_visible(), "CurrencyView not open!"
        currency_view.click_navbar_button(navbar_button=2)
        currency_view.click_add_rate_button()

        # Add Exchange Rate
        currency_view.input_exchange_rate_button(exchange_rate)
        currency_view.click_save_button()

        # Verify Exchange Rate
        assert currency_view.check_row(), "Exchange rate not found!"
        currency_view.click_close_button()

        base_page.logger.info(f"✅ Exchange rate for '{currency_name}' set to {exchange_rate} successfully!")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))