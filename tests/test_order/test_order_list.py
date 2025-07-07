import time
import pytest
from autotest.core.md.base_page import BasePage
from flows.auth_flow import login_user
from flows.order_flows.order_list_flow import order_list, order_view, order_copy, order_search_input, order_filter_panel

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_A
@pytest.mark.order(32)
def test_copy_search_filter_in_order_list_demo(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_copy_search_filter_in_order_list_demo")

    # Test data
    data = test_data["data"]
    client_name_A = f"{data['client_name']}-A"
    client_name_B = f"{data['client_name']}-B"

    room_name = data["room_name"]
    robot_name = data["robot_name"]
    total_amount = data["product_price"] * 10

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_list(driver, find_row=client_name_A, copy=True)

    order_copy(driver, copy_client_name=client_name_B)

    order_list(driver, find_row=client_name_B, view=True)

    get_values = order_view(driver, input_name = {"ИД заказа": "text", "Сумма заказа": "numeric", "Статус": "text",
                                                  "Клиент": "text", "Рабочая зона": "text", "Штат": "text"})

    save_data("order_id_2", get_values["ИД заказа"])

    assert get_values["Штат"] == robot_name,                   f"{get_values['Штат']} != {robot_name}"
    assert get_values["Статус"] == data["Draft"],              f"{get_values['Статус']} != {data['Draft']}"
    assert get_values["Клиент"] == client_name_B,              f"{get_values['Клиент']} != {client_name_B}"
    assert get_values["Рабочая зона"] == room_name,            f"{get_values['Рабочая зона']} != {room_name}"
    assert get_values["Сумма заказа"] == total_amount,         f"{get_values['Сумма заказа']} != {total_amount}"

    order_list(driver, reload=True)

    order_id_2 = load_data("order_id_2")
    order_search_input(driver, search_data=order_id_2, clear=True)

    order_filter_panel(driver, open_panel=True, option_header="Клиент", option_name=client_name_A, state=False)
    time.sleep(1)
    order_filter_panel(driver, option_header="Клиент", option_name=client_name_B)
    time.sleep(1)
    order_filter_panel(driver, show_all=True, option_name=client_name_A, close_panel=True)

# ======================================================================================================================
