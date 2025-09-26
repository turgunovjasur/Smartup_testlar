import random
import time
from datetime import date
import pytest
from flows.auth_flow import login_user
from tests.test_payment_to_suppliers.flow_payment_to_suppliers import list_flow, add_flow, check_cashout_flow, \
    view_flow, check_audit_view_flow, check_main_view_flow, check_transaction_flow


@pytest.mark.regression
@pytest.mark.skip(reason="Bu test hali implementatsiya qilinmagan")
def test_payment_to_suppliers(driver, test_data, load_data, save_data):
    """Test adding a stocktaking"""

    data = test_data["data"]

    login_user(driver, test_data, url='trade/tcs/cashout_list')

    list_flow(driver, add=True)

    cashout_number = random.randint(100000, 999999)
    result = add_flow(driver,
                      cashout_number=cashout_number,
                      get_cashout_time=True)

    current_date = date.today().strftime("%d.%m.%Y")  # 22.08.2025
    assert current_date in result["get_cashout_time"]

    result = add_flow(driver,
             supplier_name=data["supplier_name"],
             payment_type=data["payment_type_name"],
             get_currency=True)

    assert result["get_currency"] == "Узбекский сум"

    result = add_flow(driver,
                      cash_register_name=data["cash_register_name"],
                      get_balance=True)

    add_flow(driver,
             input_amount=result["get_balance"],
             save=True)

    check_cashout_flow(driver,
                       cashout_number=cashout_number,
                       close=True)

    cashout_number = current_date  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    list_flow(driver,
              find_row=cashout_number,
              view=True)

    view_flow(driver, item_name="Основная информация")
    check_main_view_flow(driver,
                         cash_register_name=data["cash_register_name"],
                         current_date=current_date,
                         payment_type_name=data["payment_type_name"],
                         get_balance=result["get_balance"],
                         supplier_name=data["supplier_name"])

    view_flow(driver, item_name="История изменений")
    check_audit_view_flow(driver, column_name=current_date)
    view_flow(driver, close=True)

    list_flow(driver, find_row=cashout_number, post=True)
    list_flow(driver, find_row=cashout_number)

    check_transaction_flow(driver)

    list_flow(driver)

    time.sleep(2)