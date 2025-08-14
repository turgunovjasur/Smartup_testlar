import pytest
from flows.auth_flow import login_user
from tests.test_reference.flow_action import list_flow, add_flow, view_flow

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order(51)
def test_add_action_cash_money(driver, test_data, assertions):
    data = test_data["data"]
    action_name = 'Test_action_cash_money'
    room_name = data["room_name"]
    warehouse_name = data["warehouse_name"]
    payment_type_name = data["payment_type_name"]
    product_name = data["product_name"]
    product_quantity = 10
    bonus_product_name = data["product_name"]
    kind_name = "Скидка"
    bonus_product_quantity = 10

    login_user(driver, test_data, url='anor/mcg/action_list')
    list_flow(driver, add=True)
    add_flow(driver,
             action_name=action_name,
             room_name=room_name,
             warehouse_name=warehouse_name,
             payment_type_name=payment_type_name,
             required_state=True,
             next_step=True)
    add_flow(driver,
             product_name=product_name,
             product_quantity=product_quantity,
             bonus_product_name=bonus_product_name,
             bonus_product_quantity=bonus_product_quantity,
             kind_name=kind_name)
    list_flow(driver, find_row=action_name, view=True)
    view_flow(driver, assertions, action_name=action_name)
    list_flow(driver)

# ======================================================================================================================
@pytest.mark.regression
@pytest.mark.order(51)
@pytest.mark.order(after="test_add_action_cash_money")
def test_add_action_terminal(driver, test_data, assertions):
    data = test_data["data"]
    action_name = 'Test_action_terminal'
    room_name = data["room_name"]
    warehouse_name = data["warehouse_name"]
    payment_type_name = "Терминал"
    product_name = data["product_name"]
    product_quantity = 10
    bonus_product_name = data["product_name"]
    kind_name = "Скидка"
    bonus_product_quantity = 20

    login_user(driver, test_data, url='anor/mcg/action_list')
    list_flow(driver, add=True)
    add_flow(driver,
             action_name=action_name,
             room_name=room_name,
             warehouse_name=warehouse_name,
             payment_type_name=payment_type_name,
             required_state=True,
             next_step=True)
    add_flow(driver,
             product_name=product_name,
             product_quantity=product_quantity,
             bonus_product_name=bonus_product_name,
             bonus_product_quantity=bonus_product_quantity,
             kind_name=kind_name)
    list_flow(driver, find_row=action_name, view=True)
    view_flow(driver, assertions, action_name=action_name)
    list_flow(driver)

# ======================================================================================================================
