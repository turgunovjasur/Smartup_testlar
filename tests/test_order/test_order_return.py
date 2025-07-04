import pytest

from autotest.anor.mdeal.order.order_view.order_view import OrderView
from autotest.core.md.base_page import BasePage
from autotest.trade.tdeal.order.order_list.orders_list import OrdersList
from autotest.trade.tdeal.order.return_order.return_order import ReturnOrder
from flows.auth_flow import login_user


def order_return(driver, test_data, client_name=None):
    base_page = BasePage(driver)

    # Log
    data = test_data["data"]

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    # List
    order_list = OrdersList(driver)
    order_list.element_visible()
    order_list.find_row(client_name)
    order_list.click_view_button()

    # View
    order_view = OrderView(driver)
    order_view.element_visible()
    get_order_id = order_view.get_input_value_in_order_view(input_name="ИД заказа")
    get_status = order_view.get_input_value_in_order_view(input_name="Статус")
    assert get_status == data["Delivered"], f'{get_status} != {data["Delivered"]}'
    get_quantity, get_price, total_sum = order_view.check_items()
    base_page.logger.info(
        f"OrderView: success checked: order_id: {get_order_id}, order_status: {get_status}, order_price: {get_price}")
    order_view.click_close_button()

    # List
    order_list.element_visible()
    order_list.click_return_button()

    # Return Order
    return_order = ReturnOrder(driver)
    return_order.element_visible()
    get_client_name = return_order.check_client_name()
    assert get_client_name == client_name, f"{get_client_name} != {client_name}"
    return_order.click_return_all_button()
    get_total_price = return_order.check_total_price()
    assert get_total_price == '0', f"Error: get_total_price: {get_total_price} != {'0'}"
    return_order.click_save_button()

    # List
    order_list.element_visible()
    order_list.find_row(client_name)
    order_list.click_view_button()

    # Order View
    order_view.element_visible()
    get_order_id_last = order_view.get_input_value_in_order_view(input_name="ИД заказа")
    assert get_order_id == get_order_id_last, f'{get_order_id} != {get_order_id_last}'
    get_status_last = order_view.get_input_value_in_order_view(input_name="Статус")
    assert get_status_last == data["Delivered"], f'{get_status_last} != {data["Delivered"]}'
    get_quantity, get_price, total_sum = order_view.check_items()
    assert get_price == 0, f"Error: get_price: {get_price} != fact: {0}"
    order_view.click_close_button()

    # List
    order_list.element_visible()
    order_list.click_change_status_button(data["Cancelled"])
    order_list.element_visible()

@pytest.mark.regression
@pytest.mark.order(55)
def test_order_return(driver, test_data):
    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    order_return(driver, test_data, client_name=client_name)