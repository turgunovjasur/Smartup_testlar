import random
import pytest
from flows.auth_flow import login_user
from tests.test_input.flow_input import list_flow, check_transaction, check_report, view_flow, add_flow
from tests.test_purchase.flow_extra_cost import add_flow as extra_cost_add_flow

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order(590)
def test_add_input(driver, test_data, save_data, load_data):
    data = test_data["data"]
    warehouse_name = data["warehouse_name"]
    purchase_quantity = 10

    login_user(driver, test_data, url='anor/mkw/input/input_list')

    list_flow(driver, add=True)

    # InputAdd: 1
    input_number = random.randint(1000000, 9999999)
    save_data("input_number_1", input_number)
    add_flow(driver, input_number=input_number, warehouse_name=warehouse_name)

    # InputAdd: 2
    purchase_number = load_data("purchase_number_1")
    assert purchase_number is not None, f"{purchase_number} not found!"
    add_flow(driver, purchase_number=purchase_number, purchase_quantity=purchase_quantity)

    # InputAdd: 3
    add_flow(driver, save=True)

    list_flow(driver, find_row=input_number, view=True)

    view_flow(driver, check_input_number=input_number)

    list_flow(driver, find_row=input_number, status=True)
    list_flow(driver, find_row=input_number)

    check_transaction(driver)

    list_flow(driver)

    check_report(driver)

    list_flow(driver)

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order(600)
def test_add_input_with_extra_cost(driver, test_data, save_data, load_data):
    data = test_data["data"]
    warehouse_name = data["warehouse_name"]
    purchase_quantity = 10
    expense_article_name = data["expense_article_name"]
    corr_template_name = "Долг поставщикам"
    extra_cost_amount = data["product_price"] / 1.2

    login_user(driver, test_data, url='anor/mkw/input/input_list')

    list_flow(driver, add=True)

    # InputAdd: 1
    input_number = random.randint(1000000, 9999999)
    save_data("input_number_2", input_number)
    add_flow(driver, input_number=input_number, warehouse_name=warehouse_name, extra_cost_checkbox=True)

    # InputAdd: 2
    purchase_number = load_data("purchase_number_2")
    assert purchase_number is not None, f"{purchase_number} not found!"
    add_flow(driver, purchase_number=purchase_number, purchase_quantity=purchase_quantity)

    # InputAdd: 3
    add_flow(driver, add_extra_cost=True, next_step=False)

    # Add Extra Cost
    note_text = random.randint(10000, 99999)
    extra_cost_add_flow(driver,
                        expense_article_name=expense_article_name,
                        corr_template_name=corr_template_name,
                        extra_cost_amount=extra_cost_amount,
                        note_text=note_text,
                        method="V",
                        post=True)

    # InputAdd: 3
    add_flow(driver, calc_extra_cost=True)

    # InputAdd: 4
    add_flow(driver, save=True)

    list_flow(driver, find_row=input_number, view=True)

    view_flow(driver, check_input_number=input_number)

    list_flow(driver, find_row=input_number, status=True)

    list_flow(driver, find_row=input_number)

    check_transaction(driver)

    list_flow(driver)

    check_report(driver)

    list_flow(driver)

# ======================================================================================================================
