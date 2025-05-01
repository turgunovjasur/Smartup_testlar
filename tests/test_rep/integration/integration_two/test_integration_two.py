import pytest
from autotest.core.md.base_page import BasePage
from autotest.trade.rep.integration.integration_two.integration_two import IntegrationTwo
from tests.test_base.test_base import login_admin
from tests.test_rep.integration.rep_main_funksiya import generate_and_verify_download
from utils.driver_setup import driver
from tests.conftest import test_data


def test_check_report_integration_two(driver, test_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Run test: test_check_report_integration_two")

    data = test_data["data"]
    price_type_name = data['price_type_name_UZB']
    company_id = 8605425
    user_name = 123
    url = "https"

    try:
        login_admin(driver, test_data, url='trade/rep/integration/integration_two')

        # IntegrationTwo
        integration_two = IntegrationTwo(driver)
        assert integration_two.element_visible(), "IntegrationTwo not open!"
        integration_two.click_show_setting()

        # Setting
        assert integration_two.element_visible_setting(), "IntegrationTwo Setting not open!"
        integration_two.input_company_id(company_id)
        integration_two.input_user_name(user_name)
        integration_two.input_url(url)
        integration_two.input_price_types(price_type_name)
        integration_two.click_edit_person()
        integration_two.click_ignore_updated_deals()
        integration_two.click_show_owner_person_code()
        integration_two.click_send_all_deals()
        integration_two.click_save()

        # IntegrationTwo
        assert integration_two.element_visible(), "IntegrationTwo not open after setting!"
        integration_two.click_generate()
        generate_and_verify_download(driver, file_name='import_order', file_type='xml')

        integration_two.check_error_modal()
        assert integration_two.element_visible(), "IntegrationTwo not open after import_order!"
        integration_two.click_exchange_mode(exchange_file=2)
        integration_two.input_date()
        integration_two.click_generate()
        generate_and_verify_download(driver, file_name='export_order', file_type='xml')

        integration_two.check_error_modal()
        assert integration_two.element_visible(), "IntegrationTwo not open after export_order!"
        integration_two.click_exchange_mode(exchange_file=3)
        integration_two.click_generate()
        generate_and_verify_download(driver, file_name='export_status', file_type='xml')

        # integration_two.check_error_modal()
        # assert integration_two.element_visible(), "IntegrationTwo not open after export_status!"
        # integration_two.click_exchange_mode(exchange_file=4)
        # integration_two.input_date()
        # integration_two.click_generate()
        # generate_and_verify_download(driver, file_name='export_balance', file_type='xml')

        integration_two.check_error_modal()
        assert integration_two.element_visible(), "IntegrationTwo not open after export_balance!"
        integration_two.click_exchange_mode(exchange_file=5)
        integration_two.input_date()
        integration_two.click_generate()
        generate_and_verify_download(driver, file_name='import_input', file_type='xml')

        integration_two.check_error_modal()
        assert integration_two.element_visible(), "IntegrationTwo not open after import_input!"

        base_page.logger.info(f"✅Test end: test_check_report_integration_two successfully!")

    except AssertionError as ae:
        base_page.logger.error(f'Assertion error: {str(ae)}')
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        pytest.fail(str(e))