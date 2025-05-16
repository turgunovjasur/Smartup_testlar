import time
from autotest.anor.mdeal.order.order_add.create_order_page import OrderAddMain
from autotest.anor.mdeal.order.order_add.final_page import OrderAddFinal
from autotest.anor.mdeal.order.order_add.goods_page import OrderAddProduct
from autotest.anor.mdeal.order.order_view.order_view import OrderView
from autotest.core.md.base_page import BasePage
from autotest.trade.tdeal.order.order_list.orders_page import OrdersList
from tests.test_base.test_base import login_user
from tests.test_order.test_cashin import test_cashin_add_C
from tests.conftest import driver, test_data


def test_edit_order_with_consignment(driver, test_data):
    # Test data
    base_page = BasePage(driver)
    base_page.logger.info("▶️Test run: test_edit_order_with_consignment")

    data = test_data["data"]
    product_price = data["product_price"]
    client_name = f"{data['client_name']}-A"
    product_quantity_edit = 10

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_list = OrdersList(driver)
    assert order_list.element_visible(), 'OrdersList not open!'
    order_list.find_row(client_name)
    order_list.click_edit_button()

    # Order Add Main
    order_add_main = OrderAddMain(driver)
    assert order_add_main.element_visible(), 'OrderEditMain not open!'
    order_add_main.click_next_step_button()

    # Order Add Product
    order_add_product = OrderAddProduct(driver)
    assert order_add_product.element_visible(), 'OrderEditProduct not open!'
    order_add_product.input_quantity(product_quantity_edit)
    order_add_product.click_next_step_button()

    # Order Add Final
    order_add_final = OrderAddFinal(driver)

    def check_error_message():
        error_message = order_add_final.error_massage()
        if error_message == data["error_massage_2"]:
            base_page.logger.info("Error message validated successfully")
            order_add_final.click_error_close_button()
            return True
        else:
            base_page.logger.error(f'Error: Expected "{data["error_massage_2"]}", got "{error_message}"')
            base_page.logger.error("Consignment edit failed!")
            return False

    if not check_error_message():
        base_page.logger.error(f'Error: check_error_message')

    assert order_add_final.element_visible(), 'OrderEditFinal not open!'
    order_add_final.click_save_button()

    # Orders List
    assert order_list.element_visible(), 'OrdersList not open!'
    order_list.find_row(client_name)
    order_list.click_view_button()

    # Orders View
    order_view = OrderView(driver)
    assert order_view.element_visible(), 'OrderView not open!'

    order_id = order_view.check_order_id()
    get_quantity, get_price, total_sum = order_view.check_items()
    assert get_quantity == product_quantity_edit, f'Error: get_quantity: {get_quantity} != product_quantity_edit: {product_quantity_edit}'
    assert get_price == product_quantity_edit * product_price, f'Error: {get_quantity} != {product_quantity_edit} * {product_price}'
    base_page.logger.info(f'order_id: {order_id}')
    order_view.click_tablist_button(navbar_button='Консигнация')
    assert order_view.check_row_consignment(), f'Error: check_row_consignment'
    order_view.click_close_button()
    base_page.logger.info(f"✅Test end: test_edit_order_with_consignment")


def test_edit_order_for_price_type_USA(driver, test_data):
    # Test data
    base_page = BasePage(driver)
    base_page.logger.info("▶️Test run: test_edit_order_for_price_type_USA")

    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    product_name = data["product_name"]
    warehouse_name = data["warehouse_name"]
    price_type_name = data["price_type_name_UZB"]
    product_quantity_edit = 10

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_list = OrdersList(driver)
    assert order_list.element_visible(), 'OrdersList not open!'
    order_list.find_row(client_name)
    order_list.click_edit_button()

    # Order Add Main
    order_add_main = OrderAddMain(driver)
    assert order_add_main.element_visible(), 'OrderEditMain not open!'
    order_add_main.click_next_step_button()

    # Order Add Product
    order_add_product = OrderAddProduct(driver)
    assert order_add_product.element_visible(), 'OrderEditProduct not open!'
    order_add_product.input_name_product(product_name, warehouse_name, price_type_name, clear_input=True)
    order_add_product.input_quantity(product_quantity_edit)
    order_add_product.click_next_step_button()

    # Order Add Final
    order_add_final = OrderAddFinal(driver)
    assert order_add_final.element_visible(), 'OrderEditFinal not open!'
    get_total_amount = order_add_final.check_total_amount()  # 0

    order_add_final.input_status(status=6)
    order_add_final.click_save_button()

    error_massage = order_add_final.error_massage()
    assert error_massage == data["error_massage_3"], f'Error: "error_massage_3" not visible!'
    order_add_final.click_error_close_button()

    cut_url = base_page.cut_url()
    base_page.switch_window(direction="new", url=cut_url + 'trade/tcs/cashin_list')
    test_cashin_add_C(driver, test_data, amount=int(get_total_amount))

    base_page.switch_window(direction="back")
    base_page.refresh_page()
    order_add_main.click_next_step_button()
    assert order_add_product.element_visible(), 'OrderEditProduct not open!'
    order_add_product.input_name_product(product_name, warehouse_name, price_type_name, clear_input=True)
    order_add_product.input_quantity(product_quantity_edit)
    order_add_product.click_next_step_button()
    time.sleep(5)

    get_booked_payment_allowed = order_add_final.get_booked_payment_allowed()  # 120_000
    get_booked_payment_percentage = order_add_final.get_booked_payment_percentage()  # 50

    assert get_total_amount == get_booked_payment_allowed, f"get_total_amount: {get_total_amount} != get_booked_payment_allowed: {get_booked_payment_allowed}"

    prepayment_amount = get_total_amount * get_booked_payment_percentage / 100  # 120_000 * 50 / 100
    order_add_final.input_booked_payment_amount(prepayment_amount - 1)

    order_add_final.input_status(status=3)
    order_add_final.click_save_button()

    # Orders List
    assert order_list.element_visible(), 'OrdersList not open!'
    order_list.find_row(client_name)
    order_list.click_change_status_button(status_name='Доставлен')

    error_massage = order_add_final.error_massage()
    assert error_massage == data["error_massage_3"], f'Error: "{data["error_massage_3"]}" not visible!'
    order_add_final.click_error_close_button()
    order_list.click_edit_button()

    # Order Add Main
    assert order_add_main.element_visible(), 'OrderEditMain not open!'
    order_add_main.click_next_step_button()

    # Order Add Product
    assert order_add_product.element_visible(), 'OrderEditProduct not open!'
    order_add_product.click_next_step_button()

    order_add_final.input_booked_payment_amount(prepayment_amount)  # 60_000
    time.sleep(5)
    order_add_final.input_status(status=4)
    order_add_final.click_save_button()

    # Orders List
    assert order_list.element_visible(), 'OrdersList not open!'
    order_list.find_row(client_name)
    order_list.click_change_status_button(status_name='Доставлен')

    # Orders List
    assert order_list.element_visible(), 'OrdersList not open!'
    order_list.find_row(client_name)
    order_list.click_view_button()

    order_view = OrderView(driver)
    assert order_view.element_visible(), 'OrderView not open!'
    text = order_view.check_status()
    assert text == data["Delivered"], f'Error: text: {text} != Delivered: {data["Delivered"]}'
    order_view.click_close_button()

    assert order_list.element_visible(), 'OrdersList not open!'
    order_list.click_change_status_button(data["Archive"])

    base_page.logger.info(f"✅Test end: test_edit_order_for_price_type_USA")