import os
import pytest
from pages.core.md.base_page import BasePage
from pages.trade.rep.integration.cislink.cislink import CisLink
from flows.auth_flow import login_admin
from utils.download_manager import clear_old_download, generate_and_verify_download, DOWNLOAD_DIR


@pytest.mark.regression
@pytest.mark.integration_report
def test_check_report_cis_link(driver, test_data):
    data = test_data["data"]
    price_types_name = data["price_type_name_UZB"]
    filial_name = data["filial_name"]

    login_admin(driver, test_data, url='trade/rep/integration/cislink')

    cis_link = CisLink(driver)
    cis_link.element_visible()
    cis_link.click_show_setting()
    cis_link.element_visible_setting()
    cis_link.input_identification_code(identification_code_name='test')
    cis_link.input_person_groups(person_groups_name='Группа')
    cis_link.input_product_groups(product_group_name='Группа')
    cis_link.input_filial(filial_name)
    cis_link.input_price_types(price_types_name)
    cis_link.click_save()
    cis_link.element_visible()

    base_page = BasePage(driver)
    clear_old_download(base_page, expected_name="cislink", file_type="zip")
    before_files = set(os.listdir(DOWNLOAD_DIR))
    cis_link.click_generate()
    generate_and_verify_download(base_page, before_files=before_files, expected_name="cislink", file_type="zip")
