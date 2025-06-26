import time
from autotest.anor.mdeal.order.order_add.create_add_main import OrderAddMain
from autotest.anor.mdeal.order.order_add.order_add_final import OrderAddFinal
from autotest.anor.mdeal.order.order_add.order_add_product import OrderAddProduct
from autotest.anor.mdeal.order.order_add.order_select.order_select import OrderSelect
from autotest.core.md.base_page import BasePage

# ======================================================================================================================

def order_add_main(driver, **kwargs):
    order_add_main = OrderAddMain(driver)
    order_add_main.element_visible()

    room_name = kwargs.get("room_name")
    robot_name = kwargs.get("robot_name")
    client_name = kwargs.get("client_name")
    sub_filial_name = kwargs.get("sub_filial_name")
    contract_name = kwargs.get("contract_name")

    if room_name:
        order_add_main.click_rooms_input(room_name)

    if robot_name:
        order_add_main.click_robots_input(robot_name)

    if client_name:
        order_add_main.click_persons_input(client_name)

    if sub_filial_name:
        order_add_main.click_sub_filial_input(sub_filial_name)

    if contract_name:
        order_add_main.click_contract_input(contract_name)

    order_add_main.click_next_step_button()

# ======================================================================================================================

def order_add_product(driver, **kwargs):
    order_add_product = OrderAddProduct(driver)
    order_add_product.element_visible()

    order_grid_setting = kwargs.get("order_grid_setting", False)
    product_name = kwargs.get("product_name")
    warehouse_name = kwargs.get("warehouse_name")
    price_type_name = kwargs.get("price_type_name")
    product_quantity = kwargs.get("product_quantity")
    margin = kwargs.get("margin")

    if order_grid_setting:
        order_add_product.click_setting_button()

    if product_name and warehouse_name and price_type_name:
        order_add_product.input_name_product(product_name, warehouse_name, price_type_name)

    if product_quantity:
        order_add_product.input_quantity(product_quantity)

    if margin:
        order_add_product.click_percent_value_button(margin)

    order_add_product.click_next_step_button()

# ----------------------------------------------------------------------------------------------------------------------

def order_add_product_select(driver, **kwargs):
    order_add_product = OrderAddProduct(driver)

    product_name = kwargs.get("product_name")
    warehouse_name = kwargs.get("warehouse_name")
    price_type_name = kwargs.get("price_type_name")
    product_quantity = kwargs.get("product_quantity")

    if product_name and warehouse_name and price_type_name and product_quantity:
        order_add_product.click_select_button()
        order_select_modal = OrderSelect(driver)
        order_select_modal.element_visible()
        order_select_modal.input_warehouses(warehouse_name)
        order_select_modal.input_price_types(price_type_name)
        order_select_modal.input_product_quantity(product_quantity)
        order_select_modal.input_collect_row_button()
        order_select_modal.click_close_button()

# ======================================================================================================================

def order_add_final(driver, **kwargs):
    order_add_final = OrderAddFinal(driver)
    order_add_final.element_visible()

    payment_type_name = kwargs.get("payment_type_name")
    consignment_day = kwargs.get("consignment_day")
    consignment_amount = kwargs.get("consignment_amount")
    status_name = kwargs.get("status_name")

    if payment_type_name:
        order_add_final.input_payment_type(payment_type_name)

    if consignment_day and consignment_amount:
        order_add_final.input_consignment_date(consignment_day, consignment_amount)

    if status_name:
        order_add_final.input_status_2(status_name)

    order_add_final.click_save_button()
    time.sleep(2)

# ----------------------------------------------------------------------------------------------------------------------

def get_order_error_massage(driver, error_massage_name):
    base_page = BasePage(driver)
    order_add_final = OrderAddFinal(driver)
    order_add_final.element_visible()
    error_message = order_add_final.error_massage()
    if error_message == error_massage_name:
        base_page.logger.info("Error message validated successfully")
        order_add_final.click_error_close_button()
        return True
    else:
        base_page.logger.error(f'Error: Expected "{error_massage_name}", got "{error_message}"')
        base_page.take_screenshot(f"order_error_massage_{error_message.lower()}")
        raise AssertionError(f"Expected error message: '{error_massage_name}', got: '{error_message}'")

# ======================================================================================================================