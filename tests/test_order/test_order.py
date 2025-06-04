import time
from autotest.anor.mdeal.order.order_add.create_add_main import OrderAddMain
from autotest.anor.mdeal.order.order_add.order_add_final import OrderAddFinal
from autotest.anor.mdeal.order.order_add.order_add_product import OrderAddProduct
from autotest.anor.mdeal.order.order_add.order_select.order_select import OrderSelect
from autotest.anor.mdeal.order.order_view.order_view import OrderView
from autotest.anor.mkw.product_file_list.product_file_list import ProductFileList
from autotest.core.md.biruni.grid_setting.grid_setting import GridSetting
from autotest.trade.tdeal.order.order_list.orders_list import OrdersList
from tests.conftest import driver, test_data
from tests.test_base.test_base import login_user
from autotest.core.md.base_page import BasePage

# Order Add ------------------------------------------------------------------------------------------------------------

def order_add(driver, test_data,
              client_name=None, contract_name=None, product_quantity=None, error_massage=False, return_quantity=None,
              consignment=None, consignment_amount=None, current_date_add_day=None, sub_filial=False, contract=True,
              price_type_name=None, product_price_USA=None, margin=False, select=False, setting=False, status=1,
              audit=False, file=False, transactions=False):

    # ------------------------------------------------------------------------------------------------------------------

    # Test data
    data = test_data["data"]
    room_name = data["room_name"]
    robot_name = data["robot_name"]
    product_name = data["product_name"]
    warehouse_name = data["warehouse_name"]
    percent_value = data["percent_value"]
    sub_filial_name = data["sub_filial_name"]
    price_type_name = price_type_name or data["price_type_name_UZB"]
    product_price = product_price_USA or data["product_price"]
    payment_type_name = data["payment_type_name"]
    client_name = client_name or data["client_name"]
    contract_name = contract_name or data["contract_name"]
    product_quantity = product_quantity or data["product_quantity"]
    return_quantity = return_quantity or product_quantity

    # ------------------------------------------------------------------------------------------------------------------

    # Login
    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    # ------------------------------------------------------------------------------------------------------------------

    # Orders List
    order_list = OrdersList(driver)
    base_page = BasePage(driver)
    order_list.element_visible()
    order_list.click_add_button()

    # ------------------------------------------------------------------------------------------------------------------

    # Order Add Main
    order_add_main = OrderAddMain(driver)
    order_add_main.element_visible()
    order_add_main.click_rooms_input(room_name)
    order_add_main.click_robots_input(robot_name)
    order_add_main.click_persons_input(client_name)

    if sub_filial:
        order_add_main.click_sub_filial_input(sub_filial_name)

    if contract:
        order_add_main.click_contract_input(contract_name)
    order_add_main.click_next_step_button()

    # ------------------------------------------------------------------------------------------------------------------

    # Order Add Product
    order_add_product = OrderAddProduct(driver)
    order_add_product.element_visible()

    if setting:
        order_add_product.click_setting_button()

        # Grid Setting
        grid_setting = GridSetting(driver)
        grid_setting.element_visible()
        grid_setting.click_save_default_button()

    if select:
        order_add_product.click_select_button()

        # Order Select
        order_select = OrderSelect(driver)
        order_select.element_visible()
        order_select.input_warehouses(warehouse_name)
        order_select.input_price_types(price_type_name)
        order_select.input_product_quantity(product_quantity)
        order_select.input_collect_row_button()
        order_select.click_close_button()
        order_add_product.element_visible()

    if not select:
        order_add_product.input_name_product(product_name, warehouse_name, price_type_name)
        order_add_product.input_quantity(product_quantity)

    if margin:
        order_add_product.click_percent_value_button(percent_value)

    order_add_product.click_next_step_button()

    # ------------------------------------------------------------------------------------------------------------------

    # Order Add Final
    order_add_final = OrderAddFinal(driver)
    order_add_final.element_visible()
    order_add_final.input_payment_type(payment_type_name)
    total_amount_margin = order_add_final.check_total_amount()  # 228
    total_amount = product_quantity * product_price  # 240
    total_margin = total_amount * percent_value / 100  # 12

    if margin:
        assert total_amount == total_amount_margin + total_margin, f"{total_amount} != {total_amount_margin} * {total_margin}"

    if consignment:
        order_add_final.input_consignment_date(current_date_add_day, consignment_amount)

    order_add_final.input_status(status)
    order_add_final.click_save_button()
    time.sleep(2)

    if error_massage:
        error_massage = order_add_final.error_massage()
        assert error_massage == data["error_massage_1"], f'Error: "{data["error_massage_1"]}" not visible!'
        base_page.logger.info(f'Test error_massage: successfully!')
        order_add_final.click_error_close_button()
        order_add_final.click_prev_step_button()
        order_add_product.input_quantity(return_quantity)
        order_add_product.click_next_step_button()
        order_add_final.element_visible()
        order_add_final.click_save_button()
        time.sleep(2)

    # ------------------------------------------------------------------------------------------------------------------

    # Orders List
    order_list.element_visible()
    order_list.click_reload_button()
    order_list.find_row(client_name)
    order_list.click_view_button()

    # ------------------------------------------------------------------------------------------------------------------

    # Orders View
    order_view = OrderView(driver)
    order_view.element_visible()
    order_id = order_view.check_order_id()
    base_page.logger.info(f"Order ID: {order_id}")

    if setting:
        order_view.click_setting_button()

        # Grid Setting
        grid_setting = GridSetting(driver)
        grid_setting.element_visible()
        grid_setting.click_save_default_button()

    get_quantity, get_price, total_sum = order_view.check_items()

    if error_massage:
        assert get_quantity == return_quantity, f'Error: get_quantity: {get_quantity} != return_quantity: {return_quantity}'
        assert get_price == return_quantity * product_price, f'Error: get_quantity {get_quantity} != {return_quantity} * {product_price}'

    if not error_massage:
        assert get_quantity == product_quantity, f'Error: get_quantity: {get_quantity} != product_quantity: {product_quantity}'
        assert get_price == product_quantity * product_price, f'Error: get_price: {get_price} != {product_quantity} * {product_price}'

    if margin:
        assert get_price == product_quantity * product_price_USA, f'Error: get_price: {get_price} != {product_quantity} * {product_price_USA}'
        assert total_sum == get_price - total_margin, f'Error: total_sum: {total_sum} != {get_price} - {total_margin}'

    # Check consignment
    if consignment:
        order_view.click_tablist_button(tablist_name='Консигнация')
        get_consignment_amount = order_view.check_consignments(current_date_add_day)
        get_consignment_amount = int(get_consignment_amount.replace(" ", ""))
        assert get_consignment_amount == consignment_amount, f'Error: {get_consignment_amount} != {consignment_amount}'

    # Check audit
    if audit:
        order_view.click_tablist_button(tablist_name='История изменений')
        order_view.click_navbar_button(navbar_name='Название')
        order_view.check_tablist_body(header=True)
        order_view.click_navbar_button(navbar_name='ТМЦ')
        order_view.check_tablist_body(product=True)
        order_view.find_row(product_name)
        order_view.click_audit_details_button()
        order_view.check_get_order_audit_body()
        order_view.click_close_toolbar_button()

    order_view.click_close_button()

    # ------------------------------------------------------------------------------------------------------------------

    # Orders List
    order_list.element_visible()

    # ------------------------------------------------------------------------------------------------------------------

    # file
    if file:
        order_list.click_reload_button()
        order_list.element_visible()
        order_list.find_row(client_name)
        order_list.click_view_dropdown(file_name='Файлы')

        # Product File List
        product_file_list = ProductFileList(driver)
        product_file_list.element_visible()
        product_file_list.click_close_button()

    # ------------------------------------------------------------------------------------------------------------------

    # Orders List
    order_list.element_visible()

    # ------------------------------------------------------------------------------------------------------------------

    # transactions
    if transactions:
        order_list.click_reload_button()
        order_list.element_visible()
        order_list.find_row(client_name)
        order_list.click_view_dropdown(file_name='Проводки')

    # ------------------------------------------------------------------------------------------------------------------

    # Orders List
    order_list.element_visible()

    # ------------------------------------------------------------------------------------------------------------------



def test_add_order_with_consignment(driver, test_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_order_with_consignment")

    # Test data
    data = test_data["data"]
    client_name = f"{data['client_name']}-A"
    contract_name = f"{data['contract_name']}-A-UZB"
    product_quantity = 15
    current_date_add_day = 30
    consignment_amount = product_quantity * data["product_price"]
    order_add(driver, test_data,
              client_name=client_name,
              contract_name=contract_name,
              product_quantity=product_quantity,
              consignment=True,
              audit=True,
              consignment_amount=consignment_amount,
              current_date_add_day=current_date_add_day)


def test_add_order_with_contract(driver, test_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_order_with_contract")

    # Test data
    data = test_data["data"]
    client_name = f"{data['client_name']}-B"
    contract_name = f"{data['contract_name']}-B-UZB"
    product_quantity = 101
    return_quantity = 15
    order_add(driver, test_data,
              client_name=client_name,
              contract_name=contract_name,
              product_quantity=product_quantity,
              return_quantity=return_quantity,
              error_massage=True)


def test_add_order_with_price_type_USA(driver, test_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_order_with_price_type_USA")

    # Test data
    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    price_type_name = data['price_type_name_USA']
    product_price_USA = data['product_price_USA']
    product_quantity = 20
    order_add(driver, test_data,
              client_name=client_name,
              contract=False,
              price_type_name=price_type_name,
              product_price_USA=product_price_USA,
              product_quantity=product_quantity,
              margin=True,
              status=2,
              file=True,
              transactions=True)


def test_order_add_for_sub_filial_select(driver, test_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_order_add_for_sub_filial_select")

    # Test data
    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    contract_name = f"{data['contract_name']}-C-USA"
    price_type_name = data['price_type_name_USA']
    product_price_USA = data['product_price_USA']
    product_quantity = 10
    order_add(driver, test_data,
              client_name=client_name,
              sub_filial=True,
              contract_name=contract_name,
              price_type_name=price_type_name,
              product_price_USA=product_price_USA,
              product_quantity=product_quantity,
              margin=True,
              select=True,
              setting=True)

# Copy -----------------------------------------------------------------------------------------------------------------

def order_copy(driver, test_data, client_name=None, client_name_copy_A=None, client_name_copy_B=None):
    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    # List
    order_list = OrdersList(driver)
    order_list.element_visible()
    order_list.find_row(client_name)
    order_list.click_copy_button()

    # Copy
    order_list.element_visible_copy_title()
    order_list.input_persons(client_name_copy_A, client_name_copy_B)
    order_list.click_copy_save_button()

    # List
    order_list.element_visible()
    order_list.find_row(client_name_copy_A)
    order_list.click_view_button()

    # View client_A
    order_view = OrderView(driver)
    order_view.element_visible()
    get_client_name = order_view.check_client_name()
    assert get_client_name == client_name_copy_A, f"{get_client_name} != {client_name_copy_A}"
    order_view.click_close_button()

    # List
    order_list.click_reload_button()
    order_list.element_visible()
    order_list.find_row(client_name_copy_B)
    order_list.click_view_button()

    # View client_B
    order_view.element_visible()
    get_client_name = order_view.check_client_name()
    assert get_client_name == client_name_copy_B, f"{get_client_name} != {client_name_copy_B}"
    order_view.click_close_button()


def test_order_copy_C_for_A_B(driver, test_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_order_copy_C_for_A_B")

    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    client_name_copy_A = f"{data['client_name']}-A"
    client_name_copy_B = f"{data['client_name']}-B"
    order_copy(driver, test_data,
               client_name=client_name,
               client_name_copy_A=client_name_copy_A,
               client_name_copy_B=client_name_copy_B)

# Order list -----------------------------------------------------------------------------------------------------------

def order_list(driver, test_data):
    # Log
    data = test_data()["data"]

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_list = OrdersList(driver)
    order_view = OrderView(driver)

    # Order_A
    order_list.element_visible()
    order_list.click_reload_button()
    order_list.find_row(f"{data['client_name']}-A")
    order_list.click_view_button()
    order_view.element_visible()
    get_order_id_A = order_view.check_order_id()
    get_quantity_A, get_price_A = order_view.check_items()
    order_view.click_close_button()

    # Order_B
    order_list.element_visible()
    order_list.click_reload_button()
    order_list.find_row(f"{data['client_name']}-B")
    order_list.click_view_button()
    order_view.element_visible()
    get_order_id_B = order_view.check_order_id()
    get_quantity_B, get_price_B = order_view.check_items()
    order_view.click_close_button()

    # Order_C
    order_list.element_visible()
    order_list.click_reload_button()
    order_list.find_row(f"{data['client_name']}-C")
    order_list.click_view_button()
    order_view.element_visible()
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


def test_order_list(driver, test_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_order_list")

    order_list(driver, test_data)