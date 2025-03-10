import pytest
from autotest.anor.mcg.action_add.action_add import ActionAdd
from autotest.anor.mcg.action_list.action_list import ActionList
from autotest.anor.mcg.action_view.action_view import ActionIdView
from autotest.core.md.base_page import BasePage
from tests.test_base.test_base import login_user
from utils.driver_setup import driver
from tests.conftest import test_data


def test_add_action(driver, test_data):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_action")

    # Test data
    data = test_data["data"]
    action_name = 'Test_action'
    room_name = data["room_name"]
    warehouse_name = data["warehouse_name"]
    product_name = data["product_name"]
    product_quantity = 10
    bonus_product_name = data["product_name"]
    bonus_product_quantity = 10

    try:
        login_user(driver, test_data, url='anor/mcg/action_list')

        # Contract List
        action_list = ActionList(driver)
        assert action_list.element_visible(), 'ActionList not open!'
        action_list.click_add_button()

        # Contract List
        action_add = ActionAdd(driver)
        assert action_add.element_visible(), 'ActionAdd not open!'
        action_add.input_name(action_name)
        action_add.input_room(room_name)
        action_add.input_bonus_warehouse(warehouse_name)
        action_add.click_step_button()

        action_add.input_product_name(product_name)
        action_add.input_product_quantity(product_quantity)
        action_add.input_bonus_product(bonus_product_name)
        action_add.input_bonus_product_quantity(bonus_product_quantity)
        action_add.input_bonus_kind()
        action_add.click_save_button()

        assert action_list.element_visible(), 'ActionList not open after save!'
        action_list.find_row(action_name)
        action_list.click_view_button()

        # Contract List
        action_view = ActionIdView(driver)
        assert action_view.element_visible(), 'ActionIdView not open!'
        get_action_name = action_view.get_elements()
        assert get_action_name == action_name, f"Error: {get_action_name} != {action_name}"
        action_view.click_close_button()
        base_page.logger.info(f"✅ Test end: test_add_action")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))
