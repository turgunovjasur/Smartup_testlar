from autotest.anor.mkw.stocktaking.stocktaking_add import StocktakingAdd
from autotest.anor.mkw.stocktaking.stocktaking_complete import StocktakingComplete
from autotest.anor.mkw.stocktaking.stocktaking_list import StocktakingList
from autotest.anor.mkw.stocktaking.stocktaking_select import StocktakingSelect
from autotest.anor.mkw.stocktaking.stocktaking_view import StocktakingView
from autotest.core.md.base_page import BasePage

# ======================================================================================================================

def list_flow(driver, **kwargs):
    add = kwargs.get("add")
    find_row = kwargs.get("find_row")
    edit = kwargs.get("edit")
    view = kwargs.get("view")
    complete = kwargs.get("complete")

    s_list = StocktakingList(driver)
    s_list.element_visible()

    if add:
        s_list.click_add_button()
    if find_row:
        s_list.find_row(find_row)
    if edit:
        s_list.click_edit_button()
    if view:
        s_list.click_view_button()
    if complete:
        s_list.click_complete_button()

# ======================================================================================================================

def add_flow(driver, **kwargs):
    stocktaking_number = kwargs.get("stocktaking_number")
    warehouse_name = kwargs.get("warehouse_name")
    reason_name = kwargs.get("reason_name")
    note_name = kwargs.get("note_name")
    get_data = kwargs.get("get_data")

    result = {}

    add = StocktakingAdd(driver)
    add.element_visible()
    add.input_stocktaking_number(stocktaking_number)
    add.input_warehouses(warehouse_name)
    add.input_reasons(reason_name)
    add.input_note(note_name)

    result["get_data"] = add.get_input_value(input_name=get_data)

    get_currency = add.get_input_value(input_name="Валюта")
    assert get_currency == "Узбекский сум", f'{get_currency} != "Узбекский сум"'

    return result

# ======================================================================================================================

def select_flow(driver, **kwargs):
    product_name = kwargs.get("product_name")

    select = StocktakingSelect(driver)
    select.element_visible_select()
    select.input_search(product_name)
    get_value = select.get_value_by_column_name(column_name="Остаток")
    select.input_row_quant(product_row_quant=int(get_value) - 5)
    select.click_move_one_button()
    select.click_close_button()

# ======================================================================================================================

def add_product_flow(driver, **kwargs):
    product_name = kwargs.get("product_name")
    product_item_quant = kwargs.get("product_item_quant")
    product_item_income_price = kwargs.get("product_item_income_price")

    add = StocktakingAdd(driver)
    add.element_visible()
    add.input_product(product_name)
    add.input_item_quant(product_item_quant)
    add.input_item_income_price(product_item_income_price)
    add.click_save_button()

# ======================================================================================================================

def edit_flow(driver, **kwargs):
    stocktaking_number = kwargs.get("stocktaking_number")
    warehouse_name = kwargs.get("warehouse_name")

    add = StocktakingAdd(driver)
    add.element_visible()

    get_number = add.get_input_value(input_name="Номер")
    assert int(get_number) == stocktaking_number, f'{int(get_number)} != {stocktaking_number}'

    get_warehouse = add.get_input_value(input_name="Склад")
    assert get_warehouse == warehouse_name, f'{get_warehouse} != {warehouse_name}'

    get_currency = add.get_input_value(input_name="Валюта")
    assert get_currency == "Узбекский сум", f'{get_currency} != "Узбекский сум"'

    get_reason = add.get_input_value(input_name="Причина инвентаризации")
    assert get_reason == "Контрольная проверка", f'{get_reason} != "Контрольная проверка"'

    get_nota = add.get_input_value(input_name="Примечание")
    assert get_nota == "TEST_TEXT", f'{get_nota} != "TEST_TEXT"'

    add.click_save_button(post=True)

# ======================================================================================================================

def view_flow(driver, **kwargs):
    navbar_name = kwargs.get("navbar_name")
    warehouse_name = kwargs.get("warehouse_name")
    sum_excess = kwargs.get("sum_excess")
    sum_minority = kwargs.get("sum_minority")
    data_creation = kwargs.get("data_creation")
    search_name = kwargs.get("search_name")
    product_name = kwargs.get("product_name")

    view = StocktakingView(driver)
    view.element_visible()

    if navbar_name == "Основная информация":
        view.click_navbar_button(navbar_name)
        get_warehouse = view.get_input_value(input_name="Склад")
        assert get_warehouse == warehouse_name, f"Error: {get_warehouse} != {warehouse_name}"
        get_currency = view.get_input_value(input_name="Валюта")
        assert get_currency == "Узбекский сум", f"Error: {get_currency} != 'Узбекский сум'"
        get_reason = view.get_input_value(input_name="Причина инвентаризации")
        assert get_reason == "Контрольная проверка", f"Error: {get_reason} != 'Контрольная проверка'"
        get_nota = view.get_input_value(input_name="Примечание")
        assert get_nota == "TEST_TEXT", f"Error: {get_nota} != 'TEST_TEXT'"
        get_sum_excess = view.get_input_value(input_name="Сумма излишков", clean=True)
        assert int(get_sum_excess) == sum_excess, f"Error: {int(get_sum_excess)} != {sum_excess}"
        get_sum_minority = view.get_input_value(input_name="Сумма недостач", clean=True)
        assert int(get_sum_minority) == sum_minority, f"Error: {int(get_sum_minority)} != {sum_minority}"
        get_data_creation = view.get_input_value(input_name="Дата создания")
        assert data_creation in get_data_creation, f"Error: {data_creation} in {get_data_creation}"

    if navbar_name == "ТМЦ":
        view.click_navbar_button(navbar_name)
        view.input_search(search_name)
        view.check_product(product_name)

        view.click_navbar_button(navbar_name="Распределение расходов")
        view.check_corr(templates_name="Прочие операционные доходы")
        view.check_corr(templates_name="Прочие операционные расходы")

    view.click_close_button()

# ======================================================================================================================

def check_transaction_flow(driver):
    base_page = BasePage(driver)
    base_page.switch_window(direction="prepare")
    s_list = StocktakingList(driver)
    s_list.click_transaction_button()
    base_page.switch_window(direction="forward")
    s_list.check_transaction_body(timeout=20)
    base_page.switch_window(direction="back")

# ======================================================================================================================

def complete_flow(driver, **kwargs):
    stocktaking_number = kwargs.get("stocktaking_number")
    data = kwargs.get("data")
    warehouse_name = kwargs.get("warehouse_name")
    sum_excess = kwargs.get("sum_excess")
    sum_minority = kwargs.get("sum_minority")

    complete = StocktakingComplete(driver)
    complete.element_visible()

    get_stocktaking_number = complete.get_input_value(input_name="Номер")
    assert int(get_stocktaking_number) == stocktaking_number, f"{get_stocktaking_number} != {stocktaking_number}"

    get_data = complete.get_input_value(input_name="Дата")
    assert get_data == data, f"{get_data} != {data}"

    get_warehouse = complete.get_input_value(input_name="Склад")
    assert get_warehouse == warehouse_name, f"{get_warehouse} != {warehouse_name}"

    get_nota = complete.get_input_value(input_name="Примечание")
    assert get_nota == "TEST_TEXT", f"{get_nota} != 'TEST_TEXT'"

    get_currency = complete.get_input_value(input_name="Валюта")
    assert get_currency == "Узбекский сум", f"{get_currency} != {'Узбекский сум'}"

    get_sum_excess = complete.get_input_value(input_name="Сумма излишков в базовой валюте", clean=True)
    assert int(get_sum_excess) == sum_excess, f"{get_sum_excess} != {sum_excess}"

    get_sum_minority = complete.get_input_value(input_name="Сумма недостач в базовой валюте", clean=True)
    assert int(get_sum_minority) == sum_minority, f"{get_sum_minority} != {sum_minority}"

    complete.click_movements_button()
    complete.input_templates(template_name="Прочие операционные доходы", index=1)
    complete.input_amount(product_amount=sum_excess, index=1)

    complete.click_add_template_button()
    complete.click_corr_kind_radio_button()

    complete.input_templates(template_name="Прочие операционные расходы", index=2)
    complete.input_amount(product_amount=get_sum_minority, index=2)

    complete.click_finish_button()

# ======================================================================================================================
