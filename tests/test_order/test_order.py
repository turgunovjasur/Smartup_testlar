import time
from autotest.anor.mdeal.order.order_add.create_order_page import OrderAddMain
from autotest.anor.mdeal.order.order_add.final_page import OrderAddFinal
from autotest.anor.mdeal.order.order_add.goods_page import OrderAddProduct
from autotest.anor.mdeal.order.order_edit.order_edit_final import OrderEditFinal
from autotest.anor.mdeal.order.order_edit.order_edit_main import OrderEditMain
from autotest.anor.mdeal.order.order_edit.order_edit_product import OrderEditProduct
from autotest.anor.mdeal.order.order_view.order_view import OrderView
from autotest.trade.tdeal.order.order_list.orders_page import OrdersList
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
              contract=True):
    # Test data
    data = test_data()["data"]
    room_name = data["room_name"]
    robot_name = data["robot_name"]
    product_name = data["product_name"]
    product_price = data["product_price"]
    payment_type_name = data["payment_type_name"]
    client_name = client_name if client_name is not None else data["client_name"]
    contract_name = contract_name if contract_name is not None else data["contract_name"]
    product_quantity = product_quantity if product_quantity is not None else data["product_quantity"]
    return_quantity = return_quantity if return_quantity is not None else product_quantity

    login_user(driver, url='trade/tdeal/order/order_list')

    order_list = OrdersList(driver)
    assert order_list.element_visible(), 'OrdersList not open!'
    order_list.click_add_button()

    # Order Add Main
    order_add_main = OrderAddMain(driver)
    assert order_add_main.element_visible(), 'OrderAddMain not open!'
    order_add_main.click_rooms_input(room_name)
    order_add_main.click_robots_input(robot_name)
    order_add_main.click_persons_input(client_name)
    if contract is True:
        order_add_main.click_contract_input(contract_name)
    order_add_main.click_next_step_button()

    # Order Add Product
    order_add_product = OrderAddProduct(driver)
    assert order_add_product.element_visible(), 'OrderAddProduct not open!'
    order_add_product.input_name(product_name)
    order_add_product.input_quantity(product_quantity)
    order_add_product.click_next_step_button()

    # Order Add Final
    order_add_final = OrderAddFinal(driver)
    assert order_add_final.element_visible(), 'OrderAddFinal not open!'
    order_add_final.input_payment_type(payment_type_name)
    if consignment is True:
        order_add_final.input_consignment_date(current_date_add_day, consignment_amount)

    order_add_final.input_status()
    order_add_final.click_save_button()
    time.sleep(2)

    if error_massage is True:
        error_massage = order_add_final.error_massage()
        assert error_massage == data["error_massage_1"], f'Error: "error_massage_1" not visible!'
        print(f'Test error_massage: successfully!')

        order_add_final.click_error_close_button()
        order_add_final.click_prev_step_button()
        order_add_product.input_quantity(return_quantity)
        order_add_product.click_next_step_button()
        assert order_add_final.element_visible(), 'OrderAddFinal not open!'
        order_add_final.click_save_button()
        time.sleep(2)

    # Orders List
    assert order_list.element_visible(), 'OrdersList not open!'
    order_list.find_row(client_name)
    order_list.click_view_button()

    # Orders View
    order_view = OrderView(driver)
    assert order_view.element_visible(), 'OrderView not open!'

    order_id = order_view.check_order_id()
    get_quantity, get_price = order_view.check_items()

    if error_massage is True:
        assert get_quantity == return_quantity, f'Error: get_quantity: {get_quantity} != return_quantity: {return_quantity}'
        assert get_price == return_quantity * product_price, f'Error: {get_quantity} != {return_quantity} * {product_price}'

    if error_massage is False:
        assert get_quantity == product_quantity, f'Error: get_quantity: {get_quantity} != product_quantity: {product_quantity}'
        assert get_price == product_quantity * product_price, f'Error: {get_quantity} != {product_quantity} * {product_price}'

    # Check consignment
    if consignment is True:
        order_view.click_tablist_button(navbar_button='Консигнация')
        get_consignment_amount = order_view.check_consignments(current_date_add_day)
        get_consignment_amount = int(get_consignment_amount.replace(" ", ""))
        assert get_consignment_amount == consignment_amount, f'Error: {get_consignment_amount} != {consignment_amount}'

    print("-" * 50)
    print(f'Order Product Add: '
          f'\nOrder ID: {order_id} '
          f'\nClient name: {client_name} '
          f'\nProduct quantity: {get_quantity} '
          f'\nProduct price: {get_price}')
    if consignment is True:
        print(f'Consignment date: {current_date_add_day} \nConsignment amount: {consignment_amount}')
    print("-" * 50)
    order_view.click_close_button()


def test_order_add_A(driver):
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


def test_order_add_B(driver):
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


def test_order_add_C(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-C"
    contract_name = f"{data['contract_name']}-C"
    product_quantity = 20
    order_add(driver,
              client_name=client_name,
              contract_name=contract_name,
              product_quantity=product_quantity,
              contract=False)


# Edit -----------------------------------------------------------------------------------------------------------------

def order_edit(driver, client_name=None, product_quantity_edit=None):
    # Test data
    data = test_data()["data"]
    product_price = data["product_price"]
    product_quantity = data["product_quantity"]
    client_name = client_name if client_name is not None else data["client_name"]
    product_quantity_edit = product_quantity_edit if product_quantity_edit is not None else (product_quantity - 1)

    login_user(driver, url='trade/tdeal/order/order_list')

    order_list = OrdersList(driver)
    assert order_list.element_visible(), 'OrdersList not open!'
    order_list.find_row(client_name)
    order_list.click_edit_button()

    # Order Edit Main
    order_edit_main = OrderEditMain(driver)
    assert order_edit_main.element_visible(), 'OrderEditMain not open!'
    order_edit_main.click_next_step_button()

    # Order Edit Product
    order_edit_product = OrderEditProduct(driver)
    assert order_edit_product.element_visible(), 'OrderEditProduct not open!'
    order_edit_product.input_quantity(product_quantity_edit)
    order_edit_product.click_next_step_button()

    # Order Edit Final
    order_edit_final = OrderEditFinal(driver)
    assert order_edit_final.element_visible(), 'OrderEditFinal not open!'
    order_edit_final.click_save_button()
    time.sleep(2)

    # Orders List
    assert order_list.element_visible(), 'OrdersList not open!'
    order_list.find_row(client_name)
    order_list.click_view_button()

    # Orders View
    order_view = OrderView(driver)
    assert order_view.element_visible(), 'OrderView not open!'

    order_id = order_view.check_order_id()
    get_quantity, get_price = order_view.check_items()
    assert get_quantity == product_quantity_edit, f'Error: get_quantity: {get_quantity} != product_quantity_edit: {product_quantity_edit}'
    assert get_price == product_quantity_edit * product_price, f'Error: {get_quantity} != {product_quantity_edit} * {product_price}'
    print("-" * 50)
    print(
        f'Order Product Edit: \nOrder ID: {order_id} \nClient name: {client_name} \nProduct quantity: {get_quantity} \nProduct price: {get_price}')
    print("-" * 50)
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
    assert order_list.element_visible(), 'OrdersList not open!'
    order_list.find_row(client_name)
    order_list.click_view_button()

    assert order_view.element_visible(), 'OrderView not open!'
    order_id = order_view.check_order_id()
    text = order_view.check_status()
    assert text == data["Draft"], base_page.take_screenshot("status_name_Draft") or f'{text} != {data["Draft"]}'
    draft_quantity, draft_price = order_view.check_items()
    order_view.click_close_button()

    # ------------------------------------------------------------------------------------------------------------------
    if status:
        # New
        assert order_list.element_visible(), 'OrdersList not open!'
        order_list.click_change_status_button(data["New"])
        order_list.find_row(client_name)
        order_list.click_view_button()

        assert order_view.element_visible(), 'OrderView not open!'
        text = order_view.check_status()
        assert text == data["New"], base_page.take_screenshot("status_name_New") or f'{text} != {data["New"]}'
        new_quantity, new_price = order_view.check_items()
        assert draft_quantity == new_quantity, f'Error: draft_quantity: {draft_quantity} != new_quantity: {new_quantity}'
        assert draft_price == new_price, f'Error: draft_price: {draft_price} != new_price: {new_price}'
        order_view.click_close_button()
        # ------------------------------------------------------------------------------------------------------------------

        # Processing
        assert order_list.element_visible(), 'OrdersList not open!'
        order_list.click_change_status_button(data["Processing"])
        order_list.find_row(client_name)
        order_list.click_view_button()

        assert order_view.element_visible(), 'OrderView not open!'
        text = order_view.check_status()
        assert text == data["Processing"], base_page.take_screenshot(
            "status_name_Processing") or f'{text} != {data["Processing"]}'
        processing_quantity, processing_price = order_view.check_items()
        assert draft_quantity == processing_quantity, f'Error: draft_quantity: {draft_quantity} != processing_quantity: {processing_quantity}'
        assert draft_price == processing_price, f'Error: draft_price: {draft_price} != processing_price: {processing_price}'
        order_view.click_close_button()
        # ------------------------------------------------------------------------------------------------------------------

        # Pending
        assert order_list.element_visible(), 'OrdersList not open!'
        order_list.click_change_status_button(data["Pending"])
        order_list.find_row(client_name)
        order_list.click_view_button()

        assert order_view.element_visible(), 'OrderView not open!'
        text = order_view.check_status()
        assert text == data["Pending"], base_page.take_screenshot(
            "status_name_Pending") or f'{text} != {data["Pending"]}'
        pending_quantity, pending_price = order_view.check_items()
        assert draft_quantity == pending_quantity, f'Error: draft_quantity: {draft_quantity} != pending_quantity: {pending_quantity}'
        assert draft_price == pending_price, f'Error: draft_price: {draft_price} != pending_price: {pending_price}'
        order_view.click_close_button()
        # ------------------------------------------------------------------------------------------------------------------

        # Shipped
        assert order_list.element_visible(), 'OrdersList not open!'
        order_list.click_change_status_button(data["Shipped"])
        order_list.find_row(client_name)
        order_list.click_view_button()

        assert order_view.element_visible(), 'OrderView not open!'
        text = order_view.check_status()
        assert text == data["Shipped"], base_page.take_screenshot(
            "status_name_Shipped") or f'{text} != {data["Shipped"]}'
        shipped_quantity, shipped_price = order_view.check_items()
        assert draft_quantity == shipped_quantity, f'Error: draft_quantity: {draft_quantity} != shipped_quantity: {shipped_quantity}'
        assert draft_price == shipped_price, f'Error: draft_price: {draft_price} != shipped_price: {shipped_price}'
        order_view.click_close_button()
        # ------------------------------------------------------------------------------------------------------------------

        # Delivered
        assert order_list.element_visible(), 'OrdersList not open!'
        order_list.click_change_status_button(data["Delivered"])
        order_list.find_row(client_name)
        order_list.click_view_button()

        assert order_view.element_visible(), 'OrderView not open!'
        text = order_view.check_status()
        assert text == data["Delivered"], base_page.take_screenshot(
            "status_name_Delivered") or f'{text} != {data["Delivered"]}'
        delivered_quantity, delivered_price = order_view.check_items()
        assert draft_quantity == delivered_quantity, f'Error: draft_quantity: {draft_quantity} != delivered_quantity: {delivered_quantity}'
        assert draft_price == delivered_price, f'Error: draft_price: {draft_price} != delivered_price: {delivered_price}'
        order_view.click_close_button()
        print("-" * 50)
        print(f'Order change status: '
              f'\nOrder ID: {order_id} '
              f'\n"{data["Draft"]}" --> '
              f'\n"{data["New"]}" --> '
              f'\n"{data["Processing"]}" --> '
              f'\n"{data["Pending"]}" --> '
              f'\n"{data["Shipped"]}" --> '
              f'\n"{data["Delivered"]}" --> '
              f'\n"{data["Archive"]}"')
        print("-" * 50)

    # ------------------------------------------------------------------------------------------------------------------
    # Archive
    assert order_list.element_visible(), 'OrdersList not open!'
    order_list.click_change_status_button(data["Archive"])

    if status is False:
        print("-" * 50)
        print(f'Order change status: '
              f'\nOrder ID: {order_id} '
              f'\n"{data["Draft"]}" --> '
              f'\n"{data["Archive"]}"')
        print("-" * 50)


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
    base_page.logger.info("Test run(▶️): order_copy")
    base_page.logger.info(f"Test data: client_name='{client_name}', client_name_copy_A='{client_name_copy_A}'")
    base_page.logger.info(f"Test data: client_name='{client_name}', client_name_copy_B='{client_name_copy_B}'")

    try:
        login_user(driver, url='trade/tdeal/order/order_list')
        base_page.logger.info("Successful access to the system.")

        # List
        order_list = OrdersList(driver)
        assert order_list.element_visible() \
               or base_page.logger.error("order_list not open!") \
               or base_page.take_screenshot("order_list_error")
        order_list.find_row(client_name)
        order_list.click_copy_button()
        base_page.logger.info("OrdersList: click_copy_button pressed.")

        # Copy
        assert order_list.element_visible_copy_title() \
               or base_page.logger.error("order_copy_title not open!") \
               or base_page.take_screenshot("order_copy_title_error")
        order_list.input_persons(client_name_copy_A, client_name_copy_B)
        base_page.logger.info(f"OrdersList: client_name_copy_A inputted: '{client_name_copy_A}'")
        base_page.logger.info(f"OrdersList: client_name_copy_B inputted: '{client_name_copy_B}'")

        order_list.click_copy_save_button()
        base_page.logger.info("OrdersList: click_copy_save_button pressed.")

        # List
        assert order_list.element_visible() \
               or base_page.logger.error("order_list not open!") \
               or base_page.take_screenshot("order_list_error")
        order_list.find_row(client_name_copy_A)
        order_list.click_view_button()
        base_page.logger.info("OrdersList: click_view_button pressed.")

        # View client_A
        order_view = OrderView(driver)
        assert order_view.element_visible() \
               or base_page.logger.error("order_view client_A not open!") \
               or base_page.take_screenshot("order_view_client_A_error")
        get_client_name = order_view.check_client_name()
        assert get_client_name == client_name_copy_A \
               or base_page.logger.error(f"{get_client_name} != {client_name_copy_A}") \
               or base_page.take_screenshot("check_client_A_error")
        order_view.click_close_button()
        base_page.logger.info("OrdersList: click_close_button pressed.")

        # List
        order_list.click_reload_button()
        base_page.logger.info("OrdersList: click_reload_button pressed.")
        assert order_list.element_visible() \
               or base_page.logger.error("order_list not open!") \
               or base_page.take_screenshot("order_list_error")
        order_list.find_row(client_name_copy_B)
        order_list.click_view_button()
        base_page.logger.info("OrdersList: click_view_button pressed.")

        # View client_B
        assert order_view.element_visible() \
               or base_page.logger.error("order_view client_B not open!") \
               or base_page.take_screenshot("order_view_client_B_error")
        get_client_name = order_view.check_client_name()
        assert get_client_name == client_name_copy_B \
               or base_page.logger.error(f"{get_client_name} != {client_name_copy_B}") \
               or base_page.take_screenshot("check_client_B_error")
        order_view.click_close_button()
        base_page.logger.info("OrdersList: click_close_button pressed.")

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

