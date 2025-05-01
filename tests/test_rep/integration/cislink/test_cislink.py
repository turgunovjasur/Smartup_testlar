import pytest
from autotest.core.md.base_page import BasePage
from autotest.trade.rep.integration.cislink.cislink import CisLink
from tests.test_base.test_base import login_user
from tests.test_rep.integration.rep_main_funksiya import generate_and_verify_download
from utils.driver_setup import driver
from tests.conftest import test_data


def test_check_report_cis_link(driver, test_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Run test: test_check_report_cislink")

    try:
        login_user(driver, test_data, url='trade/rep/integration/cislink')

        # CisLink
        cis_link = CisLink(driver)
        assert cis_link.element_visible(), "CisLink not open!"
        cis_link.click_show_setting()

        # Setting
        assert cis_link.element_visible_setting(), "CisLink Setting not open!"
        cis_link.click_save()

        # CisLink
        assert cis_link.element_visible(), "CisLink not open after setting!"
        cis_link.click_generate()
        generate_and_verify_download(driver, file_name='cislink', file_type='zip')

        base_page.logger.info(f"✅Test end: test_check_report_cis_link successfully!")

    except AssertionError as ae:
        base_page.logger.error(f'Assertion error: {str(ae)}')
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        pytest.fail(str(e))