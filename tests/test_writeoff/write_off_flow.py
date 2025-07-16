import time
from autotest.anor.mkw.balance.balance_list.balance_list import BalanceList
from autotest.anor.mkw.writeoff.writeoff_add import WriteOffAdd
from autotest.anor.mkw.writeoff.writeoff_expense import WriteOffExpense
from autotest.anor.mkw.writeoff.writeoff_list import WriteOffList
from autotest.anor.mkw.writeoff.writeoff_view import WriteOffView
from autotest.core.md.base_page import BasePage

# ======================================================================================================================

def list_flow(driver, **kwargs):
    add = kwargs.get("add")
    find_row = kwargs.get("find_row")
    view = kwargs.get("view")
    change_status = kwargs.get("change_status")
    expense = kwargs.get("expense")

    write_off_list = WriteOffList(driver)
    write_off_list.element_visible()

    if add:
        write_off_list.click_add_button()
    if find_row:
        write_off_list.find_row(find_row)
    if view:
        write_off_list.click_view_button()
    if change_status:
        write_off_list.click_change_status_button(status_name=change_status)
    if expense:
        write_off_list.click_expense_button()

# ======================================================================================================================

def add_flow(driver, **kwargs):
    write_off_number = kwargs.get("write_off_number")
    warehouse_name = kwargs.get("warehouse_name")
    reason_name = kwargs.get("reason_name")
    select = kwargs.get("select", False)

    write_off_add = WriteOffAdd(driver)
    write_off_add.element_visible()

    if select:
        write_off_add.element_visible_product()
        write_off_add.click_save_button()
        return

    write_off_add.input_write_off_number(write_off_number)
    get_data_input_value = write_off_add.get_data_input_value()
    write_off_add.input_warehouses(warehouse_name)
    write_off_add.input_reasons(reason_name)
    return get_data_input_value

# ======================================================================================================================

def select_flow(driver, **kwargs):
    product_name = kwargs.get("product_name")
    product_quantity = kwargs.get("product_quantity")

    write_off_add = WriteOffAdd(driver)
    write_off_add.click_select_button()
    write_off_add.element_visible_select()
    write_off_add.input_search(product_name)
    write_off_add.input_quantity(product_quantity)
    write_off_add.click_move_one_button()
    write_off_add.click_close_button()

# ======================================================================================================================

def view_flow(driver, **kwargs):
    navbar_name = kwargs.get("navbar_name")
    currency_name = kwargs.get("currency_name")
    warehouse_name = kwargs.get("warehouse_name")
    reason_name = kwargs.get("reason_name")

    write_off_view = WriteOffView(driver)
    write_off_view.element_visible()

    write_off_view.click_navbar_button(navbar_name)

    if navbar_name=="Основная информация":
        get_currency = write_off_view.get_input_value(input_name="Валюта")
        assert get_currency == currency_name
        get_warehouse = write_off_view.get_input_value(input_name="Склад")
        assert get_warehouse == warehouse_name
        get_reason = write_off_view.get_input_value(input_name="Причина списания")
        assert get_reason == reason_name

    if navbar_name == "Расходы":
        write_off_view.input_search(search_name="Прочие операционные расходы")
        write_off_view.check_expenses(expense_name="Прочие операционные расходы")

    write_off_view.click_close_button()

# ======================================================================================================================

def get_balance_flow(driver, **kwargs):
    warehouse_name = kwargs.get("warehouse_name")
    product_name = kwargs.get("product_name")

    base_page = BasePage(driver)
    base_page.switch_window(direction="prepare")
    cut_url = base_page.cut_url()
    base_page.switch_window(direction="new", url=cut_url + 'anor/mkw/balance/balance_list')

    balance_list = BalanceList(driver)
    balance_list.element_visible()
    balance_list.click_reload_button()
    get_balance = balance_list.get_balance(warehouse_name, product_name)
    base_page.logger.info(f"get_balance: {get_balance}")
    base_page.switch_window(direction="prepare")
    base_page.switch_window(direction="back")
    return get_balance

# ======================================================================================================================

def check_transaction_flow(driver):
    base_page = BasePage(driver)
    base_page.switch_window(direction="prepare")
    write_off_list = WriteOffList(driver)
    write_off_list.click_transaction_button()
    base_page.switch_window(direction="forward")
    write_off_list.check_transaction_body(timeout=20)
    base_page.switch_window(direction="back")

# ======================================================================================================================

def expense_flow(driver, **kwargs):
    write_off_number = kwargs.get("write_off_number")
    warehouse_name = kwargs.get("warehouse_name")
    total_sum = kwargs.get("total_sum")
    get_data_input_value = kwargs.get("get_data_input_value")
    expense_article_name = kwargs.get("expense_article_name")

    write_off_expense = WriteOffExpense(driver)
    write_off_expense.element_visible()

    get_write_off_number = write_off_expense.get_input_value(input_name="Номер")
    assert int(get_write_off_number) == write_off_number

    get_currency = write_off_expense.get_input_value(input_name="Валюта")
    assert get_currency == "Узбекский сум"

    get_warehouse = write_off_expense.get_input_value(input_name="Склад")
    assert get_warehouse == warehouse_name

    get_summa = write_off_expense.get_input_value(input_name="Сумма")
    get_summa = int(get_summa.replace(' ',''))
    assert get_summa == total_sum

    get_data = write_off_expense.get_input_value(input_name="Дата")
    assert get_data == get_data_input_value

    get_reason = write_off_expense.get_input_value(input_name="Причина списания")
    assert get_reason == "Контрольная проверка"

    write_off_expense.input_corr_templates(corr_template_name="Прочие операционные расходы")
    write_off_expense.input_origins(origin_name=expense_article_name)
    write_off_expense.input_expense_amount(expense_amount=get_summa)

    get_input_currency = write_off_expense.get_input_currencies()
    assert get_input_currency == "Узбекский сум"

    time.sleep(2)
    write_off_expense.click_complete_button()

# ======================================================================================================================
