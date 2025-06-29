from autotest.anor.mdeal.return_.return_add.return_add import ReturnAdd
from autotest.anor.mdeal.return_.return_list.return_list import ReturnList
from autotest.anor.mdeal.return_.return_view.return_view import ReturnView
from autotest.anor.mkw.balance.balance_list.balance_list import BalanceList
from autotest.core.md.base_page import BasePage
from flows.auth_flow import login_user


def test_return(driver, test_data):
    # Log
    data = test_data["data"]
    room_name = data["room_name"]
    robot_name = data["robot_name"]
    warehouse_name = data["warehouse_name"]
    client_name = f"{data['client_name']}-A"
    currency_name = "Узбекский сум"
    product_name = data["product_name"]
    product_quantity = 10
    product_price = data["product_price"]
    percent_value = data["percent_value"]
    payment_type_name = data["payment_type_name"]

    login_user(driver, test_data, url='anor/mdeal/return/return_list')

    # List
    return_list = ReturnList(driver)
    return_list.element_visible()
    return_list.click_add_button()

    # Add
    return_add = ReturnAdd(driver)
    return_add.element_visible()
    return_add.input_room(room_name)
    return_add.input_robot(robot_name)
    return_add.input_warehouse(warehouse_name)
    return_add.input_persons(client_name)
    return_add.input_currencies(currency_name)
    return_add.click_next_step_button()

    # Add: 2
    return_add.input_inventory_products(product_name)
    return_add.input_inventory_quantity(product_quantity)
    return_add.input_inventory_price(product_price)
    return_add.click_margin_value()
    return_add.click_next_step_button()

    # Add: 3
    return_add.input_payment_types(payment_type_name)
    return_add.click_next_step_button()

    # Add: 4
    return_add.input_status(status=3)
    return_add.click_next_step_button(save_button=True)

    # List
    return_list.element_visible()
    return_list.find_row(client_name)
    return_list.click_view_button()

    # View
    return_view = ReturnView(driver)
    return_view.element_visible()
    get_quantity, get_margin, get_total_sum = return_view.check_items()
    assert get_quantity == product_quantity, f"{get_quantity} != {product_quantity}"
    total_sum = (product_quantity * product_price) - ((product_quantity * product_price) * (percent_value / 100))
    assert get_total_sum == total_sum, f"{get_total_sum} != {total_sum}"
    return_view.click_close_button()

    # List
    return_list.element_visible()
    return_list.find_row(client_name)
    return_list.click_draft_one_button()
    return_list.element_visible()
    return_list.find_row(client_name)
    return_list.click_delete_one_button()
    return_list.element_visible()


def test_return_id(driver, test_data):
    base_page = BasePage(driver)

    # Log
    data = test_data["data"]
    warehouse_name = data["warehouse_name"]
    sub_filial_name = data["sub_filial_name"]
    client_name = f"{data['client_name']}-A"
    product_name = data["product_name"]
    product_quantity = 10
    product_price = data["product_price"] + 2000
    payment_type_name = data["payment_type_name"]
    expeditor_name = data["natural_person_name"]
    contract_name = f"{data['contract_name']}-A-UZB"
    text = ("test - " * 30).strip()

    login_user(driver, test_data, url='anor/mdeal/return/return_list')

    # List
    return_list = ReturnList(driver)
    return_list.element_visible()
    return_list.click_add_button()

    # Add
    return_add = ReturnAdd(driver)
    return_add.element_visible()
    return_add.input_order_deals(client_name)
    return_add.input_warehouse(warehouse_name)
    return_add.input_sub_filial(sub_filial_name)
    return_add.click_next_step_button()

    # Add: 2
    return_add.input_inventory_price(product_price)
    return_add.click_next_step_button()

    # Add: 3
    return_add.input_payment_types(payment_type_name)
    return_add.input_expeditors(expeditor_name)
    return_add.input_contracts(contract_name)
    return_add.input_note(text)
    return_add.click_next_step_button()

    # Add: 4
    return_add.input_status()
    return_add.click_next_step_button(save_button=True)

    # List
    return_list.element_visible()
    return_list.find_row(client_name)
    return_list.click_view_button()

    # View
    return_view = ReturnView(driver)
    return_view.element_visible()
    get_quantity, get_margin, get_total_sum = return_view.check_items()
    assert get_quantity == product_quantity, f"{get_quantity} != {product_quantity}"
    total_sum = (product_quantity * product_price) - 20000
    assert get_total_sum == total_sum, f"{get_total_sum} != {total_sum}"
    return_view.click_close_button()

    # List
    return_list.element_visible()
    return_list.find_row(client_name)
    return_list.click_shipped_one_button()
    return_list.element_visible()
    return_list.find_row(client_name)
    return_list.click_archive_one_button()
    return_list.element_visible()

    # Open Balance List
    base_page.switch_window(direction="prepare")
    cut_url = base_page.cut_url()
    base_page.switch_window(direction="new", url=cut_url + 'anor/mkw/balance/balance_list')

    balance_list = BalanceList(driver)
    balance_list.element_visible()
    balance_list.click_reload_button()
    balance_list.find_row(product_name)
    balance_list.click_detail_button()
    balance_list.click_reload_button()
    balance = balance_list.check_balance_quantity()
    assert balance == product_quantity, f"Error: Balance: '{balance}' != product_quantity: '{product_quantity}'"

    base_page.switch_window(direction="back")
    base_page.refresh_page()

    return_list.find_row(client_name)
    return_list.click_draft_one_button()
    return_list.element_visible()
    return_list.find_row(client_name)
    return_list.click_delete_one_button()
    return_list.element_visible()