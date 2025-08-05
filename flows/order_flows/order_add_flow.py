import time
from autotest.anor.mdeal.order.order_add.create_add_main import OrderAddMain
from autotest.anor.mdeal.order.order_add.order_add_final import OrderAddFinal
from autotest.anor.mdeal.order.order_add.order_add_product import OrderAddProduct
from autotest.anor.mdeal.order.order_add.order_select.order_select import OrderSelect

# ======================================================================================================================

def main_flow(driver, **kwargs):
    # --------------------------------------------------
    # get_deal_time = kwargs.get("get_deal_time")
    # get_delivery_date = kwargs.get("get_delivery_date")
    # room_name = kwargs.get("room_name")
    # robot_name = kwargs.get("robot_name")
    # client_name = kwargs.get("client_name")
    # sub_filial_name = kwargs.get("sub_filial_name")
    # contract_name = kwargs.get("contract_name")
    # --------------------------------------------------

    main_page = OrderAddMain(driver)
    main_page.element_visible()

    result = {}

    if kwargs.get("get_deal_time"):
        result["deal_time"] = main_page.input_deal_time()

    if kwargs.get("get_delivery_date"):
        result["delivery_date"] = main_page.input_delivery_date()

    if kwargs.get("room_name"):
        main_page.click_rooms_input(kwargs.get("room_name"))

    if kwargs.get("robot_name"):
        result["natural_person"] = main_page.click_robots_input(kwargs.get("robot_name"))

    if kwargs.get("client_name"):
        main_page.click_persons_input(kwargs.get("client_name"))

    if kwargs.get("sub_filial_name"):
        main_page.click_sub_filial_input(kwargs.get("sub_filial_name"))

    if kwargs.get("contract_name"):
        main_page.click_contract_input(kwargs.get("contract_name"))

    main_page.click_next_step_button()

    return result

# ======================================================================================================================

def product_flow(driver, **kwargs):
    # --------------------------------------------------
    order_grid_setting = kwargs.get("order_grid_setting", False)
    product_name = kwargs.get("product_name")
    warehouse_name = kwargs.get("warehouse_name")
    price_type_name = kwargs.get("price_type_name")
    clear_input = kwargs.get("clear_input", False)
    product_quantity = kwargs.get("product_quantity")
    margin = kwargs.get("margin")
    next_step = kwargs.get("next_step", True)
    # --------------------------------------------------

    product_page = OrderAddProduct(driver)
    product_page.element_visible()

    if order_grid_setting:
        product_page.click_setting_button()

    if product_name and warehouse_name and price_type_name:
        product_page.input_name_product(product_name, warehouse_name, price_type_name, clear_input)

    if product_quantity:
        product_page.input_quantity(product_quantity)

    if margin:
        product_page.click_percent_value_button(margin)

    if next_step:
        product_page.click_next_step_button()

# ----------------------------------------------------------------------------------------------------------------------

def product_select_flow(driver, **kwargs):

    warehouse_name = kwargs.get("warehouse_name")
    price_type_name = kwargs.get("price_type_name")
    product_quantity = kwargs.get("product_quantity")
    margin = kwargs.get("margin")

    if warehouse_name and price_type_name:

        product_page = OrderAddProduct(driver)
        product_page.click_select_button()

        order_select_modal = OrderSelect(driver)
        order_select_modal.element_visible()
        order_select_modal.input_warehouses(warehouse_name)
        order_select_modal.input_price_types(price_type_name)

        if product_quantity:
            order_select_modal.input_product_quantity(product_quantity)

        if margin:
            product_page.click_percent_value_button(margin)

        order_select_modal.input_collect_row_button()
        order_select_modal.click_close_button()

# ======================================================================================================================

def final_flow(driver, **kwargs):
    # --------------------------------------------------
    # order_grid_setting = kwargs.get("order_grid_setting")
    # payment_type_name = kwargs.get("payment_type_name")
    # prepayment_amount = kwargs.get("prepayment_amount")
    # consignment_day = kwargs.get("consignment_day")
    # consignment_amount = kwargs.get("consignment_amount")
    # status_name = kwargs.get("status_name")
    # get_total_amount = kwargs.get("get_total_amount")
    # --------------------------------------------------

    final_page = OrderAddFinal(driver)
    final_page.element_visible()

    result = {}

    if kwargs.get("order_grid_setting"):
        final_page.click_setting_button()
        return True

    if kwargs.get("payment_type_name"):
        final_page.input_payment_type(kwargs.get("payment_type_name"))

    if kwargs.get("get_total_amount"):
        result["total_amount"] = final_page.check_total_amount()

    if kwargs.get("prepayment_amount"):
        final_page.input_booked_payment_amount(kwargs.get("prepayment_amount"))

    if kwargs.get("consignment_day") and kwargs.get("consignment_amount"):
        final_page.input_consignment_date(kwargs.get("consignment_day"), kwargs.get("consignment_amount"))

    if kwargs.get("status_name"):
        final_page.input_status_2(kwargs.get("status_name"))

    if kwargs.get("save", True):
        final_page.click_save_button()
        time.sleep(2)

    return result

# ======================================================================================================================

def final_input_value_flow(driver, **kwargs):

    final_page = OrderAddFinal(driver)
    final_page.element_visible()

    if kwargs.get("client_name"):
        get_client = final_page.get_input_value(input_name="Клиент")
        assert get_client == kwargs.get("client_name"), f'{get_client} != {kwargs.get("client_name")}'

    if kwargs.get("deal_time"):
        get_deal_time = final_page.get_input_value(input_name="Дата заказа")
        assert get_deal_time == kwargs.get("deal_time"), f'{get_deal_time} != {kwargs.get("deal_time")}'

    if kwargs.get("delivery_date"):
        get_delivery_date = final_page.get_input_value(input_name="Дата отгрузки")
        assert get_delivery_date in kwargs.get("delivery_date"), f'{get_delivery_date} not in {kwargs.get("delivery_date")}'

    if kwargs.get("room_name"):
        get_room = final_page.get_input_value(input_name="Рабочая зона")
        assert get_room == kwargs.get("room_name"), f'{get_room} != {kwargs.get("room_name")}'

    if kwargs.get("robot_name"):
        get_robot = final_page.get_input_value(input_name="Штат")
        assert get_robot == kwargs.get("robot_name"), f'{get_robot} != {kwargs.get("robot_name")}'

    if kwargs.get("sub_filial_name"):
        get_sub_filial = final_page.get_input_value(input_name="Проект")
        assert get_sub_filial == kwargs.get("sub_filial_name"), f'{get_sub_filial} != {kwargs.get("sub_filial_name")}'

    if kwargs.get("contract_name"):
        get_contract = final_page.get_input_value(input_name="Договор")
        assert get_contract == kwargs.get("contract_name"), f'{get_contract} != {kwargs.get("contract_name")}'

# ======================================================================================================================

def step_flow(driver, **kwargs):
    # --------------------------------------------------
    # next_step = kwargs.get("next_step", False)
    # prev_step = kwargs.get("prev_step", False)
    # --------------------------------------------------

    product_page = OrderAddProduct(driver)
    product_page.element_visible()

    if kwargs.get("next_step", False):
        product_page.click_next_step_button()

    if kwargs.get("prev_step", False):
        product_page = OrderAddFinal(driver)
        product_page.click_prev_step_button()

# ======================================================================================================================
