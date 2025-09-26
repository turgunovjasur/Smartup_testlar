import pytest
from autotest.anor.mkw.warehouse_add.warehouse_add import WarehouseAdd
from autotest.anor.mkw.warehouse_list.warehouse_list import WarehouseList
from autotest.anor.mkw.warehouse_type_add.warehouse_type_add import WarehouseTypeAdd
from autotest.anor.mkw.warehouse_view.warehouse_view import WarehouseView
from flows.auth_flow import login_user


@pytest.mark.regression
@pytest.mark.order(630)
def test_add_warehouse(driver, test_data):
    """Test adding a warehouse"""
    # Test data
    data = test_data["data"]
    warehouse_name = data["minor_warehouse_name"]
    warehouse_type_name = "Minor"
    room_name = data["room_name"]

    # Login
    login_user(driver, test_data, url='anor/mkw/warehouse_list')

    # WarehouseList
    warehouse_list = WarehouseList(driver)
    warehouse_list.element_visible()
    warehouse_list.click_add_button()

    # WarehouseAdd
    warehouse_add = WarehouseAdd(driver)
    warehouse_add.element_visible()
    warehouse_add.input_warehouse(warehouse_name)
    if not warehouse_add.input_warehouse_type(warehouse_type_name):

        # WarehouseTypeAdd
        warehouse_type_add = WarehouseTypeAdd(driver)
        warehouse_type_add.element_visible()
        warehouse_type_add.input_warehouse_name(warehouse_type_name)
        warehouse_type_add.click_save_button()

    # WarehouseAdd
    warehouse_add.input_room(room_name)
    warehouse_add.click_save_button()

    # WarehouseList
    warehouse_list.element_visible()
    warehouse_list.find_row(warehouse_name)
    warehouse_list.click_view_button()

    # WarehouseView
    warehouse_view = WarehouseView(driver)
    warehouse_view.element_visible()
    get_warehouse_name = warehouse_view.check_warehouse_name()
    assert get_warehouse_name == warehouse_name, f"Error: {get_warehouse_name} != {warehouse_name}"
    warehouse_view.click_close_button()

    # WarehouseList
    warehouse_list.element_visible()