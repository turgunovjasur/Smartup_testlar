from autotest.trade.rep.integration.saleswork.saleswork import SalesWork
from tests.test_base.test_base import login_user
from tests.test_rep.integration.rep_main_funksiya import generate_and_verify_download
from tests.conftest import driver, test_data


def test_check_report_sales_work(driver, test_data):
    login_user(driver, test_data, url='trade/rep/integration/saleswork')

    # SalesWork
    sales_work = SalesWork(driver)
    sales_work.element_visible()
    sales_work.click_show_setting()

    # Setting
    sales_work.element_visible_setting()
    sales_work.input_product_groups(product_group_name='Группа')
    sales_work.click_save()

    # SalesWork
    sales_work.element_visible()
    sales_work.click_generate()
    generate_and_verify_download(driver, file_name='saleswork', file_type='zip')