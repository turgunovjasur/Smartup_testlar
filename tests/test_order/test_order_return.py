import time
import pytest
from conftest import load_data
from flows.auth_flow import login_user
from flows.order_flows.order_list_flow import order_list, order_view
from autotest.trade.tdeal.order.return_order.return_order import ReturnOrder


@pytest.mark.regression
@pytest.mark.order(55)
def test_order_return(driver, test_data, load_data):

    data = test_data["data"]

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_id_6 = load_data("order_id_6")
    order_list(driver, find_row=order_id_6, view=True)

    # View
    get_values_after = order_view(driver, input_name=["Сумма заказа", "Статус", "Клиент"])

    assert get_values_after["Статус"] == data["Delivered"], f"{get_values_after['Статус']} != {data['Delivered']}"

    order_list(driver, reload=True, find_row=order_id_6, order_return=True)

    # Return Order
    return_order = ReturnOrder(driver)
    return_order.element_visible()
    get_client_name = return_order.check_client_name()
    assert get_values_after["Клиент"] == get_client_name, f"{get_values_after['Клиент']} != {get_client_name}"

    return_order.click_return_all_button()
    time.sleep(1)
    get_total_amount = return_order.check_total_price()
    assert get_total_amount == '0', f"Error: get_total_price: {get_total_amount} != {'0'}"
    return_order.click_save_button()

    order_list(driver, reload=True, find_row=order_id_6, view=True)

    get_values_before = order_view(driver, input_name=["Сумма заказа", "Статус", "Клиент"])

    assert get_values_after["Статус"] == get_values_before["Статус"], \
        f"{get_values_after['Статус']} != {get_values_before['Статус']}"

    assert get_values_before["Сумма заказа"] == get_total_amount, \
        f"{get_values_before['Сумма заказа']} != {get_total_amount}"

    order_list(driver, reload=True, find_row=order_id_6, change_status=data["Cancelled"])

    order_list(driver)