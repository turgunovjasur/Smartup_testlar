import random
import pytest

from autotest.core.md.base_page import BasePage
from conftest import load_data
from flows.auth_flow import login_user
from tests.test_purchase.test_purchase import add_purchase
from autotest.anor.mkw.return_supplier.return_add.return_add import ReturnAdd
from autotest.anor.mkw.return_supplier.return_list.return_list import ReturnList
from autotest.anor.mkw.return_supplier.return_view.return_view import ReturnView


@pytest.mark.regression
@pytest.mark.order(610)
def test_add_purchase_to_supplier(driver, test_data, save_data):
    """Test adding purchase_to_supplier"""

    save_purchase_number = "purchase_number_5"
    add_purchase(driver, test_data, save_data, save_purchase_number)


@pytest.mark.regression
@pytest.mark.order(620)
def test_return_to_supplier(driver, test_data, load_data):
    data = test_data["data"]

    # Login
    login_user(driver, test_data, url='anor/mkw/return/return_list')

    # List
    return_list = ReturnList(driver)
    return_list.element_visible()
    return_list.click_add_button()

    # Add Main
    return_add = ReturnAdd(driver)

    purchase_number_5 = load_data("purchase_number_5")
    return_add.input_purchases(purchase_number_5)

    return_number = random.randint(100000, 999999)
    return_add.input_return_number(return_number)

    return_add.input_warehouses(data["warehouse_name"])

    get_purchase_number_5 = return_add.get_input_value(input_name="Номер закупки")
    assert get_purchase_number_5 == str(purchase_number_5)

    get_supplier_name = return_add.get_input_value(input_name="Поставщик")
    assert get_supplier_name == data["supplier_name"]

    get_currency_name = return_add.get_input_value(input_name="Валюта")
    assert get_currency_name == "Узбекский сум"

    return_add.click_next_step_button()

    # Add TMZ
    return_add.element_visible()
    return_add.input_product_search(data["product_name"])
    return_add.input_product_quantity(product_quantity=10)
    return_add.click_percent_value_button(percent_value=5)
    return_add.click_next_step_button()

    # Add Final
    return_add.element_visible()
    return_add.click_next_step_button(save=True)

    # List
    return_list.element_visible()
    return_list.find_row(return_number)
    return_list.click_view_button()

    # View
    return_view = ReturnView(driver)
    return_view.element_visible()

    get_purchase_number = return_view.get_input_value(input_name="Номер закупки")
    assert int(get_purchase_number) == purchase_number_5

    get_currency = return_view.get_input_value(input_name="Валюта")
    assert get_currency == "Узбекский сум"

    get_supplier = return_view.get_input_value(input_name="Поставщик")
    assert get_supplier == data["supplier_name"]

    get_warehouse = return_view.get_input_value(input_name="Склад")
    assert get_warehouse == data["warehouse_name"]

    get_total_amount = return_view.get_input_value(input_name="Общая сумма возврата", clean=True)
    assert int(get_total_amount) == 10 * data["product_price"]

    return_view.click_close_button()

    # List
    return_list.element_visible()
    return_list.find_row(return_number)

    # Check transactions
    base_page = BasePage(driver)
    base_page.switch_window(direction="prepare")
    return_list.click_transaction_button()
    base_page.switch_window(direction="forward")
    return_list.check_transaction_body(timeout=20)
    base_page.switch_window(direction="back")

    # List
    return_list.element_visible()