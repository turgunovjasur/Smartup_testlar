import pytest
from flows.auth_flow import login_user
from autotest.core.md.base_page import BasePage
from flows.error_message_flow import get_error_massage
from autotest.anor.mdeal.order.order_add.order_add_product import OrderAddProduct
from flows.order_flows.order_add_flow import (
    order_add_main, order_add_product, order_add_final, order_add_step, order_add_product_select)
from flows.order_flows.order_list_flow import order_list, order_view, order_file, order_transaction, order_attach_data

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_A
@pytest.mark.order(29)
def test_add_order_with_consignment_demo(driver, test_data, save_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_order_with_consignment_demo")

    # Test data
    data = test_data["data"]
    room_name = data["room_name"]
    robot_name = data["robot_name"]
    client_name = f"{data['client_name']}-A"
    product_name = data["product_name"]
    warehouse_name = data["warehouse_name"]
    price_type_name = data["price_type_name_UZB"]
    product_quantity = 15
    payment_type_name = data["payment_type_name"]
    consignment_day = 30
    consignment_amount = product_quantity * data["product_price"]
    status_name = data["Draft"]

    # Login
    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_list(driver, add=True)

    order_add_main(driver,
                   room_name=room_name,
                   robot_name=robot_name,
                   client_name=client_name)

    order_add_product(driver,
                      product_name=product_name,
                      warehouse_name=warehouse_name,
                      price_type_name=price_type_name,
                      product_quantity=product_quantity)

    order_add_final(driver,
                    payment_type_name=payment_type_name,
                    consignment_day=consignment_day,
                    consignment_amount=consignment_amount,
                    status_name=status_name)

    order_list(driver, find_row=client_name, view=True)

    input_name = {
        "ИД заказа": "text",
        "Сумма заказа": "numeric",
        "Статус": "text",
        "Клиент": "text",
        "Рабочая зона": "text",
        "Штат": "text"
    }
    get_values = order_view(driver,
                          input_name=input_name,
                          tablist_name="Консигнация",
                          consignment_day=consignment_day,
                          consignment_amount=consignment_amount)

    save_data("order_id_1", get_values["ИД заказа"])

    assert get_values["Штат"] == robot_name,                   f'{get_values["Штат"]} != {robot_name}'
    assert get_values["Статус"] == status_name,                f"{get_values['Статус']} != {status_name}"
    assert get_values["Клиент"] == client_name,                f"{get_values['Клиент']} != {client_name}"
    assert get_values["Рабочая зона"] == room_name,            f"{get_values['Рабочая зона']} != {room_name}"
    assert get_values["Сумма заказа"] == consignment_amount,   f"{get_values['Сумма заказа']} != {consignment_amount}"

    order_list(driver)

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_B
@pytest.mark.order(39)
def test_add_order_with_contract_demo(driver, test_data, save_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_order_with_contract_demo")

    # Test data
    data = test_data["data"]
    room_name = data["room_name"]
    robot_name = data["robot_name"]
    client_name = f"{data['client_name']}-B"
    contract_name = f"{data['contract_name']}-B-UZB"

    product_name = data["product_name"]
    warehouse_name = data["warehouse_name"]
    price_type_name = data["price_type_name_UZB"]
    product_quantity = 101
    return_quantity = 15

    payment_type_name = data["payment_type_name"]
    status_name = data["Draft"]

    # Login
    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_list(driver, add=True)

    order_add_main(driver,
                   room_name=room_name,
                   robot_name=robot_name,
                   client_name=client_name,
                   contract_name=contract_name)

    order_add_product(driver,
                      product_name=product_name,
                      warehouse_name=warehouse_name,
                      price_type_name=price_type_name,
                      product_quantity=product_quantity)

    order_add_final(driver,
                    payment_type_name=payment_type_name,
                    status_name=status_name)

    get_error_massage(driver, error_massage_name=data["error_massage_1"])

    order_add_step(driver, prev_step=True)

    order_add_product(driver, product_quantity=return_quantity)

    order_add_final(driver)

    order_list(driver, find_row=client_name, view=True)

    input_name = {
        "ИД заказа": "text",
        "Сумма заказа": "numeric",
        "Статус": "text",
        "Клиент": "text",
        "Рабочая зона": "text",
        "Штат": "text"
    }
    get_values = order_view(driver, input_name=input_name)

    save_data("order_id_3", get_values["ИД заказа"])

    assert get_values["Штат"] == robot_name,                   f'{get_values["Штат"]} != {robot_name}'
    assert get_values["Статус"] == status_name,                f"{get_values['Статус']} != {status_name}"
    assert get_values["Клиент"] == client_name,                f"{get_values['Клиент']} != {client_name}"
    assert get_values["Рабочая зона"] == room_name,            f"{get_values['Рабочая зона']} != {room_name}"

    order_list(driver)

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_C
@pytest.mark.order(43)
def test_add_order_for_price_type_USA_demo(driver, test_data, save_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_order_for_price_type_USA_demo")

    # Test data
    data = test_data["data"]
    room_name = data["room_name"]
    robot_name = data["robot_name"]
    client_name = f"{data['client_name']}-C"

    product_name = data["product_name"]
    warehouse_name = data["warehouse_name"]
    price_type_name = data["price_type_name_USA"]
    product_quantity = 20
    margin = data["percent_value"]

    payment_type_name = data["payment_type_name"]
    status_name = data["New"]

    # Login
    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_list(driver, add=True)

    order_add_main(driver,
                   room_name=room_name,
                   robot_name=robot_name,
                   client_name=client_name)

    order_add_product(driver,
                      product_name=product_name,
                      warehouse_name=warehouse_name,
                      price_type_name=price_type_name,
                      product_quantity=product_quantity,
                      margin=margin)

    order_add_final(driver, payment_type_name=payment_type_name, status_name=status_name)

    order_list(driver, find_row=client_name, view=True)

    input_name = {
        "ИД заказа": "text",
        "Сумма заказа": "numeric",
        "Статус": "text",
        "Клиент": "text",
        "Рабочая зона": "text",
        "Штат": "text"
    }
    get_values = order_view(driver, input_name=input_name)

    save_data("order_id_4", get_values["ИД заказа"])

    assert get_values["Штат"] == robot_name,                   f'{get_values["Штат"]} != {robot_name}'
    assert get_values["Статус"] == status_name,                f"{get_values['Статус']} != {status_name}"
    assert get_values["Клиент"] == client_name,                f"{get_values['Клиент']} != {client_name}"
    assert get_values["Рабочая зона"] == room_name,            f"{get_values['Рабочая зона']} != {room_name}"

    order_list(driver, reload=True, find_row=client_name, file=True)

    order_file(driver)

    order_list(driver, reload=True, find_row=client_name, transaction=True)

    order_transaction(driver)

    order_list(driver, reload=True, find_row=client_name, attach_data=True)

    order_attach_data(driver)

    order_list(driver)

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order(48)
@pytest.mark.no_ci
def test_add_order_for_sub_filial_demo(driver, test_data, save_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_order_for_sub_filial_demo")

    # Test data
    data = test_data["data"]
    room_name = data["room_name"]
    robot_name = data["robot_name"]
    client_name = f"{data['client_name']}-C"
    sub_filial_name = data["sub_filial_name"]
    contract_name = f"{data['contract_name']}-C-USA"

    warehouse_name = data["warehouse_name"]
    price_type_name = data["price_type_name_USA"]
    product_price_USA = data["product_price_USA"]
    product_quantity = 10
    margin = data["percent_value"]

    payment_type_name = data["payment_type_name"]
    total_amount = (product_quantity * product_price_USA) - ((product_quantity * product_price_USA) * (margin / 100))

    # Login
    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_list(driver, add=True)

    order_add_main(driver,
                   room_name=room_name,
                   robot_name=robot_name,
                   client_name=client_name,
                   sub_filial_name=sub_filial_name,
                   contract_name=contract_name)

    order_add_product_select(driver,
                             warehouse_name=warehouse_name,
                             price_type_name=price_type_name,
                             product_quantity=product_quantity,
                             margin=margin)

    order_add_step(driver, next_step=True)

    order_add_final(driver, payment_type_name=payment_type_name, status_name=data["New"])

    order_list(driver, find_row=client_name, view=True)

    input_name = {
        "ИД заказа": "text",
        "Сумма заказа": "numeric",
        "Статус": "text",
        "Клиент": "text",
        "Рабочая зона": "text",
        "Штат": "text",
        "Проект": "text"
    }
    get_values = order_view(driver, input_name=input_name)

    save_data("order_id_5", get_values["ИД заказа"])

    assert get_values["Штат"] == robot_name,           f'{get_values["Штат"]} != {robot_name}'
    assert get_values["Статус"] == data["New"],        f"{get_values['Статус']} != {data['New']}"
    assert get_values["Клиент"] == client_name,        f"{get_values['Клиент']} != {client_name}"
    assert get_values["Рабочая зона"] == room_name,    f"{get_values['Рабочая зона']} != {room_name}"
    assert get_values["Проект"] == sub_filial_name,    f"{get_values['Проект']} != {sub_filial_name}"
    assert get_values["Сумма заказа"] == total_amount, f"{get_values['Сумма заказа']} != {total_amount}"

    order_list(driver)

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order(52)
def test_add_order_for_action_demo(driver, test_data, save_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_order_for_action_demo")

    # Test data
    data = test_data["data"]
    room_name = data["room_name"]
    robot_name = data["robot_name"]
    client_name = f"{data['client_name']}-C"
    sub_filial_name = data["sub_filial_name"]
    contract_name = f"{data['contract_name']}-C-USA"

    warehouse_name = data["warehouse_name"]
    product_name = data["product_name"]
    price_type_name = data["price_type_name_USA"]
    product_price = data["product_price_USA"]
    product_quantity = 10
    percent_value = 10

    payment_type_name = data["payment_type_name"]

    # Login
    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_list(driver, add=True)

    order_add_main(driver,
                   room_name=room_name,
                   robot_name=robot_name,
                   client_name=client_name,
                   sub_filial_name=sub_filial_name,
                   contract_name=contract_name)

    order_add_product(driver,
                      product_name=product_name,
                      warehouse_name=warehouse_name,
                      price_type_name=price_type_name,
                      product_quantity=product_quantity,
                      next_step=False)

    order_add_tablist = OrderAddProduct(driver)
    order_add_tablist.click_nav_tablist_button(tablist_name="Акции")
    order_add_tablist.click_action_checkbox_button()
    order_add_tablist.click_nav_tablist_button(tablist_name="Товар")

    order_add_step(driver, next_step=True)

    get_total_amount = order_add_final(driver,
                                       payment_type_name=payment_type_name,
                                       get_total_amount=True,
                                       status_name=data["New"])
    total_amount = (product_quantity * product_price) - ((product_quantity * product_price) * (percent_value / 100))  # 120-(120*10%)
    assert get_total_amount["total_amount"] == total_amount, f"Error: {get_total_amount['total_amount']} != {total_amount}"

    order_list(driver, find_row=client_name, view=True)

    input_name = {
        "ИД заказа": "text",
        "Сумма заказа": "numeric",
        "Статус": "text",
        "Клиент": "text",
        "Рабочая зона": "text",
        "Штат": "text",
        "Проект": "text"
    }
    get_values = order_view(driver, input_name=input_name)

    save_data("order_id_6", get_values["ИД заказа"])

    assert get_values["Штат"] == robot_name,           f'{get_values["Штат"]} != {robot_name}'
    assert get_values["Статус"] == data["New"],        f"{get_values['Статус']} != {data['New']}"
    assert get_values["Клиент"] == client_name,        f"{get_values['Клиент']} != {client_name}"
    assert get_values["Рабочая зона"] == room_name,    f"{get_values['Рабочая зона']} != {room_name}"
    assert get_values["Проект"] == sub_filial_name,    f"{get_values['Проект']} != {sub_filial_name}"
    assert get_values["Сумма заказа"] == total_amount, f"{get_values['Сумма заказа']} != {total_amount}"

    order_list(driver)

# ======================================================================================================================
