import time

import pytest

from autotest.anor.mdeal.order.order_add.create_add_main import OrderAddMain
from autotest.anor.mdeal.order.order_add.order_add_final import OrderAddFinal
from autotest.anor.mdeal.order.order_add.order_add_product import OrderAddProduct
from autotest.anor.mdeal.order.order_view.order_view import OrderView
from autotest.core.md.base_page import BasePage
from autotest.core.md.biruni.grid_setting.grid_setting import GridSetting
from autotest.trade.tdeal.order.order_list.orders_list import OrdersList
from flows.auth_flow import login_user

# @pytest.mark.regression
# @pytest.mark.order(52)
# def test_add_order_for_action(driver, test_data):
#     data = test_data["data"]
#     room_name = data["room_name"]
#     robot_name = data["robot_name"]
#     product_name = data["product_name"]
#     warehouse_name = data["warehouse_name"]
#     percent_value = 10
#     sub_filial_name = data["sub_filial_name"]
#     price_type_name = data["price_type_name_USA"]
#     product_price = data["product_price_USA"]
#     payment_type_name = data["payment_type_name"]
#     client_name = f"{data['client_name']}-C"
#     contract_name = f"{data['contract_name']}-C-USA"
#     product_quantity = 10
#
#     # Login
#     login_user(driver, test_data, url='trade/tdeal/order/order_list')
#
#     # Orders List
#     order_list = OrdersList(driver)
#     base_page = BasePage(driver)
#     order_list.element_visible()
#     order_list.click_add_button()
#
#     # ------------------------------------------------------------------------------------------------------------------
#
#     # Order Step-1
#     order_add_main = OrderAddMain(driver)
#     order_add_main.element_visible()
#     order_add_main.click_rooms_input(room_name)
#     order_add_main.click_robots_input(robot_name)
#     order_add_main.click_persons_input(client_name)
#     order_add_main.click_sub_filial_input(sub_filial_name)
#     order_add_main.click_contract_input(contract_name)
#     order_add_main.click_next_step_button()
#
#     # ------------------------------------------------------------------------------------------------------------------
#
#     # Order Step-2
#     order_add_product = OrderAddProduct(driver)
#     order_add_product.element_visible()
#     order_add_product.click_setting_button()
#
#     # Grid Setting
#     grid_setting = GridSetting(driver)
#     grid_setting.element_visible()
#     grid_setting.click_save_default_button()
#
#     # Order Step-2
#     order_add_product.element_visible()
#     order_add_product.input_name_product(product_name, warehouse_name, price_type_name)
#     order_add_product.input_quantity(product_quantity)
#     # order_add_product.click_percent_value_button(percent_value)
#     order_add_product.click_nav_tablist_button(tablist_name='Акции')
#     order_add_product.click_action_checkbox_button()
#
#     order_add_product.click_nav_tablist_button(tablist_name='Товар')
#     order_add_product.click_next_step_button()
#
#     # ------------------------------------------------------------------------------------------------------------------
#
#     # Order Step-3
#     order_add_final = OrderAddFinal(driver)
#     order_add_final.element_visible()
#     order_add_final.input_payment_type(payment_type_name)
#     total_amount_margin = order_add_final.check_total_amount()  # 108
#
#     total_amount = product_quantity * product_price  # 10 * 12 = 120
#     total_margin = total_amount * percent_value / 100  # 12
#     total_sum = total_amount - total_margin  # 108
#     assert total_amount_margin == total_sum, f"{total_amount_margin} != {total_sum}"
#
#     order_add_final.input_status()
#     order_add_final.click_save_button()
#     time.sleep(2)
#
#     # ------------------------------------------------------------------------------------------------------------------
#
#     # Orders List
#     order_list.element_visible()
#     order_list.click_reload_button()
#     order_list.find_row(client_name)
#     order_list.click_view_button()
#
#     # Orders View
#     order_view = OrderView(driver)
#     order_view.element_visible()
#     order_id = order_view.get_input_value_in_order_view(input_name="ИД заказа")
#     base_page.logger.info(f"Order id: {order_id}")
#     order_view.click_setting_button()
#
#     # Grid Setting
#     grid_setting = GridSetting(driver)
#     grid_setting.element_visible()
#     grid_setting.click_save_default_button()
#
#     get_quantity, get_price, get_total_sum = order_view.check_items()
#     assert get_quantity == product_quantity, f"Error: get_quantity: {get_quantity} != product_quantity: {product_quantity}"
#     assert get_price == total_amount, f"Error: get_price: {get_price} != total_amount: {total_amount}"
#     assert get_total_sum == total_sum, f"Error: get_total_sum: {get_total_sum} != total_sum: {total_sum}"
#
#     order_view.click_close_button()


# @pytest.mark.regression
# @pytest.mark.order(53)
# def test_edit_order_for_action(driver, test_data):
#     data = test_data["data"]
#     product_price = data["product_price_USA"]
#     client_name = f"{data['client_name']}-C"
#     product_quantity = 10
#     edit_product_quantity = product_quantity - 2
#
#     # Login
#     login_user(driver, test_data, url='trade/tdeal/order/order_list')
#
#     # Orders List
#     order_list = OrdersList(driver)
#     base_page = BasePage(driver)
#     order_list.element_visible()
#     order_list.click_reload_button()
#     order_list.find_row(client_name)
#     order_list.click_edit_button()
#
#     # Order Step-1
#     order_add_main = OrderAddMain(driver)
#     order_add_main.element_visible()
#     order_add_main.click_next_step_button()
#
#     # Order Step-2
#     order_add_product = OrderAddProduct(driver)
#     order_add_product.element_visible()
#     order_add_product.input_quantity(edit_product_quantity)
#     order_add_product.click_setting_button()
#
#     # Grid Setting
#     grid_setting = GridSetting(driver)
#     grid_setting.element_visible()
#     grid_setting.click_save_default_button()
#
#     # Order Step-2
#     order_add_product.element_visible()
#     order_add_product.click_next_step_button()
#
#     # Order Step-3
#     order_add_final = OrderAddFinal(driver)
#     order_add_final.element_visible()
#     total_amount_margin = order_add_final.check_total_amount()  # 96
#     assert total_amount_margin == edit_product_quantity * product_price, \
#         f"{total_amount_margin} != {edit_product_quantity} * {product_price}"
#     order_add_final.input_status()
#     order_add_final.click_save_button()
#     time.sleep(2)
#
#     # Orders List
#     order_list.element_visible()
#     order_list.click_reload_button()
#     order_list.find_row(client_name)
#     order_list.click_view_button()
#
#     # Orders View
#     order_view = OrderView(driver)
#     order_view.element_visible()
#     order_id = order_view.get_input_value_in_order_view(input_name="ИД заказа")
#     base_page.logger.info(f"Order id: {order_id}")
#     order_view.click_setting_button()
#
#     # Grid Setting
#     grid_setting = GridSetting(driver)
#     grid_setting.element_visible()
#     grid_setting.click_save_default_button()
#
#     get_quantity, get_price, get_total_sum = order_view.check_items()
#     assert get_quantity == edit_product_quantity, f"Error: get_quantity: {get_quantity} != edit_product_quantity: {edit_product_quantity}"
#     assert get_price == total_amount_margin, f"Error: get_price: {get_price} != total_amount_margin: {total_amount_margin}"
#     assert get_total_sum == total_amount_margin, f"Error: get_total_sum: {get_total_sum} != total_amount_margin: {total_amount_margin}"
#
#     order_view.click_close_button()