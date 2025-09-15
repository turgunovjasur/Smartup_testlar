from datetime import datetime
import pytest
from conftest import soft_assertions
from flows.auth_flow import login_user
from flows.modal_content_flow import get_error_massage_flow
from autotest.anor.mdeal.order.order_add.order_add_product import OrderAddProduct
from flows.grid_setting_flow import grid_setting_in_form
from flows.modal_content_flow import get_biruni_confirm_flow
from flows.order_flows.order_add_flow import (
    main_flow, product_flow, final_flow, step_flow, product_select_flow, final_input_value_flow)
from flows.order_flows.order_list_flow import order_list, order_view, order_file, order_transaction, order_attach_data

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_A
@pytest.mark.order(29)
def test_add_order_with_consignment_demo(driver, test_data, save_data, soft_assertions, assertions):
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

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_list(driver, add=True)

    deal_time = datetime.today().strftime("%d.%m.%Y %H:%M")
    result = main_flow(driver,
                       get_deal_time=True,
                       get_delivery_date=True,
                       room_name=room_name,
                       robot_name=robot_name,
                       client_name=client_name)

    assertions.assert_equals(result["natural_person"], data["natural_person_name"])
    assertions.assert_equals(result["deal_time"], deal_time)
    assertions.assert_contains(deal_time, result["delivery_date"])

    product_flow(driver, order_grid_setting=True, next_step=False)
    grid_setting_in_form(driver)
    product_flow(driver,
                 product_name=product_name,
                 warehouse_name=warehouse_name,
                 price_type_name=price_type_name,
                 product_quantity=product_quantity)

    final_flow(driver, order_grid_setting=True)
    grid_setting_in_form(driver)
    final_input_value_flow(driver,
                           client_name=client_name,
                           deal_time=deal_time,
                           delivery_date=deal_time,
                           room_name=room_name,
                           robot_name=robot_name)
    final_flow(driver,
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

    soft_assertions.assert_equals(get_values["Штат"], robot_name)
    soft_assertions.assert_equals(get_values["Статус"], status_name)
    soft_assertions.assert_equals(get_values["Клиент"], client_name)
    soft_assertions.assert_equals(get_values["Рабочая зона"], room_name)
    soft_assertions.assert_equals(get_values["Сумма заказа"], consignment_amount)
    soft_assertions.assert_all()

    order_list(driver)

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_B
@pytest.mark.order(39)
def test_add_order_with_contract_demo(driver, test_data, save_data, soft_assertions):
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

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_list(driver, add=True)

    main_flow(driver,
              room_name=room_name,
              robot_name=robot_name,
              client_name=client_name,
              contract_name=contract_name)

    product_flow(driver,
                 product_name=product_name,
                 warehouse_name=warehouse_name,
                 price_type_name=price_type_name,
                 product_quantity=product_quantity)

    final_flow(driver, payment_type_name=payment_type_name, status_name=status_name)

    get_error_massage_flow(driver, error_massage_name=data["error_massage_1"])

    step_flow(driver, prev_step=True)

    product_flow(driver, product_quantity=return_quantity)

    final_flow(driver)

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

    soft_assertions.assert_equals(get_values["Штат"], robot_name)
    soft_assertions.assert_equals(get_values["Статус"], status_name)
    soft_assertions.assert_equals(get_values["Клиент"], client_name)
    soft_assertions.assert_equals(get_values["Рабочая зона"], room_name)
    soft_assertions.assert_all()

    order_list(driver)

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_C
@pytest.mark.order(43)
def test_add_order_for_price_type_USA_demo(driver, test_data, save_data, soft_assertions):
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

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_list(driver, add=True)

    main_flow(driver,
              room_name=room_name,
              robot_name=robot_name,
              client_name=client_name)

    product_flow(driver,
                 product_name=product_name,
                 warehouse_name=warehouse_name,
                 price_type_name=price_type_name,
                 product_quantity=product_quantity,
                 margin=margin)

    final_flow(driver, payment_type_name=payment_type_name, status_name=status_name)

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

    soft_assertions.assert_equals(get_values["Штат"], robot_name)
    soft_assertions.assert_equals(get_values["Статус"], status_name)
    soft_assertions.assert_equals(get_values["Клиент"], client_name)
    soft_assertions.assert_equals(get_values["Рабочая зона"], room_name)
    soft_assertions.assert_all()

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
def test_add_order_for_sub_filial_demo(driver, test_data, save_data, soft_assertions):
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

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_list(driver, add=True)

    main_flow(driver,
              room_name=room_name,
              robot_name=robot_name,
              client_name=client_name,
              sub_filial_name=sub_filial_name,
              contract_name=contract_name)

    product_select_flow(driver,
                        warehouse_name=warehouse_name,
                        price_type_name=price_type_name,
                        product_quantity=product_quantity,
                        margin=margin)

    step_flow(driver, next_step=True)

    final_flow(driver, payment_type_name=payment_type_name, status_name=data["New"])

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

    soft_assertions.assert_equals(get_values["Штат"], robot_name)
    soft_assertions.assert_equals(get_values["Статус"], data["New"])
    soft_assertions.assert_equals(get_values["Клиент"], client_name)
    soft_assertions.assert_equals(get_values["Рабочая зона"], room_name)
    soft_assertions.assert_equals(get_values["Проект"], sub_filial_name)
    soft_assertions.assert_equals(get_values["Сумма заказа"], total_amount)
    soft_assertions.assert_all()

    order_list(driver)

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order(52)
def test_add_order_for_action_demo(driver, test_data, save_data, assertions, soft_assertions):
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
    margin = data["percent_value"]
    margin_cash_money = 10
    margin_terminal = 20

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_list(driver, add=True)
    main_flow(driver,
              room_name=room_name,
              robot_name=robot_name,
              client_name=client_name,
              sub_filial_name=sub_filial_name,
              contract_name=contract_name)
    product_flow(driver,
                 product_name=product_name,
                 warehouse_name=warehouse_name,
                 price_type_name=price_type_name,
                 product_quantity=product_quantity,
                 next_step=False)
    order_add_tablist = OrderAddProduct(driver)
    order_add_tablist.click_nav_tablist_button(tablist_name="Акции")
    # ------------------------------------------------------------------------------------------------------------------
    action_name = "Test_action_cash_money"
    get_action_name = order_add_tablist.get_action_name(action_name)
    get_action_first_text = get_action_name.split("\n")[0]
    soft_assertions.assert_equals(get_action_first_text, action_name)

    action_name = "Test_action_terminal"
    get_action_name = order_add_tablist.get_action_name(action_name)
    get_action_first_text = get_action_name.split("\n")[0]
    soft_assertions.assert_equals(get_action_first_text, action_name)

    soft_assertions.assert_all()
    # ------------------------------------------------------------------------------------------------------------------
    order_add_tablist.click_nav_tablist_button(tablist_name="Товар")
    product_flow(driver, margin=margin)

    result = final_flow(driver, get_total_amount=True, save=False)  # 114
    total_amount_no_margin = product_quantity * product_price  # 120
    total_amount = total_amount_no_margin - (total_amount_no_margin * margin / 100)  # 114
    assertions.assert_equals(result["total_amount"], total_amount)

    payment_type_name = "Наличные деньги"
    result = final_flow(driver, payment_type_name=payment_type_name, get_total_amount=True, save=False)  # 108
    total_amount = total_amount_no_margin - (total_amount_no_margin * margin_cash_money / 100)  # 108
    assertions.assert_equals(result["total_amount"], total_amount)

    payment_type_name = "Терминал"
    final_flow(driver, payment_type_name=payment_type_name, save=False)
    get_biruni_confirm_flow(driver, button_state=True)

    result = final_flow(driver, get_total_amount=True, save=False)  # 108
    total_amount = total_amount_no_margin - (total_amount_no_margin * margin_terminal / 100)  # 96
    assertions.assert_equals(result["total_amount"], total_amount)

    step_flow(driver, save=True)

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

    soft_assertions.assert_equals(get_values["Штат"], robot_name)
    soft_assertions.assert_equals(get_values["Статус"], data["New"])
    soft_assertions.assert_equals(get_values["Клиент"], client_name)
    soft_assertions.assert_equals(get_values["Рабочая зона"], room_name)
    soft_assertions.assert_equals(get_values["Проект"], sub_filial_name)
    soft_assertions.assert_equals(get_values["Сумма заказа"], total_amount)
    soft_assertions.assert_all()

    order_list(driver)

# ======================================================================================================================
