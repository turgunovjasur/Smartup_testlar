import time
from autotest.anor.mdeal.order.order_add.create_order_page import OrderAddMain
from autotest.anor.mdeal.order.order_add.final_page import OrderAddFinal
from autotest.anor.mdeal.order.order_add.goods_page import OrderAddProduct
from autotest.anor.mdeal.order.order_edit.order_edit_final import OrderEditFinal
from autotest.anor.mdeal.order.order_edit.order_edit_main import OrderEditMain
from autotest.anor.mdeal.order.order_edit.order_edit_product import OrderEditProduct
from autotest.anor.mdeal.order.order_view.order_view import OrderView
from autotest.trade.tdeal.order.order_list.orders_page import OrdersList
from autotest.trade.tdeal.order.return_order.return_order import ReturnOrder
from tests.test_base.test_base import test_data, login_user
from autotest.core.md.base_page import BasePage
from utils.driver_setup import driver


# Order Add ------------------------------------------------------------------------------------------------------------

def order_add(driver,
              client_name=None,
              contract_name=None,
              product_quantity=None,
              error_massage=False,
              return_quantity=None,
              consignment=None,
              consignment_amount=None,
              current_date_add_day=None,
              contract=True,
              price_type_name=None,
              product_price_USA=None,
              margin=False):

    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): order_add")

    # Test data
    data = test_data()["data"]
    room_name = data["room_name"]
    robot_name = data["robot_name"]
    product_name = data["product_name"]
    warehouse_name = data["warehouse_name"]
    percent_value = data["percent_value"]
    price_type_name = price_type_name if price_type_name is not None else data["price_type_name_UZB"]
    product_price = product_price_USA if product_price_USA is not None else data["product_price"]
    payment_type_name = data["payment_type_name"]
    client_name = client_name if client_name is not None else data["client_name"]
    contract_name = contract_name if contract_name is not None else data["contract_name"]
    product_quantity = product_quantity if product_quantity is not None else data["product_quantity"]
    return_quantity = return_quantity if return_quantity is not None else product_quantity

    # Login
    login_user(driver, url='trade/tdeal/order/order_list')

    # Orders List
    order_list = OrdersList(driver)
    base_page = BasePage(driver)
    assert order_list.element_visible(), base_page.logger.error('OrdersList not open!')
    order_list.click_add_button()

    # Order Add Main
    order_add_main = OrderAddMain(driver)
    assert order_add_main.element_visible(), base_page.logger.error('OrderAddMain not open!')
    order_add_main.click_rooms_input(room_name)
    order_add_main.click_robots_input(robot_name)
    order_add_main.click_persons_input(client_name)

    if contract is True:
        order_add_main.click_contract_input(contract_name)

    order_add_main.click_next_step_button()

    # Order Add Product
    order_add_product = OrderAddProduct(driver)
    assert order_add_product.element_visible(), base_page.logger.error('OrderAddProduct not open!')
    order_add_product.input_name_product(product_name, warehouse_name, price_type_name)
    order_add_product.input_quantity(product_quantity)

    if margin is True:
        order_add_product.click_percent_value_button(percent_value)

    order_add_product.click_next_step_button()

    # Order Add Final
    order_add_final = OrderAddFinal(driver)
    assert order_add_final.element_visible(), base_page.logger.error('OrderAddFinal not open!')
    order_add_final.input_payment_type(payment_type_name)

    total_amount_margin = order_add_final.check_total_amount()  # 228
    total_amount = product_quantity * product_price  # 240
    total_margin = total_amount * percent_value / 100  # 12
    if margin is True:
        assert total_amount == total_amount_margin + total_margin, \
            base_page.logger.error(f"{total_amount} != {total_amount_margin} * {total_margin}")

    if consignment is True:
        order_add_final.input_consignment_date(current_date_add_day, consignment_amount)

    order_add_final.input_status()
    order_add_final.click_save_button()
    time.sleep(2)

    if error_massage is True:
        error_massage = order_add_final.error_massage()
        assert error_massage == data["error_massage_1"], \
            base_page.logger.error(f'Error: "error_massage_1" not visible!')
        base_page.logger.info(f'Test error_massage: successfully!')

        order_add_final.click_error_close_button()
        order_add_final.click_prev_step_button()
        order_add_product.input_quantity(return_quantity)
        order_add_product.click_next_step_button()
        assert order_add_final.element_visible(), base_page.logger.error('OrderAddFinal not open!')
        order_add_final.click_save_button()
        time.sleep(2)

    # Orders List
    assert order_list.element_visible(), base_page.logger.error('OrdersList not open!')
    order_list.find_row(client_name)
    order_list.click_view_button()

    # Orders View
    order_view = OrderView(driver)
    assert order_view.element_visible(), base_page.logger.error('OrderView not open!')

    order_id = order_view.check_order_id()
    get_quantity, get_price, total_sum = order_view.check_items()

    if error_massage is True:
        assert get_quantity == return_quantity, \
            base_page.logger.error(f'Error: get_quantity: {get_quantity} != return_quantity: {return_quantity}')
        assert get_price == return_quantity * product_price, \
            base_page.logger.error(f'Error: get_quantity {get_quantity} != {return_quantity} * {product_price}')

    if error_massage is False:
        assert get_quantity == product_quantity, \
               base_page.logger.error(f'Error: get_quantity: {get_quantity} != product_quantity: {product_quantity}')
        assert get_price == product_quantity * product_price, \
               base_page.logger.error(f'Error: get_price: {get_price} != {product_quantity} * {product_price}')

    if margin is True:
        assert get_price == product_quantity * product_price_USA, \
               base_page.logger.error(f'Error: get_price: {get_price} != {product_quantity} * {product_price_USA}')
        assert total_sum == get_price - total_margin, \
               base_page.logger.error(f'Error: total_sum: {total_sum} != {get_price} - {total_margin}')

    # Check consignment
    if consignment is True:
        order_view.click_tablist_button(navbar_button='Консигнация')
        get_consignment_amount = order_view.check_consignments(current_date_add_day)
        get_consignment_amount = int(get_consignment_amount.replace(" ", ""))
        assert get_consignment_amount == consignment_amount, \
            base_page.logger.error(f'Error: {get_consignment_amount} != {consignment_amount}')

    order_view.click_close_button()


def test_order_add_with_consignment(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-A"
    contract_name = f"{data['contract_name']}-A"
    product_quantity = 15
    current_date_add_day = 30
    consignment_amount = product_quantity * data["product_price"]
    order_add(driver,
              client_name=client_name,
              contract_name=contract_name,
              product_quantity=product_quantity,
              consignment=True,
              consignment_amount=consignment_amount,
              current_date_add_day=current_date_add_day)


def test_order_add_client_B_check_contract(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-B"
    contract_name = f"{data['contract_name']}-B"
    product_quantity = 101
    return_quantity = 15
    order_add(driver,
              client_name=client_name,
              contract_name=contract_name,
              product_quantity=product_quantity,
              return_quantity=return_quantity,
              error_massage=True)


def test_order_add_price_type_USA(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-C"
    price_type_name = data['price_type_name_USA']
    product_price_USA = data['product_price_USA']
    product_quantity = 20
    order_add(driver,
              client_name=client_name,
              contract=False,
              price_type_name=price_type_name,
              product_price_USA=product_price_USA,
              product_quantity=product_quantity,
              margin=True,)


# Edit -----------------------------------------------------------------------------------------------------------------

def order_edit(driver, client_name=None, product_quantity_edit=None):
    # Test data
    base_page = BasePage(driver)
    data = test_data()["data"]
    product_price = data["product_price"]
    product_quantity = data["product_quantity"]
    client_name = client_name if client_name is not None else data["client_name"]
    product_quantity_edit = product_quantity_edit if product_quantity_edit is not None else (product_quantity - 1)

    login_user(driver, url='trade/tdeal/order/order_list')

    order_list = OrdersList(driver)
    assert order_list.element_visible(), base_page.logger.error('OrdersList not open!')
    order_list.find_row(client_name)
    order_list.click_edit_button()

    # Order Edit Main
    order_edit_main = OrderEditMain(driver)
    assert order_edit_main.element_visible(), base_page.logger.error('OrderEditMain not open!')
    order_edit_main.click_next_step_button()

    # Order Edit Product
    order_edit_product = OrderEditProduct(driver)
    assert order_edit_product.element_visible(), base_page.logger.error('OrderEditProduct not open!')
    order_edit_product.input_quantity(product_quantity_edit)
    order_edit_product.click_next_step_button()

    # Order Edit Final
    order_edit_final = OrderEditFinal(driver)
    try:
        error_massage = order_edit_final.error_massage()
        assert error_massage == data["error_massage_2"], \
            base_page.logger.error(f'❌Error: "error_massage_2" not visible!')
        base_page.logger.info(f"✅Error message found: successfully!")
        order_edit_final.click_error_button()
    except Exception:
        base_page.logger.error(f"❌Error message not found.")
        base_page.take_screenshot("error_message_not_found")

    assert order_edit_final.element_visible(), base_page.logger.error('OrderEditFinal not open!')
    order_edit_final.click_save_button()
    time.sleep(2)

    # Orders List
    assert order_list.element_visible(), base_page.logger.error('OrdersList not open!')
    order_list.find_row(client_name)
    order_list.click_view_button()

    # Orders View
    order_view = OrderView(driver)
    assert order_view.element_visible(), base_page.logger.error('OrderView not open!')

    order_id = order_view.check_order_id()
    get_quantity, get_price = order_view.check_items()
    assert get_quantity == product_quantity_edit, \
        base_page.logger.error(f'Error: get_quantity: {get_quantity} != product_quantity_edit: {product_quantity_edit}')
    assert get_price == product_quantity_edit * product_price, \
        base_page.logger.error(f'Error: {get_quantity} != {product_quantity_edit} * {product_price}')
    base_page.logger.info(f'order_id: {order_id}')
    order_view.click_tablist_button(navbar_button='Консигнация')
    try:
        order_view.check_row_consignment()
    except Exception:
        base_page.logger.error(f"❌Error consignment yes found.")
        base_page.take_screenshot("error_message_yes_found")
    order_view.click_close_button()


def test_order_edit_A(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-A"
    product_quantity_edit = 10
    order_edit(driver,
               client_name=client_name,
               product_quantity_edit=product_quantity_edit)


# Status ---------------------------------------------------------------------------------------------------------------

def order_change_status(driver, client_name=None, status=True):
    # Test data
    data = test_data()["data"]
    client_name = client_name if client_name is not None else data["client_name"]

    login_user(driver, url='trade/tdeal/order/order_list')

    order_list = OrdersList(driver)
    order_view = OrderView(driver)
    base_page = BasePage(driver)

    # Draft
    assert order_list.element_visible(), base_page.logger.error('OrdersList not open!')
    order_list.find_row(client_name)
    order_list.click_view_button()

    assert order_view.element_visible(), base_page.logger.error('OrderView not open!')
    order_id = order_view.check_order_id()
    text = order_view.check_status()
    assert text == data["Draft"], base_page.logger.error(f'{text} != {data["Draft"]}')
    draft_quantity, draft_price = order_view.check_items()
    order_view.click_close_button()

    # ------------------------------------------------------------------------------------------------------------------
    if status:
        # New
        assert order_list.element_visible(), base_page.logger.error('OrdersList not open!')
        order_list.click_change_status_button(data["New"])
        order_list.find_row(client_name)
        order_list.click_view_button()

        assert order_view.element_visible(), base_page.logger.error('OrderView not open!')
        text = order_view.check_status()
        assert text == data["New"], base_page.logger.error(f'{text} != {data["New"]}')
        new_quantity, new_price = order_view.check_items()
        assert draft_quantity == new_quantity, \
            base_page.logger.error(f'Error: draft_quantity: {draft_quantity} != new_quantity: {new_quantity}')
        assert draft_price == new_price, base_page.logger.error(f'Error: draft_price: {draft_price} != new_price: {new_price}')
        order_view.click_close_button()
        # ------------------------------------------------------------------------------------------------------------------

        # Processing
        assert order_list.element_visible(), base_page.logger.error('OrdersList not open!')
        order_list.click_change_status_button(data["Processing"])
        order_list.find_row(client_name)
        order_list.click_view_button()

        assert order_view.element_visible(), base_page.logger.error('OrderView not open!')
        text = order_view.check_status()
        assert text == data["Processing"], base_page.logger.error(f'{text} != {data["Processing"]}')
        processing_quantity, processing_price = order_view.check_items()
        assert draft_quantity == processing_quantity, \
            base_page.logger.error(f'Error: draft_quantity: {draft_quantity} != processing_quantity: {processing_quantity}')
        assert draft_price == processing_price, \
            base_page.logger.error(f'Error: draft_price: {draft_price} != processing_price: {processing_price}')
        order_view.click_close_button()
        # ------------------------------------------------------------------------------------------------------------------

        # Pending
        assert order_list.element_visible(), base_page.logger.error('OrdersList not open!')
        order_list.click_change_status_button(data["Pending"])
        order_list.find_row(client_name)
        order_list.click_view_button()

        assert order_view.element_visible(), base_page.logger.error('OrderView not open!')
        text = order_view.check_status()
        assert text == data["Pending"], base_page.logger.error(f'{text} != {data["Pending"]}')
        pending_quantity, pending_price = order_view.check_items()
        assert draft_quantity == pending_quantity, \
            base_page.logger.error(f'Error: draft_quantity: {draft_quantity} != pending_quantity: {pending_quantity}')
        assert draft_price == pending_price, \
            base_page.logger.error(f'Error: draft_price: {draft_price} != pending_price: {pending_price}')
        order_view.click_close_button()
        # ------------------------------------------------------------------------------------------------------------------

        # Shipped
        assert order_list.element_visible(), base_page.logger.error('OrdersList not open!')
        order_list.click_change_status_button(data["Shipped"])
        order_list.find_row(client_name)
        order_list.click_view_button()

        assert order_view.element_visible(), base_page.logger.error('OrderView not open!')
        text = order_view.check_status()
        assert text == data["Shipped"], base_page.logger.error(f'{text} != {data["Shipped"]}')
        shipped_quantity, shipped_price = order_view.check_items()
        assert draft_quantity == shipped_quantity, \
            base_page.logger.error(f'Error: draft_quantity: {draft_quantity} != shipped_quantity: {shipped_quantity}')
        assert draft_price == shipped_price, \
            base_page.logger.error(f'Error: draft_price: {draft_price} != shipped_price: {shipped_price}')
        order_view.click_close_button()
        # ------------------------------------------------------------------------------------------------------------------

        # Delivered
        assert order_list.element_visible(), base_page.logger.error('OrdersList not open!')
        order_list.click_change_status_button(data["Delivered"])
        order_list.find_row(client_name)
        order_list.click_view_button()

        assert order_view.element_visible(), base_page.logger.error('OrderView not open!')
        text = order_view.check_status()
        assert text == data["Delivered"], base_page.logger.error(f'{text} != {data["Delivered"]}')
        delivered_quantity, delivered_price = order_view.check_items()
        assert draft_quantity == delivered_quantity, \
            base_page.logger.error(f'Error: draft_quantity: {draft_quantity} != delivered_quantity: {delivered_quantity}')
        assert draft_price == delivered_price, \
            base_page.logger.error(f'Error: draft_price: {draft_price} != delivered_price: {delivered_price}')
        order_view.click_close_button()

    # ------------------------------------------------------------------------------------------------------------------
    # Archive
    assert order_list.element_visible(), base_page.logger.error('OrdersList not open!')
    order_list.click_change_status_button(data["Archive"])


def test_order_change_status_A(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-A"
    order_change_status(driver,
                        client_name=client_name)


def test_order_change_status_B(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-B"
    order_change_status(driver,
                        client_name=client_name,
                        status=False)


def test_order_change_status_C(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-C"
    order_change_status(driver,
                        client_name=client_name,
                        status=False)


# Copy -----------------------------------------------------------------------------------------------------------------

def order_copy(driver, client_name=None, client_name_copy_A=None, client_name_copy_B=None):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("▶️Test run(): order_copy")
    base_page.logger.info(f"Test data: client_name='{client_name}', client_name_copy_A='{client_name_copy_A}'")
    base_page.logger.info(f"Test data: client_name='{client_name}', client_name_copy_B='{client_name_copy_B}'")

    try:
        login_user(driver, url='trade/tdeal/order/order_list')

        # List
        order_list = OrdersList(driver)
        assert order_list.element_visible(), base_page.logger.error("order_list not open!")
        order_list.find_row(client_name)
        order_list.click_copy_button()

        # Copy
        assert order_list.element_visible_copy_title(), base_page.logger.error("order_copy_title not open!")
        order_list.input_persons(client_name_copy_A, client_name_copy_B)
        order_list.click_copy_save_button()

        # List
        assert order_list.element_visible(), base_page.logger.error("order_list not open!")
        order_list.find_row(client_name_copy_A)
        order_list.click_view_button()

        # View client_A
        order_view = OrderView(driver)
        assert order_view.element_visible(), base_page.logger.error("order_view client_A not open!")
        get_client_name = order_view.check_client_name()
        assert get_client_name == client_name_copy_A, \
            base_page.logger.error(f"{get_client_name} != {client_name_copy_A}")
        order_view.click_close_button()

        # List
        order_list.click_reload_button()
        assert order_list.element_visible(), base_page.logger.error("order_list not open!")
        order_list.find_row(client_name_copy_B)
        order_list.click_view_button()

        # View client_B
        assert order_view.element_visible(), base_page.logger.error("order_view client_B not open!")
        get_client_name = order_view.check_client_name()
        assert get_client_name == client_name_copy_B, \
            base_page.logger.error(f"{get_client_name} != {client_name_copy_B}")
        order_view.click_close_button()

    except Exception as e:
        base_page.logger.error(f"❌Error message(): {e}")
        base_page.take_screenshot("order_copy_error")
        raise


def test_order_copy_C_for_A_B(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-C"
    client_name_copy_A = f"{data['client_name']}-A"
    client_name_copy_B = f"{data['client_name']}-B"
    order_copy(driver,
               client_name=client_name,
               client_name_copy_A=client_name_copy_A,
               client_name_copy_B=client_name_copy_B)


# Return ---------------------------------------------------------------------------------------------------------------

def order_return(driver, client_name=None):
    # Log
    data = test_data()["data"]

    base_page = BasePage(driver)
    base_page.logger.info("▶️Test run(): order_return")
    base_page.logger.info(f"Test data: client_name='{client_name}'")

    try:
        login_user(driver, url='trade/tdeal/order/order_list')

        # List
        order_list = OrdersList(driver)
        assert order_list.element_visible(), base_page.logger.error("order_list not open!")
        order_list.find_row(client_name)
        order_list.click_view_button()

        # View
        order_view = OrderView(driver)
        assert order_view.element_visible(), base_page.logger.error('OrderView not open!')
        get_order_id = order_view.check_order_id()
        get_status = order_view.check_status()
        assert get_status == data["Draft"], base_page.logger.error(f'{get_status} != {data["Draft"]}')
        get_quantity, get_price = order_view.check_items()
        base_page.logger.info(f"OrderView: success checked: order_id: {get_order_id}, order_status: {get_status}, order_price: {get_price}")
        order_view.click_close_button()

        # List
        assert order_list.element_visible(), base_page.logger.error("order_list not open!")
        order_list.click_change_status_button(data["Delivered"])
        order_list.find_row(client_name)
        order_list.click_return_button()

        # Return Order
        return_order = ReturnOrder(driver)
        assert return_order.element_visible(), base_page.logger.error("return_order not open!")
        get_client_name = return_order.check_client_name()
        assert get_client_name == client_name, base_page.logger.error(f"{get_client_name} != {client_name}")
        return_order.click_return_all_button()
        get_total_price = return_order.check_total_price()
        assert get_total_price == '0', base_page.logger.error(f"{get_total_price} != {'0'}")
        return_order.click_save_button()

        # List
        assert order_list.element_visible(), base_page.logger.error("order_list not open!")
        order_list.find_row(client_name)
        order_list.click_view_button()

        # Order View
        assert order_view.element_visible(), base_page.logger.error('OrderView not open!')
        get_order_id_last = order_view.check_order_id()
        assert get_order_id == get_order_id_last, base_page.logger.error(f'{get_order_id} != {get_order_id_last}')
        get_status_last = order_view.check_status()
        assert get_status_last == data["Delivered"], \
            base_page.logger.error(f'{get_status_last} != {data["Delivered"]}')
        get_quantity, get_price = order_view.check_items()
        assert get_price == 0, base_page.logger.error(f"Error: {get_price} != {0}")
        base_page.logger.info(
            f"OrderView: success checked: order_id: {get_order_id_last}, order_status: {get_status_last}, order_price: {get_price}")
        base_page.logger.info(f"✅Test end(): order_return successfully!")

    except Exception as e:
        base_page.logger.error(f"❌Error message(): {e}")
        base_page.take_screenshot("order_return_error")
        raise


def test_order_return(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-A"
    order_return(driver, client_name=client_name)


def order_list(driver, client_name=None):
    # Log
    data = test_data()["data"]

    base_page = BasePage(driver)
    base_page.logger.info("▶️Test run(): order_list")
    base_page.logger.info(f"Test data: client_name='{client_name}'")

    try:
        login_user(driver, url='trade/tdeal/order/order_list')

        order_list = OrdersList(driver)
        order_view = OrderView(driver)

        # Order_A
        assert order_list.element_visible(), base_page.logger.error("order_list not open!")
        order_list.click_reload_button()
        order_list.find_row(f"{data['client_name']}-A")
        order_list.click_view_button()
        assert order_view.element_visible(), base_page.logger.error("order_view not open!")
        get_order_id_A = order_view.check_order_id()
        get_quantity_A, get_price_A = order_view.check_items()
        order_view.click_close_button()

        # Order_B
        assert order_list.element_visible(), base_page.logger.error("order_list not open!")
        order_list.click_reload_button()
        order_list.find_row(f"{data['client_name']}-B")
        order_list.click_view_button()
        assert order_view.element_visible(), base_page.logger.error("order_view not open!")
        get_order_id_B = order_view.check_order_id()
        get_quantity_B, get_price_B = order_view.check_items()
        order_view.click_close_button()

        # Order_C
        assert order_list.element_visible(), base_page.logger.error("order_list not open!")
        order_list.click_reload_button()
        order_list.find_row(f"{data['client_name']}-C")
        order_list.click_view_button()
        assert order_view.element_visible(), base_page.logger.error("order_view not open!")
        get_order_id_C = order_view.check_order_id()
        get_quantity_C, get_price_C = order_view.check_items()
        order_view.click_close_button()

        print(f"get_order_id_A: {get_order_id_A}")
        print(f"get_quantity_A: {get_quantity_A}")
        print(f"get_price_A: {get_price_A}")

        print(f"get_order_id_B: {get_order_id_B}")
        print(f"get_quantity_B: {get_quantity_B}")
        print(f"get_price_B: {get_price_B}")

        print(f"get_order_id_C: {get_order_id_C}")
        print(f"get_quantity_C: {get_quantity_C}")
        print(f"get_price_C: {get_price_C}")
        time.sleep(2)

        base_page.logger.info(f"✅Test end(): order_return successfully!")

    except Exception as e:
        base_page.logger.error(f"❌Error message(): {e}")
        base_page.take_screenshot("order_list_error")
        raise


def test_order_list(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-A"
    order_list(driver, client_name=client_name)
