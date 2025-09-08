from autotest.core.md.base_page import BasePage
from autotest.trade.tcs.cashout_add.cashout_add import CashoutAdd
from autotest.trade.tcs.cashout_list.cashout_list import CashoutList
from autotest.trade.tcs.cashout_view.cashout_view import CashoutView

# ======================================================================================================================

def list_flow(driver, **kwargs):
    c_list = CashoutList(driver)
    c_list.element_visible()

    if kwargs.get("add"):
        c_list.click_add_button()

    find_row = kwargs.get("find_row")
    if find_row:
        c_list.find_row(find_row)

    if kwargs.get("view"):
        c_list.click_view_button()

    if kwargs.get("post"):
        c_list.click_post_button()

    if kwargs.get("transaction"):
        c_list.click_transaction_button()

# ======================================================================================================================

def add_flow(driver, **kwargs):
    c_add = CashoutAdd(driver)
    c_add.element_visible()

    result = {}

    cashout_number = kwargs.get("cashout_number")
    if cashout_number:
        c_add.input_cashout_number(cashout_number)

    if kwargs.get("get_cashout_time"):
        result["get_cashout_time"] =  c_add.get_input_cashout_time()

    supplier_name = kwargs.get("supplier_name")
    if supplier_name:
        c_add.input_suppliers(supplier_name)

    payment_type = kwargs.get("payment_type")
    if payment_type:
        c_add.input_payment_types(payment_type)

    if kwargs.get("get_currency"):
        result["get_currency"] = c_add.get_input_currencies()

    cash_register_name = kwargs.get("cash_register_name")
    if cash_register_name:
        c_add.input_cashboxes(cash_register_name)

    if kwargs.get("get_balance"):
        result["get_balance"] = c_add.get_balance()

    input_amount = kwargs.get("input_amount")
    if input_amount:
        c_add.input_amount(input_amount)

    if kwargs.get("save", False):
        c_add.click_save_button()

    return result

# ======================================================================================================================

def check_cashout_flow(driver, **kwargs):
    c_add = CashoutAdd(driver)
    c_add.element_visible()

    cashout_number = kwargs.get("cashout_number")
    if cashout_number:
        c_add.check_cashout_row(cashout_number)

    if kwargs.get("close", False):
        c_add.click_close_button()

# ======================================================================================================================

def view_flow(driver, **kwargs):
    c_view = CashoutView(driver)
    c_view.element_visible()

    item_name = kwargs.get("item_name")
    if item_name:
        c_view.click_navbar_items(item_name)

    if kwargs.get("close", False):
        c_view.click_close_button()

# ======================================================================================================================

def check_main_view_flow(driver, **kwargs):
    cashout_number = kwargs.get("cashout_number")
    cash_register_name = kwargs.get("cash_register_name")
    current_date = kwargs.get("current_date")
    payment_type_name = kwargs.get("payment_type_name")
    get_balance = kwargs.get("get_balance")
    supplier_name = kwargs.get("supplier_name")

    c_view = CashoutView(driver)
    c_view.element_visible()

    # get_cashout_number = c_view.get_input_value(input_name="Номер оплаты")
    # assert get_cashout_number == cashout_number

    get_currency = c_view.get_input_value(input_name="Валюта")
    assert get_currency == "Узбекский сум"

    get_cash_register = c_view.get_input_value(input_name="Касса")
    assert get_cash_register == cash_register_name

    get_current_date = c_view.get_input_value(input_name="Время")
    assert current_date in get_current_date

    get_payment_type = c_view.get_input_value(input_name="Тип оплат")
    assert get_payment_type == payment_type_name

    get_total_amount = c_view.get_input_value(input_name="Сумма", clean=True)
    assert get_total_amount == get_balance

    get_supplier = c_view.get_input_value(input_name="Поставщик")
    assert get_supplier == supplier_name

# ======================================================================================================================

def check_audit_view_flow(driver, **kwargs):
    c_view = CashoutView(driver)
    c_view.element_visible()

    column_name = kwargs.get("column_name")
    if column_name:
        c_view.check_audits(column_name)

# ======================================================================================================================

def check_transaction_flow(driver):
    base_page = BasePage(driver)
    base_page.switch_window(direction="prepare")
    c_list = CashoutList(driver)
    c_list.click_transaction_button()
    base_page.switch_window(direction="forward")
    c_list.check_transaction_body(timeout=20)
    base_page.switch_window(direction="back")

# ======================================================================================================================