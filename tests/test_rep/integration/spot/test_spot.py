import random
import pytest
from autotest.core.md.base_page import BasePage
from autotest.trade.rep.integration.spot.spot import Spot
from autotest.trade.rep.integration.spot_template_add.spot_template_add import SpotTemplateAdd
from autotest.trade.rep.integration.spot_template_list.spot_template_list import SpotTemplateList
from tests.test_base.test_base import login_admin
from tests.test_rep.integration.rep_main_funksiya import generate_and_verify_download
from utils.driver_setup import driver
from tests.conftest import test_data


def test_check_report_spot_2d(driver, test_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Run test: test_check_report_spot_2d")

    product_group_name = 'Группа'
    random_nomer = random.randint(10000, 99999)
    template_name = f'Spot2D-{random_nomer}'

    try:
        login_admin(driver, test_data, url='trade/rep/integration/spot')

        # Spot
        spot = Spot(driver)
        assert spot.element_visible(), "Spot not open!"
        spot.click_template()

        # SpotTemplateList
        spot_template_list = SpotTemplateList(driver)
        assert spot_template_list.element_visible(), "SpotTemplateList not open!"
        spot_template_list.click_add()

        # SpotTemplateAdd
        spot_template_add = SpotTemplateAdd(driver)
        assert spot_template_add.element_visible(), "SpotTemplateAdd not open!"

        spot_template_add.input_name(template_name)
        spot_template_add.input_product_groups(product_group_name)
        spot_template_add.click_save()

        # SpotTemplateList
        assert spot.element_visible(), "Spot not open after save template!"
        spot.click_template()

        assert spot_template_add.element_visible(), "SpotTemplateAdd not open after save template!"
        spot_template_list.find_row(template_name)
        spot_template_list.click_close()

        assert spot.element_visible(), "Spot not open after save template!"
        spot.click_setting()
        spot.click_preferences_clear()

        assert spot.element_visible(), "Spot not open after clear setting!"
        spot.click_run()
        generate_and_verify_download(driver, file_name='Spot2D', file_type='zip')

        base_page.logger.info(f"✅Test end: test_check_report_spot_2d successfully!")

    except AssertionError as ae:
        base_page.logger.error(f'Assertion error: {str(ae)}')
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        pytest.fail(str(e))