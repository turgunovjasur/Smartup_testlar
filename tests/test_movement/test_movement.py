import random
from autotest.anor.mkw.balance.balance_list.balance_list import BalanceList
from autotest.anor.mkw.movement.movement_add.movement_add import MovementAdd
from autotest.anor.mkw.movement.movement_list.movement_list import MovementList
from autotest.anor.mkw.movement.movement_view.movement_view import MovementView
from autotest.core.md.base_page import BasePage
from tests.test_base.test_base import login_user
from tests.conftest import driver, test_data


def test_add_internal_movement(driver, test_data):
    """Test adding a internal movement"""
    base_page = BasePage(driver)

    # Test data
    data = test_data["data"]
    from_warehouses = data["warehouse_name"]
    to_warehouses = data["minor_warehouse_name"]
    product_name = data["product_name"]
    product_quantity = 10

    # Login
    login_user(driver, test_data, url='anor/mkw/movement/movement_list')

    # MovementList
    movement_list = MovementList(driver)
    movement_list.element_visible()
    movement_list.click_add_button()

    # MovementAdd (Main)
    movement_view = MovementAdd(driver)
    movement_view.element_visible()
    movement_number = random.randint(100000, 999999)
    movement_view.input_movement_number(movement_number)
    movement_view.input_from_warehouses(from_warehouses)
    movement_view.input_to_warehouses(to_warehouses)
    movement_view.click_next_step_button()

    # MovementAdd (TMZ)
    movement_view.element_visible()
    movement_view.input_product(product_name)
    movement_view.input_quantity(product_quantity)
    movement_view.click_next_step_button()

    # MovementAdd (Complete)
    movement_view.element_visible()
    movement_view.click_next_step_button(save=True)

    # MovementList
    movement_list.element_visible()
    movement_list.find_row(movement_number)
    movement_list.click_view_button()

    # MovementView
    movement_view = MovementView(driver)
    movement_view.element_visible()
    get_movement_number = movement_view.check_movement_number()
    assert get_movement_number == movement_number, f"Error: {get_movement_number} != {movement_number}"
    movement_view.click_close_button()

    # MovementList
    movement_list.element_visible()
    movement_list.find_row(movement_number)
    movement_list.click_status_button(status=4)

    # MovementList
    movement_list.element_visible()

    # BalanceList
    base_page.switch_window(direction="prepare")
    cut_url = base_page.cut_url()
    base_page.switch_window(direction="new", url=cut_url + 'anor/mkw/balance/balance_list')

    balance_list = BalanceList(driver)
    balance_list.element_visible()
    balance_list.click_reload_button()
    balance_list.find_row(to_warehouses)
    balance_list.click_detail_button()
    balance_list.click_reload_button()

    get_balance = balance_list.check_balance_quantity()
    assert get_balance == product_quantity, f"Error: {get_balance} != {product_quantity}"
