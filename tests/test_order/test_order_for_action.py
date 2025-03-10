import time
import pytest
from autotest.anor.mdeal.order.order_add.create_order_page import OrderAddMain
from autotest.anor.mdeal.order.order_add.final_page import OrderAddFinal
from autotest.anor.mdeal.order.order_add.goods_page import OrderAddProduct
from autotest.anor.mdeal.order.order_view.order_view import OrderView
from autotest.core.md.base_page import BasePage
from autotest.core.md.biruni.grid_setting.grid_setting import GridSetting
from autotest.trade.tdeal.order.order_list.orders_page import OrdersList
from tests.test_base.test_base import login_user
from tests.conftest import test_data
from utils.driver_setup import driver


def test_add_order_for_action(driver, test_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_order_for_action")

    data = test_data["data"]
    room_name = data["room_name"]
    robot_name = data["robot_name"]
    product_name = data["product_name"]
    warehouse_name = data["warehouse_name"]
    percent_value = 10
    sub_filial_name = data["sub_filial_name"]
    price_type_name = data["price_type_name_USA"]
    product_price = data["product_price_USA"]
    payment_type_name = data["payment_type_name"]
    client_name = f"{data['client_name']}-C"
    contract_name = f"{data['contract_name']}-C-USA"
    product_quantity = 10

    try:
        # Login
        login_user(driver, test_data, url='trade/tdeal/order/order_list')

        # Orders List
        order_list = OrdersList(driver)
        base_page = BasePage(driver)
        assert order_list.element_visible(), 'OrdersList not open!'
        order_list.click_add_button()

        # ------------------------------------------------------------------------------------------------------------------

        # Order Step-1
        order_add_main = OrderAddMain(driver)
        assert order_add_main.element_visible(), 'OrderAddMain not open!'
        order_add_main.click_rooms_input(room_name)
        order_add_main.click_robots_input(robot_name)
        order_add_main.click_persons_input(client_name)
        order_add_main.click_sub_filial_input(sub_filial_name)
        order_add_main.click_contract_input(contract_name)
        order_add_main.click_next_step_button()

        # ------------------------------------------------------------------------------------------------------------------

        # Order Step-2
        order_add_product = OrderAddProduct(driver)
        assert order_add_product.element_visible(), 'OrderAddProduct not open!'
        order_add_product.click_setting_button()

        # Grid Setting
        grid_setting = GridSetting(driver)
        assert grid_setting.element_visible(), '(OrderAddProduct) -> GridSetting not open!'
        grid_setting.click_save_default_button()

        # Order Step-2
        assert order_add_product.element_visible(), 'OrderAddProduct not open!'
        order_add_product.input_name_product(product_name, warehouse_name, price_type_name)
        order_add_product.input_quantity(product_quantity)
        # order_add_product.click_percent_value_button(percent_value)
        order_add_product.click_nav_tablist_button(nav_tablist=7)
        order_add_product.click_action_checkbox_button()

        order_add_product.click_nav_tablist_button(nav_tablist=1)
        order_add_product.click_next_step_button()

        # ------------------------------------------------------------------------------------------------------------------

        # Order Step-3
        order_add_final = OrderAddFinal(driver)
        assert order_add_final.element_visible(), 'OrderAddFinal not open!'
        order_add_final.input_payment_type(payment_type_name)
        total_amount_margin = order_add_final.check_total_amount()  # 108

        total_amount = product_quantity * product_price  # 10 * 12 = 120
        total_margin = total_amount * percent_value / 100  # 12
        total_sum = total_amount - total_margin  # 108
        assert total_amount_margin == total_sum, f"{total_amount_margin} != {total_sum}"

        order_add_final.input_status()
        order_add_final.click_save_button()
        time.sleep(2)

        # ------------------------------------------------------------------------------------------------------------------

        # Orders List
        assert order_list.element_visible(), 'OrdersList not open!'
        order_list.click_reload_button()
        order_list.find_row(client_name)
        order_list.click_view_button()

        # Orders View
        order_view = OrderView(driver)
        assert order_view.element_visible(), 'OrderView not open!'
        order_id = order_view.check_order_id()
        base_page.logger.info(f"Order id: {order_id}")
        order_view.click_setting_button()

        # Grid Setting
        grid_setting = GridSetting(driver)
        assert grid_setting.element_visible(), '(OrderView) -> GridSetting not open!'
        grid_setting.click_save_default_button()

        get_quantity, get_price, get_total_sum = order_view.check_items()
        assert get_quantity == product_quantity, f"Error: get_quantity: {get_quantity} != product_quantity: {product_quantity}"
        assert get_price == total_amount, f"Error: get_price: {get_price} != total_amount: {total_amount}"
        assert get_total_sum == total_sum, f"Error: get_total_sum: {get_total_sum} != total_sum: {total_sum}"

        order_view.click_close_button()
        base_page.logger.info(f"✅ Test end: test_add_order_for_action")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_edit_order_for_action(driver, test_data):

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_edit_order_for_action")

    data = test_data["data"]
    product_price = data["product_price_USA"]
    client_name = f"{data['client_name']}-C"
    product_quantity = 10
    edit_product_quantity = product_quantity - 2

    try:
        # Login
        login_user(driver, test_data, url='trade/tdeal/order/order_list')

        # Orders List
        order_list = OrdersList(driver)
        base_page = BasePage(driver)
        assert order_list.element_visible(), 'OrdersList not open!'
        order_list.click_reload_button()
        order_list.find_row(client_name)
        order_list.click_edit_button()

        # ------------------------------------------------------------------------------------------------------------------

        # Order Step-1
        order_add_main = OrderAddMain(driver)
        assert order_add_main.element_visible(), 'OrderAddMain not open!'
        order_add_main.click_next_step_button()

        # ------------------------------------------------------------------------------------------------------------------

        # Order Step-2
        order_add_product = OrderAddProduct(driver)
        assert order_add_product.element_visible(), 'OrderAddProduct not open!'
        order_add_product.input_quantity(edit_product_quantity)
        order_add_product.click_setting_button()

        # Grid Setting
        grid_setting = GridSetting(driver)
        assert grid_setting.element_visible(), '(OrderAddProduct) -> GridSetting not open!'
        grid_setting.click_save_default_button()

        # Order Step-2
        assert order_add_product.element_visible(), 'OrderAddProduct not open!'
        order_add_product.click_next_step_button()

        # ------------------------------------------------------------------------------------------------------------------

        # Order Step-3
        order_add_final = OrderAddFinal(driver)
        assert order_add_final.element_visible(), 'OrderAddFinal not open!'
        total_amount_margin = order_add_final.check_total_amount()  # 96
        assert total_amount_margin == edit_product_quantity * product_price, \
            f"{total_amount_margin} != {edit_product_quantity} * {product_price}"
        order_add_final.input_status()
        order_add_final.click_save_button()
        time.sleep(2)

        # ------------------------------------------------------------------------------------------------------------------

        # Orders List
        assert order_list.element_visible(), 'OrdersList not open after save!'
        order_list.click_reload_button()
        order_list.find_row(client_name)
        order_list.click_view_button()

        # Orders View
        order_view = OrderView(driver)
        assert order_view.element_visible(), 'OrderView not open!'
        order_id = order_view.check_order_id()
        base_page.logger.info(f"Order id: {order_id}")
        order_view.click_setting_button()

        # Grid Setting
        grid_setting = GridSetting(driver)
        assert grid_setting.element_visible(), '(OrderView) -> GridSetting not open!'
        grid_setting.click_save_default_button()

        get_quantity, get_price, get_total_sum = order_view.check_items()
        assert get_quantity == edit_product_quantity, f"Error: get_quantity: {get_quantity} != edit_product_quantity: {edit_product_quantity}"
        assert get_price == total_amount_margin, f"Error: get_price: {get_price} != total_amount_margin: {total_amount_margin}"
        assert get_total_sum == total_amount_margin, f"Error: get_total_sum: {get_total_sum} != total_amount_margin: {total_amount_margin}"

        order_view.click_close_button()
        base_page.logger.info(f"✅ Test end: test_edit_order_for_action")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))
