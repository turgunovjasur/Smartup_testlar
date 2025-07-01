import time
import pytest
from autotest.anor.mdeal.order.order_add.create_add_main import OrderAddMain
from autotest.anor.mdeal.order.order_add.order_add_final import OrderAddFinal
from autotest.anor.mdeal.order.order_add.order_add_product import OrderAddProduct
from autotest.anor.mdeal.order.order_view.order_view import OrderView
from autotest.core.md.base_page import BasePage
from autotest.trade.tdeal.order.order_list.orders_list import OrdersList
from flows.auth_flow import login_user
from tests.test_cashin.test_cashin import test_cashin_add_C

# @pytest.mark.regression
# @pytest.mark.order(31)
# def test_edit_order_with_consignment(driver, test_data):
#     # Test data
#     base_page = BasePage(driver)
#
#     # ------------------------------------------------------------------------------------------------------------------
#
#     data = test_data["data"]
#     product_price = data["product_price"]
#     client_name = f"{data['client_name']}-A"
#     product_quantity_edit = 10
#
#     # ------------------------------------------------------------------------------------------------------------------
#
#     # Login
#     login_user(driver, test_data, url='trade/tdeal/order/order_list')
#
#     # ------------------------------------------------------------------------------------------------------------------
#
#     # OrdersList
#     order_list = OrdersList(driver)
#     order_list.element_visible()
#     order_list.find_row(client_name)
#     order_list.click_edit_button()
#
#     # ------------------------------------------------------------------------------------------------------------------
#
#     # Order Add Main
#     order_add_main = OrderAddMain(driver)
#     order_add_main.element_visible()
#     order_add_main.click_next_step_button()
#
#     # ------------------------------------------------------------------------------------------------------------------
#
#     # Order Add Product
#     order_add_product = OrderAddProduct(driver)
#     order_add_product.element_visible()
#     order_add_product.input_quantity(product_quantity_edit)
#     order_add_product.click_next_step_button()
#
#     # ------------------------------------------------------------------------------------------------------------------
#
#     # Order Add Final
#     order_add_final = OrderAddFinal(driver)
#
#     def check_error_message():
#         error_message = order_add_final.error_massage()
#         if error_message == data["error_massage_2"]:
#             base_page.logger.info("Error message validated successfully")
#             order_add_final.click_error_close_button()
#             return True
#         else:
#             base_page.logger.error(f'Error: Expected "{data["error_massage_2"]}", got "{error_message}"')
#             base_page.logger.error("Consignment edit failed!")
#             return False
#
#     if not check_error_message():
#         base_page.logger.error(f'Error: check_error_message')
#
#     order_add_final.element_visible()
#     order_add_final.click_save_button()
#
#     # ------------------------------------------------------------------------------------------------------------------
#
#     # Orders List
#     order_list.element_visible()
#     order_list.find_row(client_name)
#     order_list.click_view_button()
#
#     # ------------------------------------------------------------------------------------------------------------------
#
#     # Orders View
#     order_view = OrderView(driver)
#     order_view.element_visible()
#     order_id = order_view.get_input_value_in_order_view(input_name="ИД заказа")
#     get_quantity, get_price, total_sum = order_view.check_items()
#     assert get_quantity == product_quantity_edit, f'Error: get_quantity: {get_quantity} != product_quantity_edit: {product_quantity_edit}'
#     assert get_price == product_quantity_edit * product_price, f'Error: {get_quantity} != {product_quantity_edit} * {product_price}'
#     base_page.logger.info(f'order_id: {order_id}')
#     order_view.click_tablist_button(tablist_name='Консигнация')
#     order_view.check_row_consignment()
#     order_view.click_close_button()

    # ------------------------------------------------------------------------------------------------------------------
@pytest.mark.regression
@pytest.mark.order_group_C
@pytest.mark.order(45)
def test_edit_order_for_price_type_USA(driver, test_data):
    # Test data
    base_page = BasePage(driver)

    # ------------------------------------------------------------------------------------------------------------------

    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    product_name = data["product_name"]
    warehouse_name = data["warehouse_name"]
    price_type_name = data["price_type_name_UZB"]
    product_quantity_edit = 10

    # ------------------------------------------------------------------------------------------------------------------

    # Login
    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    # ------------------------------------------------------------------------------------------------------------------

    # OrdersList
    order_list = OrdersList(driver)
    order_list.element_visible()
    order_list.find_row(client_name)
    order_list.click_edit_button()

    # ------------------------------------------------------------------------------------------------------------------

    # Order Add Main
    order_add_main = OrderAddMain(driver)
    order_add_main.element_visible()
    order_add_main.click_next_step_button()

    # ------------------------------------------------------------------------------------------------------------------

    # Order Add Product
    order_add_product = OrderAddProduct(driver)
    order_add_product.element_visible()
    order_add_product.input_name_product(product_name, warehouse_name, price_type_name, clear_input=True)
    order_add_product.input_quantity(product_quantity_edit)
    order_add_product.click_next_step_button()

    # ------------------------------------------------------------------------------------------------------------------

    # Order Add Final
    order_add_final = OrderAddFinal(driver)
    order_add_final.element_visible()
    get_total_amount = order_add_final.check_total_amount()  # 0

    order_add_final.input_status(status=6)
    order_add_final.click_save_button()

    error_massage = order_add_final.error_massage()
    assert error_massage == data["error_massage_3"], f'Error: "error_massage_3" not visible!'
    order_add_final.click_error_close_button()

    # ------------------------------------------------------------------------------------------------------------------

    base_page.switch_window(direction="prepare")
    cut_url = base_page.cut_url()
    base_page.switch_window(direction="new", url=cut_url + 'trade/tcs/cashin_list')
    test_cashin_add_C(driver, test_data, amount=int(get_total_amount))
    base_page.switch_window(direction="back")
    base_page.refresh_page()

    # ------------------------------------------------------------------------------------------------------------------

    order_add_main.click_next_step_button()
    order_add_product.element_visible()
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

    # ------------------------------------------------------------------------------------------------------------------

    # Orders List
    order_list.element_visible()
    order_list.find_row(client_name)
    order_list.click_change_status_button(status_name='Доставлен')

    error_massage = order_add_final.error_massage()
    assert error_massage == data["error_massage_3"], f'Error: "{data["error_massage_3"]}" not visible!'
    order_add_final.click_error_close_button()
    order_list.click_edit_button()

    # ------------------------------------------------------------------------------------------------------------------

    # Order Add Main
    order_add_main.element_visible()
    order_add_main.click_next_step_button()

    # ------------------------------------------------------------------------------------------------------------------

    # Order Add Product
    order_add_product.element_visible()
    order_add_product.click_next_step_button()

    # ------------------------------------------------------------------------------------------------------------------

    # Order Add Final
    order_add_final.element_visible()
    order_add_final.input_booked_payment_amount(prepayment_amount)  # 60_000
    order_add_final.input_status(status=4)
    order_add_final.click_save_button()

    # ------------------------------------------------------------------------------------------------------------------

    # Orders List
    order_list.element_visible()
    order_list.find_row(client_name)
    order_list.click_change_status_button(status_name='Доставлен')

    # ------------------------------------------------------------------------------------------------------------------

    # Orders List
    order_list.element_visible()
    order_list.find_row(client_name)
    order_list.click_view_button()

    # ------------------------------------------------------------------------------------------------------------------

    # OrderView
    order_view = OrderView(driver)
    order_view.element_visible()
    text = order_view.get_input_value_in_order_view(input_name="Статус")
    assert text == data["Delivered"], f'Error: text: {text} != Delivered: {data["Delivered"]}'
    order_view.click_close_button()

    # ------------------------------------------------------------------------------------------------------------------

    # Orders List
    order_list.element_visible()
    order_list.click_change_status_button(data["Archive"])
    order_list.element_visible()

    # ------------------------------------------------------------------------------------------------------------------
