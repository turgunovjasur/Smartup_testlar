from autotest.trade.rep.integration.integration_three.integration_three import IntegrationThree
from tests.test_base.test_base import login_admin
from tests.conftest import driver, test_data


def test_check_report_integration_three(driver, test_data):
    login_admin(driver, test_data, url='trade/rep/integration/integration_three')

    # IntegrationThree
    integration_three = IntegrationThree(driver)
    integration_three.element_visible()
    integration_three.click_show_setting()

    # Setting
    integration_three.element_visible_setting()
    integration_three.click_save()

    # IntegrationThree
    integration_three.element_visible()
    integration_three.input_date()
    integration_three.click_generate()

    # Report content
    integration_three.switch_to_iframe()
    integration_three.check_report_document(document=1)
    integration_three.check_report_document(document=2)
    integration_three.check_report_document(document=3)