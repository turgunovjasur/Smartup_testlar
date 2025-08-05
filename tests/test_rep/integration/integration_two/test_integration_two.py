import os
import pytest
from autotest.core.md.base_page import BasePage
from autotest.trade.rep.integration.integration_two.integration_two import IntegrationTwo
from flows.auth_flow import login_admin
from tests.test_rep.integration.rep_main_funksiya import generate_and_verify_download, clear_old_download, DOWNLOAD_DIR


@pytest.mark.regression
@pytest.mark.integration_report
def test_check_report_integration_two(driver, test_data):
    data = test_data["data"]
    price_type_name = data['price_type_name_UZB']
    company_id = 8605425
    user_name = 123
    url = "https"

    login_admin(driver, test_data, url='trade/rep/integration/integration_two')

    # IntegrationTwo
    integration_two = IntegrationTwo(driver)
    integration_two.element_visible()
    integration_two.click_show_setting()

    # Setting
    integration_two.element_visible_setting()
    integration_two.input_company_id(company_id)
    integration_two.input_user_name(user_name)
    integration_two.input_url(url)
    integration_two.input_price_types(price_type_name)
    integration_two.click_edit_person()
    integration_two.click_ignore_updated_deals()
    integration_two.click_show_owner_person_code()
    integration_two.click_send_all_deals()
    integration_two.click_save()
    # ------------------------------------------------------------------------------------------------------------------
    integration_two.element_visible()

    base_page = BasePage(driver)
    clear_old_download(base_page, expected_name="import_order", file_type="xml")
    before_files = set(os.listdir(DOWNLOAD_DIR))
    integration_two.click_generate()
    generate_and_verify_download(base_page, before_files=before_files, expected_name="import_order", file_type="xml")
    # ------------------------------------------------------------------------------------------------------------------
    integration_two.check_error_modal()
    integration_two.element_visible()
    integration_two.click_exchange_mode(exchange_file=2)
    integration_two.input_date()

    clear_old_download(base_page, expected_name="export_order", file_type="xml")
    before_files = set(os.listdir(DOWNLOAD_DIR))
    integration_two.click_generate()
    generate_and_verify_download(base_page, before_files=before_files, expected_name="export_order", file_type="xml")
    # ------------------------------------------------------------------------------------------------------------------
    integration_two.check_error_modal()
    integration_two.element_visible()
    integration_two.click_exchange_mode(exchange_file=3)

    clear_old_download(base_page, expected_name="import_order_status", file_type="xml")
    before_files = set(os.listdir(DOWNLOAD_DIR))
    integration_two.click_generate()
    generate_and_verify_download(base_page, before_files=before_files, expected_name="import_order_status", file_type="xml")
    # ------------------------------------------------------------------------------------------------------------------
    # integration_two.check_error_modal()
    # assert integration_two.element_visible(), "IntegrationTwo not open after export_status!"
    # integration_two.click_exchange_mode(exchange_file=4)
    # integration_two.input_date()
    # integration_two.click_generate()
    # generate_and_verify_download(driver, file_name='export_balance', file_type='xml')
    # ------------------------------------------------------------------------------------------------------------------
    integration_two.check_error_modal()
    integration_two.element_visible()
    integration_two.click_exchange_mode(exchange_file=5)
    integration_two.input_date()

    clear_old_download(base_page, expected_name="export_input", file_type="xml")
    before_files = set(os.listdir(DOWNLOAD_DIR))
    integration_two.click_generate()
    generate_and_verify_download(base_page, before_files=before_files, expected_name="export_input", file_type="xml")
    integration_two.check_error_modal()
    integration_two.element_visible()
    # ------------------------------------------------------------------------------------------------------------------
