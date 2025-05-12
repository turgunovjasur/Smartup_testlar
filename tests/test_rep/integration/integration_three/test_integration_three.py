import pytest
from autotest.core.md.base_page import BasePage
from autotest.trade.rep.integration.integration_three.integration_three import IntegrationThree
from tests.test_base.test_base import login_admin
from utils.driver_setup import driver
from tests.conftest import test_data


def test_check_report_integration_three(driver, test_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Run test: test_check_report_integration_three")

    try:
        login_admin(driver, test_data, url='trade/rep/integration/integration_three')

        # IntegrationThree
        integration_three = IntegrationThree(driver)
        assert integration_three.element_visible(), "IntegrationThree not open!"
        integration_three.click_show_setting()

        # Setting
        assert integration_three.element_visible_setting(), "IntegrationThree Setting not open!"
        integration_three.click_save()

        # IntegrationThree
        assert integration_three.element_visible(), "IntegrationThree not open after setting!"
        integration_three.input_date()
        integration_three.click_generate()

        # Report content
        integration_three.switch_to_iframe()
        assert integration_three.check_report_document(document=1), "Report content (document=1) not open!"
        assert integration_three.check_report_document(document=2), "Report content (document=2) not open!"
        assert integration_three.check_report_document(document=3), "Report content (document=3) not open!"

        base_page.logger.info(f"✅Test end: test_check_report_integration_three successfully!")

    except AssertionError as ae:
        base_page.logger.error(f'Assertion error: {str(ae)}')
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        pytest.fail(str(e))
