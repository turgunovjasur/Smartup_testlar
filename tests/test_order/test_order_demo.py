from autotest.trade.rep.mbi.tdeal.order.sales_report_constructor import SalesReportConstructor
from flows.grid_setting_flow import grid_setting
from flows.order_flows.order_add_flow import *
from flows.order_flows.order_list_flow import *
from flows.auth_flow import *

# ======================================================================================================================

def test_add_order_with_basic_fields(driver, test_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_order_with_basic_fields")

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

    order_add_final(driver, payment_type_name=payment_type_name, status=1)

    order_list(driver, find_row=client_name)
    order_list(driver, view=True)

    order_id = order_view(driver)
    base_page.logger.info(f"Order ID: {order_id}")

    order_list(driver)

# ======================================================================================================================

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

def test_edit_order_with_consignment_demo(driver, test_data, load_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_edit_order_with_consignment_demo")

    data = test_data["data"]

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    grid_setting(driver, option_name="deal_id", search_type="ИД заказа")

    order_id_1 = load_data("order_id_1")
    order_list(driver, find_row=order_id_1, edit=True)

    order_add_main(driver)

    order_add_product(driver, product_quantity=10)

    get_order_error_massage(driver, error_massage_name=data["error_massage_2"])

    order_add_final(driver, status_name=data["Draft"])

    order_list(driver, find_row=order_id_1, view=True)

    order_view(driver, tablist_name="Консигнация", consignment_empty=True)

    order_list(driver, change_status=data["New"])

# ======================================================================================================================

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
    order_filter_panel(driver, option_header="Клиент", option_name=client_name_B)
    order_filter_panel(driver, show_all=True, option_name=client_name_A, close_panel=True)

# ======================================================================================================================

def test_sales_report_constructor_demo(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_sales_report_constructor_demo")

    login_user(driver, test_data, url='trade/rep/mbi/tdeal/order')

    sales_report_constructor = SalesReportConstructor(driver)
    sales_report_constructor.input_search_value(value_name="Заказ")
    sales_report_constructor.click_source_and_target(option_name="Заказ", field_name="row")
    sales_report_constructor.click_view_button()
    time.sleep(2)

# ======================================================================================================================

def test_order_change_status_demo(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_order_change_status_demo")

    data = test_data["data"]

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_id_2 = load_data("order_id_2")

    # Status: Draft -> New
    status_name = data["New"]
    order_list(driver, find_row=order_id_2, change_status=status_name)
    order_list(driver, find_row=order_id_2, view=True)
    get_values = order_view(driver, input_name="Статус")
    assert get_values["Статус"] == status_name, f"{get_values['Статус']} != {status_name}"
    order_list(driver, reload=True)

    # Status: New -> Processing
    status_name = data["Processing"]
    order_list(driver, find_row=order_id_2, change_status=status_name)
    order_list(driver, find_row=order_id_2, view=True)
    get_values = order_view(driver, input_name="Статус")
    assert get_values["Статус"] == status_name, f"{get_values['Статус']} != {status_name}"
    order_list(driver, reload=True)

    # Status: Processing -> Pending
    status_name = data["Pending"]
    order_list(driver, find_row=order_id_2, change_status=status_name)
    order_list(driver, find_row=order_id_2, view=True)
    get_values = order_view(driver, input_name="Статус")
    assert get_values["Статус"] == status_name, f"{get_values['Статус']} != {status_name}"
    order_list(driver, reload=True)

    # Status: Pending -> Shipped
    status_name = data["Shipped"]
    order_list(driver, find_row=order_id_2, change_status=status_name)
    order_list(driver, find_row=order_id_2, view=True)
    get_values = order_view(driver, input_name="Статус")
    assert get_values["Статус"] == status_name, f"{get_values['Статус']} != {status_name}"
    order_list(driver, reload=True)

    # Status: Shipped -> Delivered
    status_name = data["Delivered"]
    order_list(driver, find_row=order_id_2, change_status=status_name)
    order_list(driver, find_row=order_id_2, view=True)
    get_values = order_view(driver, input_name="Статус")
    assert get_values["Статус"] == status_name, f"{get_values['Статус']} != {status_name}"
    order_list(driver, reload=True)

# ======================================================================================================================

def test_order_demo_all(driver, test_data, save_data, load_data):
    test_add_order_with_consignment_demo(driver, test_data, save_data)
    test_edit_order_with_consignment_demo(driver, test_data, load_data)
    test_copy_search_filter_in_order_list_demo(driver, test_data, save_data, load_data)
    test_sales_report_constructor_demo(driver, test_data, save_data, load_data)