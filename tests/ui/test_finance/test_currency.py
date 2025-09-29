import pytest

from pages.anor.mk.currency_list.currency_list import CurrencyList
from pages.anor.mk.currency_view.currency_view import CurrencyView
from flows.auth_flow import login_user


@pytest.mark.regression
@pytest.mark.order(170)
def test_currency_add(driver, test_data):
    """Test adding a currency exchange rate"""
    # Test data
    currency_name = "Доллар США"
    exchange_rate = 10_000

    # Login
    login_user(driver, test_data, url='anor/mk/currency_list')

    # Open Currency List
    currency_list = CurrencyList(driver)
    currency_list.element_visible()
    currency_list.find_row(currency_name)
    currency_list.click_view_button()

    # Open Currency View
    currency_view = CurrencyView(driver)
    currency_view.element_visible()
    currency_view.click_navbar_button(navbar_button=2)
    currency_view.click_add_rate_button()

    # Add Exchange Rate
    currency_view.input_exchange_rate_button(exchange_rate)
    currency_view.click_save_button()

    # Verify Exchange Rate
    currency_view.check_row()
    currency_view.click_close_button()