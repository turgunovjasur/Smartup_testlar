import pytest
from autotest.core.md.base_page import BasePage
from autotest.trade.rep.integration.saleswork.saleswork import SalesWork
from tests.test_base.test_base import login_user
from tests.test_rep.integration.rep_main_funksiya import generate_and_verify_download
from utils.driver_setup import driver
from tests.conftest import test_data


def test_check_report_sales_work(driver, test_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Run test: test_check_report_sales_work")

    try:
        login_user(driver, test_data, url='trade/rep/integration/saleswork')

        # SalesWork
        sales_work = SalesWork(driver)
        assert sales_work.element_visible(), "SalesWork not open!"
        sales_work.click_show_setting()

        # Setting
        assert sales_work.element_visible_setting(), "SalesWork Setting not open!"
        sales_work.click_save()

        # SalesWork
        assert sales_work.element_visible(), "SalesWork not open after setting!"
        sales_work.click_generate()
        generate_and_verify_download(driver, file_name='saleswork', file_type='zip')

        base_page.logger.info(f"✅Test end: test_check_report_sales_work successfully!")

    except AssertionError as ae:
        base_page.logger.error(f'Assertion error: {str(ae)}')
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        pytest.fail(str(e))