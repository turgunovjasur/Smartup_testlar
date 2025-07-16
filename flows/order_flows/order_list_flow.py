from autotest.anor.mdeal.order.order_view.order_view import OrderView
from autotest.anor.mkw.product_file_list.product_file_list import ProductFileList
from autotest.core.md.base_page import BasePage
from autotest.core.md.biruni.grid_setting.grid_setting import GridSetting
from autotest.trade.tdeal.order.order_attach_data.order_attach_data import OrderAttachData
from autotest.trade.tdeal.order.order_list.order_copy_modal import OrderCopyModal
from autotest.trade.tdeal.order.order_list.orders_list import OrdersList
from autotest.trade.tdeal.order.transactions.transactions import Transaction


# ======================================================================================================================

def order_list(driver, **kwargs):
    base_page = BasePage(driver)
    order_list = OrdersList(driver)
    order_list.element_visible()

    reload = kwargs.get("reload")
    find_row = kwargs.get("find_row")
    add = kwargs.get("add")
    view = kwargs.get("view")
    edit = kwargs.get("edit")
    order_return = kwargs.get("order_return")
    copy = kwargs.get("copy")
    change_status = kwargs.get("change_status")
    file = kwargs.get("file")
    transaction = kwargs.get("transaction")
    attach_data = kwargs.get("attach_data")

    if reload:
        order_list.click_reload_button()
    if find_row:
        order_list.find_row(find_row)
    if add:
        order_list.click_add_button()
    if view:
        order_list.click_view_button()
    if edit:
        order_list.click_edit_button()
    if order_return:
        order_list.click_return_button()
    if copy:
        order_list.click_copy_button()
    if change_status:
        order_list.click_change_status_button(change_status)
        order_list.element_visible()
    if file:
        order_list.click_view_dropdown(file_name='Файлы')
    if transaction:
        base_page.switch_window(direction="prepare")
        order_list.click_view_dropdown(file_name="Проводки")
        base_page.switch_window(direction="forward")
    if attach_data:
        order_list.click_edit_dropdown(file_name="Прикрепить")

# ======================================================================================================================

def order_view(driver, **kwargs):
    order_view = OrderView(driver)
    order_view.element_visible()

    input_name = kwargs.get("input_name")
    default_dtype = kwargs.get("data_type", "text")

    tablist_name = kwargs.get("tablist_name")
    consignment_day = kwargs.get("consignment_day")
    consignment_amount = kwargs.get("consignment_amount")
    consignment_empty = kwargs.get("consignment_empty", False)

    input_values = {}

    if input_name:
        # str bo‘lsa: {"Клиент": default_dtype}
        if isinstance(input_name, str):
            input_name = {input_name: default_dtype}

        # list bo‘lsa: ["Клиент", "Статус"] → {"Клиент": default_dtype, ...}
        elif isinstance(input_name, list):
            input_name = {name: default_dtype for name in input_name}

        # dict bo‘lsa: {"ИД заказа": "numeric", "Клиент": "text"} → qoldiramiz

        for name, dtype in input_name.items():
            input_values[name] = order_view.get_input_value_in_order_view(name, dtype)

    if tablist_name:
        order_view.click_tablist_button(tablist_name)

        if consignment_day and consignment_amount:
            get_consignment_amount = order_view.check_consignments(consignment_day)
            get_consignment_amount = int(get_consignment_amount.replace(" ", ""))
            assert get_consignment_amount == consignment_amount, f'Error: {get_consignment_amount} != {consignment_amount}'

        if consignment_empty:
            order_view.check_row_consignment()

    order_view.click_close_button()

    return input_values if input_values else None

# ======================================================================================================================

def order_file(driver):
        product_file_list = ProductFileList(driver)
        product_file_list.element_visible()
        product_file_list.click_close_button()

# ======================================================================================================================

def order_transaction(driver):
    base_page = BasePage(driver)
    transaction = Transaction(driver)
    transaction.check_transaction_body(timeout=20)
    base_page.switch_window(direction="back")

# ======================================================================================================================

def order_attach_data(driver):
    order_attach_data = OrderAttachData(driver)
    order_attach_data.element_visible()
    order_attach_data.click_delivery_date_checkbox(days=5)
    order_attach_data.click_save_button()

# ======================================================================================================================

def order_grid_setting(driver):
    grid_setting = GridSetting(driver)
    grid_setting.element_visible()
    grid_setting.click_save_default_button()

# ======================================================================================================================

def order_copy(driver, copy_client_name):
    order_copy_modal = OrderCopyModal(driver)
    order_copy_modal.element_visible_copy_title()
    order_copy_modal.input_persons(copy_client_name)
    order_copy_modal.click_copy_save_button()

# ======================================================================================================================

def order_search_input(driver, **kwargs):
    order_list = OrdersList(driver)
    order_list.element_visible()

    search_data = kwargs.get("search_data")
    clear = kwargs.get("clear", False)

    order_list.input_search(search_data)
    order_list.find_row(search_data)

    if clear:
        order_list.input_search(clear=True)
        order_list.click_reload_button()
        return

# ======================================================================================================================

def order_filter_panel(driver, **kwargs):
    order_list = OrdersList(driver)
    order_list.element_visible()

    open_panel = kwargs.get("open_panel", False)
    show_all = kwargs.get("show_all", False)
    state = kwargs.get("state", True)
    option_header = kwargs.get("option_header")
    option_name = kwargs.get("option_name")
    close_panel = kwargs.get("close_panel", False)

    if open_panel:
        order_list.click_filter_panel_button()

    if option_header and option_name:
        order_list.click_option_in_filter_panel(option_header, option_name, state)
        order_list.click_filter_run_button()
        order_list.element_visible()
        order_list.find_row(option_name)

    if not state:
        order_list.click_option_in_filter_panel(option_header, option_name, state)

    if show_all:
        order_list.click_show_all_button()
        order_list.find_row(option_name)

    if close_panel:
        order_list.click_close_filter_panel()
# ======================================================================================================================