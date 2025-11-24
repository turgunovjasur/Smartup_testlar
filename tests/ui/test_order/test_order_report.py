import os
import time
import pytest
from pages.core.md.base_page import BasePage
from pages.trade.rep.mbi.tdeal.order.sales_report_constructor import SalesReportConstructor
from flows.auth_flow import login_user
from pages.trade.tdeal.order.order_list.orders_list import OrdersList
from utils.download_manager import clear_old_download, generate_and_verify_download, DOWNLOAD_DIR

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_D
@pytest.mark.order(460)
def test_check_invoice_report_for_order_list(driver, test_data):
    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    invoice_report_name = data["template_name"]

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_list = OrdersList(driver)
    order_list.element_visible()
    order_list.find_row(client_name)

    base_page = BasePage(driver)
    clear_old_download(base_page, expected_name="Test_invoice_report", file_type="xlsx")
    before_files = set(os.listdir(DOWNLOAD_DIR))
    order_list.click_invoice_reports_all_button(invoice_report_name)
    generate_and_verify_download(base_page, before_files=before_files, expected_name="Test_invoice_report", file_type="xlsx")

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_A
@pytest.mark.order(290)
def test_sales_report_constructor(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_sales_report_constructor")

    login_user(driver, test_data, url='trade/rep/mbi/tdeal/order')

    sales_report_constructor = SalesReportConstructor(driver)
    sales_report_constructor.input_search_option(option_name="Заказ")

    sales_report_constructor.click_source_and_target(option_name="Заказ", field_name="row")

    sales_report_constructor.input_filter_fields(option_name="Статус", clear=True)

    sales_report_constructor.click_view_button()

    sales_report_constructor.switch_to_iframe()
    order_ids = sales_report_constructor.get_order_id_list()

    base_page.logger.info(f"order_ids: {order_ids}")

    order_id_1 = load_data("order_id_1")
    order_id_2 = load_data("order_id_2")

    assert order_id_1 in order_ids, f"Error: {order_id_1} not found!"
    assert order_id_2 in order_ids, f"Error: {order_id_2} not found!"

    time.sleep(2)

# ======================================================================================================================
