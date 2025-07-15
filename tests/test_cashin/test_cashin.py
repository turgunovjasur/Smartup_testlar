import random
import time
import pytest
from autotest.trade.tcs.cashin_add.cashin_add import CashinAdd
from autotest.trade.tcs.cashin_list.cashin_list import CashinList
from autotest.trade.tcs.cashin_view.cashin_view import CashinView
from flows.auth_flow import login_user


def cashin_add(driver, test_data, client_name, login=True, amount=None):
    # Test data
    data = test_data["data"]
    payment_type_name = data["payment_type_name"]
    cashbox_name = data["cash_register_name"]
    client_name = client_name

    # Login
    if login:
        login_user(driver, test_data, url='trade/tcs/cashin_list')

    # Cashin List
    cashin_list = CashinList(driver)
    cashin_list.element_visible()
    cashin_list.click_add_button()

    # Cashin Add
    cashin_add = CashinAdd(driver)
    cashin_add.element_visible()
    cashin_number = random.randint(1, 999999)
    cashin_add.input_cashin_number(cashin_number)
    cashin_add.input_clients(client_name)
    cashin_add.input_contracts(clear=True)

    input_amount = amount or cashin_add.get_amount()
    if input_amount == 0:
        time.sleep(2)
        input_amount = cashin_add.get_amount()
    cashin_add.input_amount(input_amount)

    cashin_add.input_payment_types(payment_type_name)
    cashin_add.input_cashbox(cashbox_name)
    cashin_add.click_save_button()
    cashin_add.click_close_button()

    # Cashin List
    cashin_list.element_visible()
    cashin_list.find_row(cashin_number)
    cashin_list.click_view_button()

    # Cashin View
    cashin_view = CashinView(driver)
    cashin_view.element_visible()
    text = cashin_view.check_cashin_number()
    assert cashin_number == text, f'cashin_number: {cashin_number} != text: {text}'
    cashin_view.click_close_button()

    # Cashin List
    cashin_list.element_visible()
    cashin_list.find_row(cashin_number)
    cashin_list.click_post_button()
    time.sleep(2)


@pytest.mark.regression
@pytest.mark.order_group_A
@pytest.mark.order(36)
def test_cashin_add_A(driver, test_data):
    data = test_data["data"]
    client_name = f'{data["client_name"]}-A'
    cashin_add(driver, test_data, client_name=client_name)


def test_cashin_add_B(driver, test_data):
    data = test_data["data"]
    client_name = f'{data["client_name"]}-B'
    cashin_add(driver, test_data, client_name=client_name)


def test_cashin_add_C(driver, test_data, amount=1_000_00):
    data = test_data["data"]
    client_name = f'{data["client_name"]}-C'
    cashin_add(driver, test_data, client_name=client_name, login=False, amount=amount)
