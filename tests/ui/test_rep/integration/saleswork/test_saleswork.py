import os
import random
import pytest
from pages.core.md.base_page import BasePage
from pages.trade.rep.integration.saleswork.saleswork import SalesWork
from pages.trade.rep.integration.saleswork.saleswork_template_add import SalesWorkTemplateAdd
from pages.trade.rep.integration.saleswork.saleswork_template_list import SalesWorkTemplateList
from flows.auth_flow import login_admin
from utils.download_manager import clear_old_download, generate_and_verify_download, DOWNLOAD_DIR


@pytest.mark.regression
@pytest.mark.integration_report
def test_check_report_sales_work(driver, test_data):
    # test data
    random_number = random.randint(1, 9999)
    template_name = f'SalesWork template-{random_number}'

    # login
    login_admin(driver, test_data, url='trade/rep/integration/saleswork')

    # SalesWork
    sales_work = SalesWork(driver)
    sales_work.element_visible()
    sales_work.click_select_template()

    template_list = SalesWorkTemplateList(driver)
    template_list.click_add()

    template_add = SalesWorkTemplateAdd(driver)
    template_add.element_visible()
    template_add.input_name(template_name)
    template_add.input_product_groups(product_group_name='Группа')
    template_add.click_save()

    # SalesWork
    sales_work.element_visible()
    get_templates = sales_work.input_templates()
    assert get_templates == template_name, f"Error: {get_templates} != {template_name}"

    base_page = BasePage(driver)
    clear_old_download(base_page, expected_name="sales_work", file_type="zip")
    before_files = set(os.listdir(DOWNLOAD_DIR))
    sales_work.click_generate()
    generate_and_verify_download(base_page, before_files=before_files, expected_name="sales_work", file_type="zip")