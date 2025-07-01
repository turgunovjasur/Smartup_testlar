import random
import pytest
from autotest.trade.rep.integration.spot.spot import Spot
from autotest.trade.rep.integration.spot_template_add.spot_template_add import SpotTemplateAdd
from autotest.trade.rep.integration.spot_template_list.spot_template_list import SpotTemplateList
from flows.auth_flow import login_admin
from tests.test_rep.integration.rep_main_funksiya import generate_and_verify_download


@pytest.mark.regression
@pytest.mark.integration_report
@pytest.mark.order(73)
def test_check_report_spot_2d(driver, test_data):
    product_group_name = 'Группа'
    random_nomer = random.randint(10000, 99999)
    template_name = f'Spot2D-{random_nomer}'

    login_admin(driver, test_data, url='trade/rep/integration/spot')

    # Spot
    spot = Spot(driver)
    spot.element_visible()
    spot.click_template()

    # SpotTemplateList
    spot_template_list = SpotTemplateList(driver)
    spot_template_list.element_visible()
    spot_template_list.click_add()

    # SpotTemplateAdd
    spot_template_add = SpotTemplateAdd(driver)
    spot_template_add.element_visible()

    spot_template_add.input_name(template_name)
    spot_template_add.input_product_groups(product_group_name)
    spot_template_add.click_save()

    # SpotTemplateList
    spot.element_visible()
    spot.click_template()

    spot_template_add.element_visible()
    spot_template_list.find_row(template_name)
    spot_template_list.click_close()

    spot.element_visible()
    spot.click_setting()
    spot.click_preferences_clear()

    spot.element_visible()
    spot.click_run()
    generate_and_verify_download(driver, file_name='Spot2D', file_type='zip')