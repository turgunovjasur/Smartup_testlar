import random
import pytest
from autotest.anor.mkf.contract_add.contract_add import ContractAdd
from autotest.anor.mkf.contract_list.contract_list import ContractList
from autotest.anor.mkf.contract_view.contract_view import ContractView
from autotest.core.md.base_page import BasePage
from tests.test_base.test_base import login_user
from utils.driver_setup import driver
from tests.conftest import test_data


def contract_add(driver, test_data, client_name=None, contract_name=None, initial_amount=None,
                 currency_cod=None, currency_name=None, sub_filial_name=None, sub_filial=False):
    """Test adding a contract."""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: contract_add")

    # Test data
    data = test_data["data"]
    client_name = client_name or data["client_name"]
    contract_name = contract_name or data["contract_name"]
    initial_amount = initial_amount or data["product_quantity"] * data["product_price"]
    base_currency_cod = currency_cod or data["base_currency_cod"]
    currency_name = currency_name or "Узбекский сум"
    sub_filial_name = sub_filial_name or data["sub_filial_name"]

    base_page.logger.info(f"Test data: client_name='{client_name}', contract_name='{contract_name}', "
                          f"initial_amount='{initial_amount}', base_currency_cod='{base_currency_cod}',"
                          f" sub_filial_name='{sub_filial_name}'")

    try:
        # Login
        login_user(driver, test_data, url='anor/mkf/contract_list')

        # Open Contract List
        contract_list = ContractList(driver)
        assert contract_list.element_visible(), "ContractList not open!"
        contract_list.click_add_button()

        # Open Contract Add
        contract_add = ContractAdd(driver)
        assert contract_add.element_visible(), "ContractAdd not open!"
        contract_number = random.randint(1, 999999)
        contract_add.input_contract_number(contract_number)
        contract_add.input_contract_name(contract_name)
        contract_add.click_radio_button()
        contract_add.input_person_name(client_name)
        contract_add.input_currency_name(base_currency_cod)
        contract_add.input_initial_amount(initial_amount)
        if sub_filial:
            contract_add.input_sub_filial(sub_filial_name)
        contract_add.click_is_main_checkbox()
        contract_add.click_save_button()

        # Verify in Contract List
        assert contract_list.element_visible(), "ContractList not open after save!"
        contract_list.find_row(contract_name)
        contract_list.click_view_button()

        # Verify in Contract View
        contract_view = ContractView(driver)
        assert contract_view.element_visible(), "ContractView not open!"
        get_contract_name = contract_view.check_contract_name()
        assert get_contract_name == contract_name, f"Error: {get_contract_name} != {contract_name}"
        get_currency_name = contract_view.check_currency_name()
        assert get_currency_name == currency_name, f"Error: {get_currency_name} != {currency_name}"
        contract_view.click_close_button()

        base_page.logger.info(f"✅ Contract '{contract_name}' successfully added. Contract Number: {contract_number}")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        base_page.logger.error(f"❌ Unexpected error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_add_contract_for_client_A_UZB(driver, test_data):
    """Test adding a contract for Client A in UZB currency."""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_contract_for_client_A_UZB")

    data = test_data["data"]
    client_name = f"{data['client_name']}-A"
    contract_name = f"{data['contract_name']}-A-UZB"
    contract_add(driver, test_data,
                 client_name=client_name,
                 contract_name=contract_name)


def test_add_contract_for_client_B_UZB(driver, test_data):
    """Test adding a contract for Client B in UZB currency with a higher initial amount."""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_contract_for_client_B_UZB")

    data = test_data["data"]
    client_name = f"{data['client_name']}-B"
    contract_name = f"{data['contract_name']}-B-UZB"
    initial_amount = 100 * data["product_price"]
    contract_add(driver, test_data,
                 client_name=client_name,
                 contract_name=contract_name,
                 initial_amount=initial_amount)


def test_add_contract_for_client_C_USA(driver, test_data):
    """Test adding a contract for Client C in USA currency."""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_contract_for_client_C_USA")

    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    contract_name = f"{data['contract_name']}-C-USA"
    currency_cod = 840
    currency_name = 'Доллар США'
    initial_amount = 100 * data["product_price_USA"]
    contract_add(driver, test_data,
                 client_name=client_name,
                 contract_name=contract_name,
                 currency_cod=currency_cod,
                 currency_name=currency_name,
                 initial_amount=initial_amount,
                 sub_filial=True)