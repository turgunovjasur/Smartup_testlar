import time
from autotest.anor.mdeal.order.order_add.create_order_page import OrderAddMain
from autotest.anor.mdeal.order.order_add.final_page import OrderAddFinal
from autotest.anor.mdeal.order.order_add.goods_page import OrderAddProduct
from autotest.anor.mdeal.order.order_edit.order_edit_final import OrderEditFinal
from autotest.anor.mdeal.order.order_edit.order_edit_main import OrderEditMain
from autotest.anor.mdeal.order.order_edit.order_edit_product import OrderEditProduct
from autotest.anor.mdeal.order.order_view.order_view import OrderView
from autotest.core.md.base_page import BasePage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.tdeal.order.order_list.orders_page import OrdersList
from tests.test_base.test_base import test_data, login, dashboard, open_new_window, get_driver
from utils.driver_setup import driver


# Add ------------------------------------------------------------------------------------------------------------------

def order_add(driver, client_name=None, contract_name=None, product_quantity=None, error_massage=False, return_quantity=None):
    # Test data
    data = test_data()["data"]

    email_user = data["email_user"]
    password_user = data["password_user"]
    filial_name = data["filial_name"]
    room_name = data["room_name"]
    robot_name = data["robot_name"]
    client_name = client_name if client_name is not None else data["client_name"]
    contract_name = contract_name if contract_name is not None else data["contract_name"]
    product_name = data["product_name"]
    product_quantity = product_quantity if product_quantity is not None else data["product_quantity"]
    return_quantity = return_quantity if return_quantity is not None else product_quantity
    product_price = data["product_price"]
    payment_type_name = data["payment_type_name"]

    # Login
    login(driver, email_user, password_user)

    # Dashboard
    dashboard(driver)
    dashboard_page = DashboardPage(driver)
    dashboard_page.find_filial(filial_name)

    # Open Orders List
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'trade/tdeal/order/order_list')
    order_list = OrdersList(driver)
    assert order_list.element_visible(), 'OrdersList not open!'
    order_list.click_add_button()

    # Order Add Main
    order_add_main = OrderAddMain(driver)
    assert order_add_main.element_visible(), 'OrderAddMain not open!'
    order_add_main.click_rooms_input(room_name)
    order_add_main.click_robots_input(robot_name)
    order_add_main.click_persons_input(client_name)
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

    print("-" * 50)
    print(f'Order Product Add: \nOrder ID: {order_id} \nProduct quantity: {get_quantity} \nProduct price: {get_price}')
    print("-" * 50)
    order_view.click_close_button()


def test_order_add_A(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-A"
    contract_name = f"{data['contract_name']}-A"
    product_quantity = 7
    order_add(driver,
              client_name=client_name,
              contract_name=contract_name,
              product_quantity=product_quantity)


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
    product_quantity = 10
    order_add(driver,
              client_name=client_name,
              contract_name=contract_name,
              product_quantity=product_quantity)


# Edit -----------------------------------------------------------------------------------------------------------------

def order_edit(driver, client_name=None, product_quantity_edit=None):
    # Test data
    data = test_data()["data"]

    email_user = data["email_user"]
    password_user = data["password_user"]
    filial_name = data["filial_name"]
    client_name = client_name if client_name is not None else data["client_name"]
    product_quantity = data["product_quantity"]
    product_quantity_edit = product_quantity_edit if product_quantity_edit is not None else (product_quantity - 1)
    product_price = data["product_price"]

    # Login
    login(driver, email_user, password_user)

    # Dashboard
    dashboard(driver)
    dashboard_page = DashboardPage(driver)
    dashboard_page.find_filial(filial_name)

    # Open Orders List
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'trade/tdeal/order/order_list')
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
    print(f'Order Product Edit: \nOrder ID: {order_id} \nProduct quantity: {get_quantity} \nProduct price: {get_price}')
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

    email_user = data["email_user"]
    password_user = data["password_user"]
    filial_name = data["filial_name"]
    client_name = client_name if client_name is not None else data["client_name"]

    # Login
    login(driver, email_user, password_user)

    # Dashboard
    dashboard(driver)
    dashboard_page = DashboardPage(driver)
    dashboard_page.find_filial(filial_name)

    # Open Orders List
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'trade/tdeal/order/order_list')
    order_list = OrdersList(driver)
    order_view = OrderView(driver)

    if status:
        # Draft
        assert order_list.element_visible(), 'OrdersList not open!'
        order_list.find_row(client_name)
        order_list.click_view_button()

        assert order_view.element_visible(), 'OrderView not open!'
        text = order_view.check_status()
        assert text == data["Draft"], f'{text} != {data["Draft"]}'
        draft_quantity, draft_price = order_view.check_items()
        order_view.click_close_button()
        # ------------------------------------------------------------------------------------------------------------------

        # New
        assert order_list.element_visible(), 'OrdersList not open!'
        order_list.click_change_status_button(data["New"])
        order_list.find_row(client_name)
        order_list.click_view_button()

        assert order_view.element_visible(), 'OrderView not open!'
        text = order_view.check_status()
        assert text == data["New"], f'{text} != {data["New"]}'
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
        assert text == data["Processing"], f'{text} != {data["Processing"]}'
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
        assert text == data["Pending"], f'{text} != {data["Pending"]}'
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
        assert text == data["Shipped"], f'{text} != {data["Shipped"]}'
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
        assert text == data["Delivered"], f'{text} != {data["Delivered"]}'
        delivered_quantity, delivered_price = order_view.check_items()
        assert draft_quantity == delivered_quantity, f'Error: draft_quantity: {draft_quantity} != delivered_quantity: {delivered_quantity}'
        assert draft_price == delivered_price, f'Error: draft_price: {draft_price} != delivered_price: {delivered_price}'
        order_view.click_close_button()
        print("-" * 50)
        print(f'Order change status: \n"{data["Draft"]}" --> \n"{data["New"]}" --> \n"{data["Processing"]}" --> \n"{data["Pending"]}" --> \n"{data["Shipped"]}" --> \n"{data["Delivered"]}" --> \n"{data["Archive"]}"')
        # ------------------------------------------------------------------------------------------------------------------

    # Archive
    assert order_list.element_visible(), 'OrdersList not open!'

    if status is False:
        order_list.find_row(client_name)

    order_list.click_change_status_button(data["Archive"])

    if status is False:
        print("-" * 50)
        print(f'Order change status: "{data["Draft"]}" --> "{data["Archive"]}"')


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


# All ------------------------------------------------------------------------------------------------------------------

# pytest tests/test_order/test_order.py::test_all -v --html=report.html --self-contained-html
def test_all():
    """Order test runner"""
    tests = [
        # Add
        {"name": "Order Add-A", "func": test_order_add_A},
        {"name": "Order Add-B", "func": test_order_add_B},
        {"name": "Order Add-C", "func": test_order_add_C},

        # Edit
        {"name": "Order Edit-A", "func": test_order_edit_A},

        # Status
        {"name": "Order Change Status-A", "func": test_order_change_status_A},
        {"name": "Order Change Status-B", "func": test_order_change_status_B},
        {"name": "Order Change Status-C", "func": test_order_change_status_C},
    ]

    passed_tests = []
    failed_tests = []
    total_tests = len(tests)

    print("\n=== Test Execution Summary ===")

    for test in tests:
        try:
            driver = get_driver()
            if driver is None:
                raise Exception("WebDriver initialization failed")

            test['func'](driver)
            passed_tests.append(test['name'])
            print(f"✅ {test['name']}: PASSED")
            print("*" * 50)
        except Exception as e:
            failed_tests.append({"name": test['name'], "error": str(e)})
            print(f"❌ {test['name']}: FAILED")
            print(f"   Error: {str(e)}")
            print("*" * 50)
        finally:
            if driver:
                driver.quit()
            time.sleep(1)

    print("\n=== Final Results ===")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {len(passed_tests)}")
    print(f"Failed: {len(failed_tests)}")

    if failed_tests:
        print("\nFailed Tests Details:")
        for test in failed_tests:
            print(f"❌ {test['name']}")
            print(f"   Error: {test['error']}\n")

    # Agar birorta test muvaffaqiyatsiz bo'lsa, pytest uchun xatolikni ko'rsatamiz
    assert len(failed_tests) == 0, "Some tests failed"
