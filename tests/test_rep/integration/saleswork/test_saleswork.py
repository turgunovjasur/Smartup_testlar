import random

import pytest

from autotest.trade.rep.integration.saleswork.saleswork import SalesWork
from autotest.trade.rep.integration.saleswork.saleswork_template_add import SalesWorkTemplateAdd
from autotest.trade.rep.integration.saleswork.saleswork_template_list import SalesWorkTemplateList
from flows.auth_flow import login_user
from tests.test_rep.integration.rep_main_funksiya import generate_and_verify_download


@pytest.mark.integration_report
def test_check_report_sales_work(driver, test_data):
    # test data
    random_number = random.randint(1, 9999)
    template_name = f'SalesWork template-{random_number}'

    # login
    login_user(driver, test_data, url='trade/rep/integration/saleswork')

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

    sales_work.click_generate()
    generate_and_verify_download(driver, file_name='saleswork', file_type='zip')