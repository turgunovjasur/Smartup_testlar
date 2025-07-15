import random
import pytest
from autotest.anor.rep.mbi.tdeal.order.write_off_report_constructor import WriteOffReportConstructor
from autotest.core.md.base_page import BasePage
from flows.auth_flow import login_user
from tests.test_writeoff.write_off_flow import list_flow, add_flow, select_flow, get_balance_flow, \
    check_transaction_flow, view_flow, expense_flow


@pytest.mark.regression
@pytest.mark.order(70)
def test_add_write_off(driver, test_data, load_data, save_data):
    """Test adding a write-off"""

    data = test_data["data"]

    # Login
    login_user(driver, test_data, url='anor/mkw/writeoff/writeoff_list')

    list_flow(driver, add=True)

    write_off_number = random.randint(100000, 999999)
    get_data_input_value = add_flow(driver,
                                    write_off_number=write_off_number,
                                    warehouse_name=data["warehouse_name"],
                                    reason_name="Контрольная проверка")

    select_flow(driver, product_name=data["product_name"], product_quantity=10)

    add_flow(driver, select=True)

    list_flow(driver, find_row=write_off_number, view=True)

    view_flow(driver,
              navbar_name="Основная информация",
              currency_name="Узбекский сум",
              warehouse_name=data["warehouse_name"],
              reason_name="Контрольная проверка")

    list_flow(driver)

    get_balance_old = get_balance_flow(driver,
                                       warehouse_name=data["warehouse_name"],
                                       product_name=data["product_name"])

    list_flow(driver, find_row=write_off_number, change_status="В сборке")
    list_flow(driver, find_row=write_off_number)

    check_transaction_flow(driver)

    list_flow(driver, change_status="Проведено")
    list_flow(driver)

    get_balance_new = get_balance_flow(driver,
                                       warehouse_name=data["warehouse_name"],
                                       product_name=data["product_name"])
    assert get_balance_old == get_balance_new + 10
    list_flow(driver, find_row=write_off_number, expense=True)

    expense_flow(driver,
                 write_off_number=write_off_number,
                 warehouse_name=data["warehouse_name"],
                 total_sum=data["product_price"] * 10,
                 get_data_input_value=get_data_input_value,
                 expense_article_name=data["expense_article_name"])

    list_flow(driver, find_row=write_off_number, view=True)

    view_flow(driver, navbar_name="Расходы")

    list_flow(driver)


@pytest.mark.regression
@pytest.mark.order(71)
def test_check_constructor_report_write_off(driver, test_data, save_data, load_data):
    """Test checking a constructor report by write-off"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_check_constructor_report_write_off")

    login_user(driver, test_data, url='anor/rep/mbi/mkw/writeoff')

    write_off_report_constructor = WriteOffReportConstructor(driver)
    write_off_report_constructor.input_search_option(option_name="Дата списания")
    write_off_report_constructor.click_source_and_target(option_name="Дата списания", field_name="row")

    write_off_report_constructor.input_search_option(option_name="Списание")
    write_off_report_constructor.click_source_and_target(option_name="Списание", field_name="row")

    write_off_report_constructor.input_search_option(option_name="Склад")
    write_off_report_constructor.click_source_and_target(option_name="Склад", field_name="row")

    write_off_report_constructor.input_search_option(option_name="Валюта")
    write_off_report_constructor.click_source_and_target(option_name="Валюта", field_name="row")

    write_off_report_constructor.input_search_option(option_name="ТМЦ")
    write_off_report_constructor.click_source_and_target(option_name="ТМЦ", field_name="row")

    write_off_report_constructor.click_view_button()

    write_off_report_constructor.switch_to_iframe()
    valyuta = write_off_report_constructor.get_value_by_option_name("Валюта")
    kol_vo = write_off_report_constructor.get_value_by_option_name("Кол-во")

    base_page.logger.info(f"Валюта: {valyuta}")
    base_page.logger.info(f"Кол-во: {kol_vo}")
