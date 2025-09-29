import random
import pytest
from flows.auth_flow import login_user
from pages.core.md.base_page import BasePage
from pages.anor.mkf.contract_add.contract_add import ContractAdd
from pages.anor.mkf.contract_list.contract_list import ContractList
from pages.anor.mkf.contract_view.contract_view import ContractView


def contract_add(driver, test_data, **kwargs):
    """Test adding a contract."""
    # Test data
    is_main = kwargs.get("is_main", True)
    client_name = kwargs.get("client_name")
    contract_name = kwargs.get("contract_name")
    initial_amount = kwargs.get("initial_amount")
    currency_name = kwargs.get("currency_name", "Узбекский сум")
    sub_filial_name = kwargs.get("sub_filial_name")

    # Login
    login_user(driver, test_data, url='anor/mkf/contract_list')

    # Open Contract List
    contract_list = ContractList(driver)
    contract_list.element_visible()
    contract_list.click_add_button()

    # Open Contract Add
    contract_add = ContractAdd(driver)
    contract_add.element_visible()
    contract_number = random.randint(1, 999999)
    contract_add.input_contract_number(contract_number)
    contract_add.input_contract_name(contract_name)
    contract_add.click_radio_button()
    contract_add.input_person_name(client_name)
    contract_add.input_currency_name(currency_name)
    contract_add.input_initial_amount(initial_amount)
    if sub_filial_name:
        contract_add.input_sub_filial(sub_filial_name)
    contract_add.click_is_main_checkbox(state=is_main)
    contract_add.click_save_button()

    # Verify in Contract List
    contract_list.element_visible()
    contract_list.find_row(contract_name)
    contract_list.click_view_button()

    # Verify in Contract View
    contract_view = ContractView(driver)
    contract_view.element_visible()
    get_contract_name = contract_view.check_contract_name()
    assert get_contract_name == contract_name, f"Error: {get_contract_name} != {contract_name}"
    get_currency_name = contract_view.check_currency_name()
    assert get_currency_name == currency_name, f"Error: {get_currency_name} != {currency_name}"
    contract_view.click_close_button()


@pytest.mark.regression
@pytest.mark.order_group_A
@pytest.mark.order(230)
def test_add_contract_for_client_A_UZB(driver, test_data):
    """Test adding a contract for Client A in UZB currency."""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_contract_for_client_A_UZB")

    data = test_data["data"]
    client_name = f"{data['client_name']}-A"
    contract_name = f"{data['contract_name']}-A-UZB"
    initial_amount = data["product_quantity"] * data["product_price"]

    contract_add(driver, test_data,
                 client_name=client_name,
                 contract_name=contract_name,
                 initial_amount=initial_amount,
                 is_main=False)


@pytest.mark.regression
@pytest.mark.order_group_B
@pytest.mark.order(350)
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
                 initial_amount=initial_amount,
                 is_main=False)


@pytest.mark.regression
@pytest.mark.order_group_C
@pytest.mark.order(390)
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
    sub_filial_name = data["sub_filial_name"]

    contract_add(driver, test_data,
                 client_name=client_name,
                 contract_name=contract_name,
                 currency_cod=currency_cod,
                 currency_name=currency_name,
                 initial_amount=initial_amount,
                 sub_filial_name=sub_filial_name,
                 is_main=False)