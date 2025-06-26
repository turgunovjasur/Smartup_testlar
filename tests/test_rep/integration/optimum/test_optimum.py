import pytest
from autotest.trade.rep.integration.optimum.optimum import Optimum
from flows.auth_flow import login_admin
from tests.test_rep.integration.rep_main_funksiya import generate_and_verify_download


@pytest.mark.integration_report
def test_check_report_optimum(driver, test_data):
    data = test_data["data"]
    product_group = "Группа"
    filial_name = data['filial_name']

    login_admin(driver, test_data, url='trade/rep/integration/optimum')

    # Optimum
    optimum = Optimum(driver)
    optimum.element_visible()
    optimum.click_show_setting()

    # Setting
    optimum.element_visible_setting()
    optimum.element_visible_setting()
    optimum.input_product_groups(product_group)
    optimum.input_prefix_transfer_out(prefix_transfer_out=1)
    optimum.input_prefix_transfer_in(prefix_transfer_in=2)
    optimum.input_prefix_write_off(prefix_write_off=3)
    optimum.input_prefix_warehouse_receipt(prefix_warehouse_receipt=4)
    optimum.input_prefix_site_transfer_out(prefix_site_transfer_out=5)
    optimum.input_prefix_site_transfer_in(prefix_site_transfer_in=6)
    optimum.input_prefix_production_write_off(prefix_production_write_off=7)
    optimum.input_prefix_production_receipt(prefix_production_receipt=8)
    optimum.click_save()

    # Optimum
    optimum.element_visible()
    optimum.click_generate()
    generate_and_verify_download(driver, file_name='optimum', file_type='zip')

    # Optimum
    optimum.element_visible()
    optimum.click_all_filial_checkbox()
    optimum.input_filial(filial_name)
    optimum.click_generate()
    generate_and_verify_download(driver, file_name='ooptimum', file_type='zip')