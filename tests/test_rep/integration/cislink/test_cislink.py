import pytest
from autotest.trade.rep.integration.cislink.cislink import CisLink
from flows.auth_flow import login_user
from tests.test_rep.integration.rep_main_funksiya import generate_and_verify_download


@pytest.mark.integration_report
def test_check_report_cis_link(driver, test_data):
    data = test_data["data"]
    price_types_name = data["price_type_name_UZB"]

    login_user(driver, test_data, url='trade/rep/integration/cislink')

    # CisLink
    cis_link = CisLink(driver)
    cis_link.element_visible()
    cis_link.click_show_setting()

    # Setting
    cis_link.element_visible_setting()
    cis_link.input_identification_code(identification_code_name='test')
    cis_link.input_person_groups(person_groups_name='Группа')
    cis_link.input_product_groups(product_group_name='Группа')
    cis_link.input_price_types(price_types_name)
    cis_link.click_save()

    # CisLink
    cis_link.element_visible()
    cis_link.click_generate()
    generate_and_verify_download(driver, file_name='cislink', file_type='zip')