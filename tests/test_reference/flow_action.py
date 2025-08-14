from autotest.anor.mcg.action_add.action_add import ActionAdd
from autotest.anor.mcg.action_list.action_list import ActionList
from autotest.anor.mcg.action_view.action_view import ActionIdView

# ======================================================================================================================

def list_flow(driver, **kwargs):
    action_list = ActionList(driver)
    action_list.element_visible()

    if kwargs.get("add"):
        action_list.click_add_button()

    find_row = kwargs.get("find_row")
    if find_row:
        action_list.find_row(find_row)

    if kwargs.get("view"):
        action_list.click_view_button()

# ======================================================================================================================

def add_flow(driver, **kwargs):
    action_add = ActionAdd(driver)
    action_add.element_visible()

    action_name = kwargs.get("action_name")
    if action_name:
        action_add.input_name(action_name)

    room_name = kwargs.get("room_name")
    if room_name:
        action_add.input_room(room_name)

    warehouse_name = kwargs.get("warehouse_name")
    if warehouse_name:
        action_add.input_bonus_warehouse(warehouse_name)

    payment_type_name = kwargs.get("payment_type_name")
    if payment_type_name:
        action_add.input_payment_type(payment_type_name)

    if kwargs.get("required_state"):
        action_add.input_required()

    if kwargs.get("next_step", False):
        action_add.click_step_button()
        return

    product_name = kwargs.get("product_name")
    if product_name:
        action_add.input_product_name(product_name)

    product_quantity = kwargs.get("product_quantity")
    if product_quantity:
        action_add.input_product_quantity(product_quantity)

    bonus_product_name = kwargs.get("bonus_product_name")
    if bonus_product_name:
        action_add.input_bonus_product(bonus_product_name)

    bonus_product_quantity = kwargs.get("bonus_product_quantity")
    if bonus_product_quantity:
        action_add.input_bonus_product_quantity(bonus_product_quantity)

    kind_name = kwargs.get("kind_name")
    if kind_name:
        action_add.input_bonus_kind(kind_name)

    if kwargs.get("save", True):
        action_add.click_save_button()

# ======================================================================================================================

def view_flow(driver, assertions, **kwargs):
    action_view = ActionIdView(driver)
    action_view.element_visible()

    action_name = kwargs.get("action_name")

    if action_name:
        get_action_name = action_view.get_elements()
        assertions.assert_equals(get_action_name, action_name)

    close = kwargs.get("close", True)

    if close:
        action_view.click_close_button()

# ======================================================================================================================
