from pages.anor.mkw.input.input_add.input_add import InputAdd
from pages.anor.mkw.input.input_list.input_list import InputList
from pages.anor.mkw.input.input_view.input_view import InputView
from pages.core.md.base_page import BasePage

# ======================================================================================================================

def list_flow(driver, **kwargs):
    input_list = InputList(driver)
    input_list.element_visible()

    if kwargs.get("add"):
        input_list.click_add_button()

    find_row = kwargs.get("find_row")
    if find_row:
        input_list.find_row(input_number=find_row)

    if kwargs.get("view"):
        input_list.click_view_button()

    if kwargs.get("status"):
        input_list.click_change_status_button()

# ======================================================================================================================

def add_flow(driver, **kwargs):
    input_add = InputAdd(driver)
    input_add.element_visible()

    input_number = kwargs.get("input_number")
    if input_number:
        input_add.input_number(input_number)

    warehouse_name = kwargs.get("warehouse_name")
    if warehouse_name:
        input_add.input_warehouse(warehouse_name)

    extra_cost_checkbox = kwargs.get("extra_cost_checkbox")
    if extra_cost_checkbox:
        input_add.click_extra_cost_checkbox()

    purchase_number = kwargs.get("purchase_number")
    if purchase_number:
        input_add.input_purchase(purchase_number)

    purchase_quantity = kwargs.get("purchase_quantity")
    if purchase_quantity:
        input_add.input_quantity(purchase_quantity)

    add_extra_cost = kwargs.get("add_extra_cost")
    if add_extra_cost:
        input_add.input_extra_cost()

    calc_extra_cost = kwargs.get("calc_extra_cost")
    if calc_extra_cost:
        input_add.click_distribute_extra_cost_button()

    if kwargs.get("next_step", True):
        input_add.click_next_step(save=kwargs.get("save", False))

# ======================================================================================================================

def view_flow(driver, **kwargs):
    input_add = InputView(driver)
    input_add.element_visible()

    input_number = kwargs.get("check_input_number")
    if input_number:
        get_input_number = input_add.check_input_number()
        assert get_input_number == input_number, f"Error: {get_input_number} != {input_number}"

    if kwargs.get("close", True):
        input_add.click_close_button()

# ======================================================================================================================

def check_transaction(driver):
    input_list = InputList(driver)
    base_page = BasePage(driver)
    base_page.switch_window(direction="prepare")
    input_list.click_transactions_button()
    base_page.switch_window(direction="forward")
    input_list.check_transaction_body(timeout=20)
    base_page.switch_window(direction="back")

# ======================================================================================================================

def check_report(driver):
    input_list = InputList(driver)
    base_page = BasePage(driver)
    base_page.switch_window(direction="prepare")
    input_list.click_report_button()
    base_page.switch_window(direction="forward")
    input_list.check_report_body(timeout=20)
    base_page.switch_window(direction="back")

# ======================================================================================================================