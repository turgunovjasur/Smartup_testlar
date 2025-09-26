import pytest
from autotest.core.md.base_page import BasePage
from flows.auth_flow import login_user
from flows.modal_content_flow import get_error_massage_flow
from flows.grid_setting_flow import grid_setting
from flows.order_flows.order_add_flow import main_flow, product_flow, final_flow
from flows.order_flows.order_list_flow import order_list, order_view
from tests.test_cashin.test_cashin import test_cashin_add_C

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_A
@pytest.mark.order(270)
def test_edit_order_with_consignment_demo(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_edit_order_with_consignment_demo")

    data = test_data["data"]

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    grid_setting(driver, option_name="deal_id", search_type="ИД заказа")

    order_id_1 = load_data("order_id_1")
    order_list(driver, find_row=order_id_1, edit=True)

    main_flow(driver)

    product_flow(driver, product_quantity=10)

    get_error_massage_flow(driver, error_massage_name=data["error_massage_2"])

    final_flow(driver, status_name=data["Draft"])

    order_list(driver, find_row=order_id_1, view=True)

    order_view(driver, tablist_name="Консигнация", consignment_empty=True)

    order_list(driver, change_status=data["New"])

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_C
@pytest.mark.order(420)
def test_edit_order_for_price_type_USA_demo(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_edit_order_for_price_type_USA_demo")

    data = test_data["data"]
    product_name = data["product_name"]
    warehouse_name = data["warehouse_name"]
    price_type_name = data["price_type_name_UZB"]
    product_quantity_edit = 10
    cashin_amount = product_quantity_edit * data["product_price"]
    prepayment_amount = cashin_amount / 2

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_id_4 = load_data("order_id_4")
    order_list(driver, find_row=order_id_4, edit=True)

    main_flow(driver)

    product_flow(driver, clear_input=True, product_name=product_name, warehouse_name=warehouse_name,
                 price_type_name=price_type_name, product_quantity=product_quantity_edit)

    final_flow(driver, status_name=data["Delivered"])

    get_error_massage_flow(driver, error_massage_name=data["error_massage_3"])

    base_page.switch_window(direction="prepare")
    cut_url = base_page.cut_url()
    base_page.switch_window(direction="new", url=cut_url + 'trade/tcs/cashin_list')
    test_cashin_add_C(driver, test_data, amount=cashin_amount)
    base_page.switch_window(direction="back")
    base_page.refresh_page()

    main_flow(driver)

    product_flow(driver, clear_input=True, product_name=product_name, warehouse_name=warehouse_name,
                 price_type_name=price_type_name, product_quantity=product_quantity_edit)

    final_flow(driver, prepayment_amount=(prepayment_amount - 1), status_name=data["Processing"])

    order_list(driver, find_row=order_id_4, change_status=data["Delivered"])

    get_error_massage_flow(driver, error_massage_name=data["error_massage_3"])

    order_list(driver, reload=True, find_row=order_id_4, edit=True)

    main_flow(driver)

    product_flow(driver)

    final_flow(driver, prepayment_amount=(prepayment_amount - 1), status_name=data["Pending"])

    order_list(driver, reload=True, find_row=order_id_4, change_status=data["Shipped"])

    order_list(driver, reload=True, find_row=order_id_4, change_status=data["Delivered"])

    get_error_massage_flow(driver, error_massage_name=data["error_massage_3"])

    order_list(driver, reload=True, find_row=order_id_4, change_status=data["New"])

    order_list(driver, reload=True, find_row=order_id_4, edit=True)

    main_flow(driver)

    product_flow(driver)

    final_flow(driver, prepayment_amount=prepayment_amount, status_name=data["New"])

    order_list(driver, reload=True, find_row=order_id_4, change_status=data["Delivered"])

    order_list(driver, find_row=order_id_4, view=True)

    get_values = order_view(driver, input_name="Статус")

    assert get_values["Статус"] == data["Delivered"], f"{get_values['Статус']} != {data['Delivered']}"

    order_list(driver)

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order(500)
def test_edit_order_for_action_demo(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_edit_order_for_action_demo")

    data = test_data["data"]
    robot_name = data["robot_name"]
    room_name = data["room_name"]
    sub_filial_name = data["sub_filial_name"]
    product_price = data["product_price_USA"]
    client_name = f"{data['client_name']}-C"
    edit_product_quantity = 8

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_id_6 = load_data("order_id_6")
    order_list(driver, find_row=order_id_6, edit=True)

    main_flow(driver)

    product_flow(driver, product_quantity=edit_product_quantity)


    get_total_amount = final_flow(driver, get_total_amount=True, status_name=data["New"])

    total_amount = edit_product_quantity * product_price  # 8*12=96
    assert get_total_amount["total_amount"] == total_amount

    order_list(driver, find_row=order_id_6, view=True)

    input_name = {
        "Сумма заказа": "numeric",
        "Статус": "text",
        "Клиент": "text",
        "Рабочая зона": "text",
        "Штат": "text",
        "Проект": "text"
    }
    get_values = order_view(driver, input_name=input_name)

    assert get_values["Штат"] == robot_name,           f'{get_values["Штат"]} != {robot_name}'
    assert get_values["Статус"] == data["New"],        f"{get_values['Статус']} != {data['New']}"
    assert get_values["Клиент"] == client_name,        f"{get_values['Клиент']} != {client_name}"
    assert get_values["Рабочая зона"] == room_name,    f"{get_values['Рабочая зона']} != {room_name}"
    assert get_values["Проект"] == sub_filial_name,    f"{get_values['Проект']} != {sub_filial_name}"
    assert get_values["Сумма заказа"] == total_amount, f"{get_values['Сумма заказа']} != {total_amount}"

    order_list(driver)

# ======================================================================================================================
