import time
import random

import pytest

from autotest.anor.mdeal.order.offset.offset.offset import Offset
from autotest.anor.mdeal.order.offset.offset_detail_list.offset_detail_list import OffsetDetailList
from autotest.anor.mdeal.order.offset.offset_list.offset_list import OffsetList
from autotest.core.md.base_page import BasePage
from autotest.trade.tcs.cashin_add.cashin_add import CashinAdd
from autotest.trade.tcs.cashin_list.cashin_list import CashinList
from autotest.trade.tcs.cashin_view.cashin_view import CashinView
from tests.test_base.test_base import test_data, login_user
from utils.driver_setup import driver


def cashin_add(driver, test_data, client_name=None, login=True, amount=None):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): cashin_add")

    # Test data
    data = test_data["data"]
    payment_type_name = data["payment_type_name"]
    cashbox_name = data["cash_register_name"]
    client_name = client_name if client_name is not None else data["client_name"]

    try:
        # Login
        if login:
            login_user(driver, test_data, url='trade/tcs/cashin_list')

        # Cashin List
        cashin_list = CashinList(driver)
        assert cashin_list.element_visible(), base_page.logger.error('CashinList not open!')
        cashin_list.click_add_button()

        # Cashin Add
        cashin_add = CashinAdd(driver)
        assert cashin_add.element_visible(), base_page.logger.error('CashinAdd not open!')
        cashin_number = random.randint(1, 999999)
        cashin_add.input_cashin_number(cashin_number)
        cashin_add.input_clients(client_name)

        input_amount = amount if amount is not None else cashin_add.get_amount()
        cashin_add.input_amount(input_amount)

        cashin_add.input_payment_types(payment_type_name)
        cashin_add.input_cashbox(cashbox_name)
        cashin_add.click_save_button()
        cashin_add.click_close_button()

        # Cashin List
        assert cashin_list.element_visible(), base_page.logger.error('CashinList not open!')
        cashin_list.find_row(cashin_number)
        cashin_list.click_view_button()

        # Cashin View
        cashin_view = CashinView(driver)
        assert cashin_view.element_visible(), base_page.logger.error('CashinView not open!')
        text = cashin_view.check_cashin_number()
        assert cashin_number == text, base_page.logger.error(f'cashin_number: {cashin_number} != text: {text}')
        cashin_view.click_close_button()

        # Cashin List
        assert cashin_list.element_visible(), base_page.logger.error('CashinList not open!')
        cashin_list.find_row(cashin_number)
        cashin_list.click_post_button()

    except AssertionError as ae:
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        pytest.fail(str(e))


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


# ----------------------------------------------------------------------------------------------------------------------

def offset_add(driver, test_data, client_name=None, payment=False):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): cashin_add")

    # Test data
    data = test_data["data"]
    cash_register_name = data["cash_register_name"]
    client_name = client_name if client_name is not None else data["client_name"]

    try:
        # Login
        login_user(driver, test_data, url='anor/mdeal/order/offset/offset_list')

        offset_list = OffsetList(driver)
        assert offset_list.element_visible(), base_page.logger.error('OffsetList not open!')
        offset_list.find_row(client_name)
        offset_list.click_detail_button()

        # Offset Detail List
        offset_detail_list = OffsetDetailList(driver)
        assert offset_detail_list.element_visible(), base_page.logger.error('OffsetDetailList not open!')
        offset_detail_list.find_row(client_name)

        if payment is False:
            offset_detail_list.click_offset_button()

            # Offset Detail List
            offset = Offset(driver)
            assert offset.element_visible(), base_page.logger.error('Offset not open!')
            assert offset.find_row(client_name), base_page.logger.error(f'Error: Automatic price button did not work')
            check_balance = offset.check_balance(client_name)
            assert check_balance == 0, \
                base_page.logger.error(f'Error: Balance is not equal to zero. -> {check_balance} != {0}')

            offset.click_post_button()
            offset.click_close_button()
            time.sleep(2)

        if payment is True:
            offset_detail_list.click_payment_button()

            # Offset Detail List
            offset = Offset(driver)
            assert offset.element_visible(), base_page.logger.error('Offset not open!')
            assert offset.find_row(client_name), base_page.logger.error(f'Error: Automatic price button did not work')
            offset.input_cashboxes(cash_register_name)
            check_balance_payment = offset.check_balance_payment(client_name)
            offset.click_post_button()
            offset.click_yes_button()
            offset.click_close_button()

            # Cashin List
            base_page = BasePage(driver)
            cut_url = base_page.cut_url()
            base_page.open_new_window(cut_url + 'trade/tcs/cashin_list')
            cashin_list = CashinList(driver)
            assert cashin_list.element_visible(), base_page.logger.error('CashinList not open!')
            cashin_list.find_row(client_name)
            cashin_list.click_view_button()

            # Cashin View
            cashin_view = CashinView(driver)
            assert cashin_view.element_visible(), base_page.logger.error('CashinView not open!')
            get_cashin_number = cashin_view.check_cashin_number()
            get_client_name = cashin_view.check_client_name()
            assert client_name == get_client_name, \
                base_page.logger.error(f'client_name: {client_name} != get_client_name: {get_client_name}')
            get_total_price = cashin_view.check_total_price()
            assert check_balance_payment == get_total_price, \
                base_page.logger.error(
                    f'check_balance_payment: {check_balance_payment} != get_total_price: {get_total_price}')
            base_page.logger.info(f'get_cashin_number: {get_cashin_number}')
            cashin_view.click_close_button()

    except AssertionError as ae:
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        pytest.fail(str(e))


def test_offset_add_A(driver, test_data):
    data = test_data["data"]
    client_name = f'{data["client_name"]}-A'
    offset_add(driver, test_data, client_name=client_name)


def test_offset_add_B(driver, test_data):
    data = test_data["data"]
    client_name = f'{data["client_name"]}-B'
    offset_add(driver, test_data,
               client_name=client_name,
               payment=True)


def test_offset_add_C(driver, test_data):
    data = test_data["data"]
    client_name = f'{data["client_name"]}-C'
    offset_add(driver, test_data, client_name=client_name)

# ----------------------------------------------------------------------------------------------------------------------
