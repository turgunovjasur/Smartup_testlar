import pytest
from autotest.anor.mcg.action_add.action_add import ActionAdd
from autotest.anor.mcg.action_list.action_list import ActionList
from autotest.anor.mcg.action_view.action_view import ActionIdView
from autotest.core.md.base_page import BasePage
from tests.test_base.test_base import test_data, login_user
from utils.driver_setup import driver


def test_action(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_action")

    # Test data
    data = test_data()["data"]
    action_name = 'Test_action'
    room_name = data["room_name"]
    warehouse_name = data["warehouse_name"]
    product_name = data["product_name"]
    product_quantity = 10
    bonus_product_name = data["product_name"]
    bonus_product_quantity = 10

    try:
        login_user(driver, url='anor/mcg/action_list')

        # Contract List
        action_list = ActionList(driver)
        assert action_list.element_visible(), base_page.logger.error('ActionList not open!')
        action_list.click_add_button()

        # Contract List
        action_add = ActionAdd(driver)
        assert action_add.element_visible(), base_page.logger.error('ActionAdd not open!')
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

        assert action_list.element_visible(), base_page.logger.error('ActionList not open!')
        action_list.find_row(action_name)
        action_list.click_view_button()

        # Contract List
        action_view = ActionIdView(driver)
        assert action_view.element_visible(), base_page.logger.error('ActionIdView not open!')
        get_action_name = action_view.get_elements()
        assert get_action_name == action_name, base_page.logger.error(f"{get_action_name} != {action_name}")
        action_view.click_close_button()
        base_page.logger.info(f"Action(✅): successfully added!")

    except AssertionError as ae:
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        pytest.fail(str(e))
