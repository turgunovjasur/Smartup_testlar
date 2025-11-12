import pytest
from flows.auth_flow import login_user
from pages.core.md.base_page import BasePage
from tests.ui.test_reference.flow_action import list_flow, add_flow, view_flow
from calendar import monthrange
from datetime import datetime

# ======================================================================================================================

def get_month_days(date_format="%d.%m.%Y"):
    """
    Joriy oyning birinchi kuni, oxirgi kuni va bugungi kunini berilgan formatda qaytaradi.

    Args:
        date_format (str): Sana formati (default: "%d.%m.%Y")

    Returns:
        tuple: (birinchi_kun, oxirgi_kun, bugungi_kun)
    """
    today = datetime.now()

    # Joriy oyning birinchi kuni
    first_day = today.replace(day=1)

    # Joriy oyning oxirgi kuni
    last_day_number = monthrange(today.year, today.month)[1]
    last_day = today.replace(day=last_day_number)

    # Bugungi kun
    current_day = today

    # Formatlash
    first_day_str = first_day.strftime(date_format)
    last_day_str = last_day.strftime(date_format)
    current_day_str = current_day.strftime(date_format)

    return first_day_str, last_day_str, current_day_str

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_I
@pytest.mark.order(480)
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

    first_day_str, last_day_str, current_day_str = get_month_days()
    if current_day_str == last_day_str:
        current_day_str = first_day_str
        base_page = BasePage(driver)
        base_page.logger.warning("Bugun oyning oxirgi kuni, current_day ga first_day qiymati beriladi")

    add_flow(driver,
             action_name=action_name,
             start_date=current_day_str,
             end_date=last_day_str,
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
@pytest.mark.order_group_I
@pytest.mark.order(481)
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

    first_day_str, last_day_str, current_day_str = get_month_days()
    if current_day_str == last_day_str:
        current_day_str = first_day_str
        base_page = BasePage(driver)
        base_page.logger.warning("Bugun oyning oxirgi kuni, current_day ga first_day qiymati beriladi")

    add_flow(driver,
             action_name=action_name,
             start_date=current_day_str,
             end_date=last_day_str,
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
