import pytest
from autotest.core.md.base_page import BasePage
from flows.auth_flow import login_user
from flows.order_flows.order_list_flow import order_list, order_view

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_A
@pytest.mark.order(300)
def test_order_change_status_from_draft_to_cancelled_demo(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_order_change_status_from_draft_to_cancelled_demo")

    data = test_data["data"]

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_id_1 = load_data("order_id_1")
    order_id_2 = load_data("order_id_2")
    base_page.logger.info(f"order_id_1 = {order_id_1}, order_id_2 = {order_id_2}")

    # Status: Draft -> New
    status_name = data["New"]
    order_list(driver, find_row=order_id_2, change_status=status_name)
    order_list(driver, find_row=order_id_2, view=True)
    get_values = order_view(driver, input_name="Статус")
    assert get_values["Статус"] == status_name, f"{get_values['Статус']} != {status_name}"
    order_list(driver, reload=True)

    # Status: New -> Processing
    status_name = data["Processing"]
    order_list(driver, find_row=order_id_2, change_status=status_name)
    order_list(driver, find_row=order_id_2, view=True)
    get_values = order_view(driver, input_name="Статус")
    assert get_values["Статус"] == status_name, f"{get_values['Статус']} != {status_name}"
    order_list(driver, reload=True)

    # Status: Processing -> Pending
    status_name = data["Pending"]
    order_list(driver, find_row=order_id_2, change_status=status_name)
    order_list(driver, find_row=order_id_2, view=True)
    get_values = order_view(driver, input_name="Статус")
    assert get_values["Статус"] == status_name, f"{get_values['Статус']} != {status_name}"
    order_list(driver, reload=True)

    # Status: Pending -> Shipped
    status_name = data["Shipped"]
    order_list(driver, find_row=order_id_2, change_status=status_name)
    order_list(driver, find_row=order_id_2, view=True)
    get_values = order_view(driver, input_name="Статус")
    assert get_values["Статус"] == status_name, f"{get_values['Статус']} != {status_name}"
    order_list(driver, reload=True)

    # Status: Shipped -> Delivered
    status_name = data["Delivered"]
    order_list(driver, find_row=order_id_2, change_status=status_name)
    order_list(driver, find_row=order_id_2, view=True)
    get_values = order_view(driver, input_name="Статус")
    assert get_values["Статус"] == status_name, f"{get_values['Статус']} != {status_name}"
    order_list(driver, reload=True)

    # Status: Delivered -> Cancelled
    status_name = data["Cancelled"]
    order_list(driver, find_row=order_id_2, change_status=status_name)
    order_list(driver, reload=True)

    # Status: New -> Archive
    status_name = data["Archive"]
    order_list(driver, find_row=order_id_1, change_status=status_name)
    order_list(driver, reload=True)

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_B
@pytest.mark.order(370)
def test_change_status_draft_and_archive_demo(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_change_status_draft_and_archive_demo")

    data = test_data["data"]

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_id_3 = load_data("order_id_3")
    base_page.logger.info(f"order_id_3 = {order_id_3}")

    # Status: Check Draft
    status_name = data["Draft"]
    order_list(driver, find_row=order_id_3, view=True)
    get_values = order_view(driver, input_name="Статус")
    assert get_values["Статус"] == status_name, f"{get_values['Статус']} != {status_name}"
    order_list(driver, reload=True)

    # Status: Draft -> Archive
    status_name = data["Archive"]
    order_list(driver, find_row=order_id_3, change_status=status_name)
    order_list(driver, reload=True)

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order(470)
def test_change_status_new_and_cancelled_demo(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_change_status_new_and_cancelled_demo")

    data = test_data["data"]

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_id_5 = load_data("order_id_5")
    base_page.logger.info(f"order_id_5 = {order_id_5}")

    # Status: Check New
    status_name = data["New"]
    order_list(driver, find_row=order_id_5, view=True)
    get_values = order_view(driver, input_name="Статус")
    assert get_values["Статус"] == status_name, f"{get_values['Статус']} != {status_name}"
    order_list(driver, reload=True)

    # Status: New -> Cancelled
    status_name = data["Cancelled"]
    order_list(driver, find_row=order_id_5, change_status=status_name)
    order_list(driver, reload=True)

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order(510)
def test_change_status_draft_and_delivered_demo(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_change_status_draft_and_delivered_demo")

    data = test_data["data"]

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_id_6 = load_data("order_id_6")
    base_page.logger.info(f"order_id_6 = {order_id_6}")

    # Status: Check New
    status_name = data["New"]
    order_list(driver, find_row=order_id_6, view=True)
    get_values = order_view(driver, input_name="Статус")
    assert get_values["Статус"] == status_name, f"{get_values['Статус']} != {status_name}"
    order_list(driver, reload=True)

    # Status: New -> Delivered
    status_name = data["Delivered"]
    order_list(driver, find_row=order_id_6, change_status=status_name)
    order_list(driver, find_row=order_id_6, view=True)
    get_values = order_view(driver, input_name="Статус")
    assert get_values["Статус"] == status_name, f"{get_values['Статус']} != {status_name}"
    order_list(driver, reload=True)

# ======================================================================================================================
