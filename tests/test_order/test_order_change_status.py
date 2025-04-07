import pytest
from autotest.anor.mdeal.order.order_view.order_view import OrderView
from autotest.core.md.base_page import BasePage
from autotest.trade.tdeal.order.order_list.orders_page import OrdersList
from tests.test_base.test_base import login_user
from utils.driver_setup import driver
from tests.conftest import test_data


def order_change_status(driver, test_data, client_name=None,
                        draft=False, new=False, processing=False, pending=False,
                        shipped=False, delivered=False, archive=False, cancelled=False):
    # Test data
    base_page = BasePage(driver)
    order_list = OrdersList(driver)
    order_view = OrderView(driver)

    data = test_data["data"]
    client_name = client_name or data["client_name"]

    try:
        login_user(driver, test_data, url='trade/tdeal/order/order_list')

        if draft:  # Draft
            assert order_list.element_visible(), 'OrdersList not open!'
            order_list.find_row(client_name)
            order_list.click_view_button()

            assert order_view.element_visible(), 'OrderView not open!'
            order_id = order_view.check_order_id()
            base_page.logger.info(f"Order id: {order_id}")
            text = order_view.check_status()
            base_page.logger.info(f"Order status name: {text}")
            assert text == data["Draft"], f'{text} != {data["Draft"]}'
            draft_quantity, draft_price, draft_sum = order_view.check_items()
            order_view.click_close_button()
        # ------------------------------------------------------------------------------------------------------------------

        if new:  # New
            assert order_list.element_visible(), 'OrdersList not open after Draft!'
            order_list.click_change_status_button(data["New"])
            order_list.find_row(client_name)
            order_list.click_view_button()

            assert order_view.element_visible(), 'OrderView not open after New!'
            text = order_view.check_status()
            assert text == data["New"], f'{text} != {data["New"]}'
            new_quantity, new_price, new_sum = order_view.check_items()
            assert draft_quantity == new_quantity, f'Error: draft_quantity: {draft_quantity} != new_quantity: {new_quantity}'
            assert draft_price == new_price, f'Error: draft_price: {draft_price} != new_price: {new_price}'
            order_view.click_close_button()
        # ------------------------------------------------------------------------------------------------------------------

        if processing:  # Processing
            assert order_list.element_visible(), 'OrdersList not open after New!'
            order_list.click_change_status_button(data["Processing"])
            order_list.find_row(client_name)
            order_list.click_view_button()

            assert order_view.element_visible(), 'OrderView not open after Processing!'
            text = order_view.check_status()
            assert text == data["Processing"], f'{text} != {data["Processing"]}'
            processing_quantity, processing_price, processing_sum = order_view.check_items()
            assert draft_quantity == processing_quantity, f'Error: draft_quantity: {draft_quantity} != processing_quantity: {processing_quantity}'
            assert draft_price == processing_price, f'Error: draft_price: {draft_price} != processing_price: {processing_price}'
            order_view.click_close_button()
        # ------------------------------------------------------------------------------------------------------------------

        if pending:  # Pending
            assert order_list.element_visible(), 'OrdersList not open after Processing!'
            order_list.click_change_status_button(data["Pending"])
            order_list.find_row(client_name)
            order_list.click_view_button()

            assert order_view.element_visible(), 'OrderView not open after Pending!'
            text = order_view.check_status()
            assert text == data["Pending"], f'{text} != {data["Pending"]}'
            pending_quantity, pending_price, pending_sum = order_view.check_items()
            assert draft_quantity == pending_quantity, f'Error: draft_quantity: {draft_quantity} != pending_quantity: {pending_quantity}'
            assert draft_price == pending_price, f'Error: draft_price: {draft_price} != pending_price: {pending_price}'
            order_view.click_close_button()
        # ------------------------------------------------------------------------------------------------------------------

        if shipped:  # Shipped
            assert order_list.element_visible(), 'OrdersList not open after Pending!'
            order_list.click_change_status_button(data["Shipped"])
            order_list.find_row(client_name)
            order_list.click_view_button()

            assert order_view.element_visible(), 'OrderView not open after Shipped!'
            text = order_view.check_status()
            assert text == data["Shipped"], f'{text} != {data["Shipped"]}'
            shipped_quantity, shipped_price, shipped_sum = order_view.check_items()
            assert draft_quantity == shipped_quantity, f'Error: draft_quantity: {draft_quantity} != shipped_quantity: {shipped_quantity}'
            assert draft_price == shipped_price, f'Error: draft_price: {draft_price} != shipped_price: {shipped_price}'
            order_view.click_close_button()
        # ------------------------------------------------------------------------------------------------------------------

        if delivered:  # Delivered
            assert order_list.element_visible(), 'OrdersList not open after Shipped!'
            order_list.click_change_status_button(data["Delivered"])
            order_list.find_row(client_name)
            order_list.click_view_button()

            assert order_view.element_visible(), 'OrderView not open after Delivered!'
            text = order_view.check_status()
            assert text == data["Delivered"], f'{text} != {data["Delivered"]}'
            delivered_quantity, delivered_price, delivered_sum = order_view.check_items()
            assert draft_quantity == delivered_quantity, f'Error: draft_quantity: {draft_quantity} != delivered_quantity: {delivered_quantity}'
            assert draft_price == delivered_price, f'Error: draft_price: {draft_price} != delivered_price: {delivered_price}'
            order_view.click_close_button()
        # ------------------------------------------------------------------------------------------------------------------

        if archive:  # Archive
            assert order_list.element_visible(), f"OrdersList not open after 'Delivered'!"
            order_list.click_change_status_button(data["Archive"])
            assert order_list.element_visible(), 'OrdersList not open after Archive!'
        # ------------------------------------------------------------------------------------------------------------------

        if cancelled:  # Cancelled
            assert order_list.element_visible(), 'OrdersList not open after Draft!'
            order_list.click_change_status_button(data["Cancelled"])
            assert order_list.element_visible(), 'OrdersList not open after Cancelled!'

        base_page.logger.info(f"✅Test end: order_change_status")

    except AssertionError as ae:
        base_page.logger.error(f'Assertion error: {str(ae)}')
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        pytest.fail(str(e))


def test_change_status_from_draft_to_archive(driver, test_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️Test run: test_change_status_from_draft_to_archive")
    data = test_data["data"]
    client_name = f"{data['client_name']}-A"
    order_change_status(driver, test_data, client_name=client_name,
                        draft=True, new=True, processing=True, pending=True,
                        shipped=True, delivered=True, archive=True, cancelled=False)


def test_change_status_draft_and_archive(driver, test_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️Test run: test_change_status_draft_and_archive")
    data = test_data["data"]
    client_name = f"{data['client_name']}-B"
    order_change_status(driver, test_data, client_name=client_name, draft=True, archive=True, cancelled=False)


def test_change_status_draft_and_cancelled(driver, test_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️Test run: test_change_status_draft_and_cancelled")
    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    order_change_status(driver, test_data, client_name=client_name, draft=True, cancelled=True)


def test_change_status_draft_and_delivered(driver, test_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️Test run: test_change_status_draft_and_delivered")
    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    order_change_status(driver, test_data, client_name=client_name, draft=True, delivered=True, cancelled=False)
