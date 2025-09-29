import time
import pytest
from pages.core.md.base_page import BasePage
from pages.anor.mdeal.order.offset.offset.offset import Offset
from pages.trade.tcs.cashin_list.cashin_list import CashinList
from pages.trade.tcs.cashin_view.cashin_view import CashinView
from pages.anor.mdeal.order.offset.offset_list.offset_list import OffsetList
from pages.anor.mdeal.order.offset.offset_detail_list.offset_detail_list import OffsetDetailList
from flows.auth_flow import login_user


def offset_add(driver, test_data, client_name=None, payment=False):
    # Log
    base_page = BasePage(driver)

    # Test data
    data = test_data["data"]
    cash_register_name = data["cash_register_name"]
    client_name = client_name or data["client_name"]

    # Login
    login_user(driver, test_data, url='anor/mdeal/order/offset/offset_list')

    offset_list = OffsetList(driver)
    offset_list.element_visible()
    offset_list.find_row(client_name)
    offset_list.click_detail_button()

    # Offset Detail List
    offset_detail_list = OffsetDetailList(driver)
    offset_detail_list.element_visible()
    offset_detail_list.find_row(client_name)

    if payment is False:
        offset_detail_list.click_offset_button()

        # Offset Detail List
        offset = Offset(driver)
        offset.element_visible()
        offset.find_row(client_name)
        check_balance = offset.check_balance(client_name)
        assert check_balance == 0, f'Error: Balance is not equal to zero. -> {check_balance} != {0}'

        offset.click_post_button()
        offset.click_close_button()
        time.sleep(2)

    if payment is True:
        offset_detail_list.click_payment_button()

        # Offset Detail List
        offset = Offset(driver)
        offset.element_visible()
        offset.find_row(client_name)
        offset.input_cashboxes(cash_register_name)
        check_balance_payment = offset.check_balance_payment(client_name)
        offset.click_post_button()
        offset.click_yes_button()
        offset.click_close_button()

        # Cashin List
        base_page.switch_window(direction="prepare")
        cut_url = base_page.cut_url()
        base_page.switch_window(direction="new", url=cut_url + 'trade/tcs/cashin_list')
        cashin_list = CashinList(driver)
        cashin_list.element_visible()
        cashin_list.find_row(client_name)
        cashin_list.click_view_button()

        # Cashin View
        cashin_view = CashinView(driver)
        cashin_view.element_visible()
        get_cashin_number = cashin_view.check_cashin_number()
        get_client_name = cashin_view.check_client_name()
        assert client_name == get_client_name, f'client_name: {client_name} != get_client_name: {get_client_name}'
        get_total_price = cashin_view.check_total_price()
        assert check_balance_payment == get_total_price, f'check_balance_payment: {check_balance_payment} != get_total_price: {get_total_price}'
        base_page.logger.info(f'get_cashin_number: {get_cashin_number}')
        cashin_view.click_close_button()


@pytest.mark.regression
@pytest.mark.order_group_A
@pytest.mark.order(340)
def test_offset_add_A(driver, test_data):
    data = test_data["data"]
    client_name = f'{data["client_name"]}-A'
    offset_add(driver, test_data, client_name=client_name)


@pytest.mark.regression
@pytest.mark.order_group_B
@pytest.mark.order(380)
def test_offset_add_B(driver, test_data):
    data = test_data["data"]
    client_name = f'{data["client_name"]}-B'
    offset_add(driver, test_data, client_name=client_name, payment=True)