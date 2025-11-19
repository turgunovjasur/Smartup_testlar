import pytest
from flows.auth_flow import login_user
from flows.order_flows.order_list_flow import order_list
from pages.trade.tdeal.order.order_history_list.order_history_list import OrdersHistoryList
from pages.trade.tdeal.order.order_list.orders_list import OrdersList

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_A
@pytest.mark.order(260)
def test_check_report_for_order_list(driver, test_data):
    data = test_data["data"]
    client_name = f"{data['client_name']}-A"

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_list(driver, find_row=client_name, report=True)

    list_page = OrdersList(driver)

    def check_report_flow(report_name, all_button=None):
        try:
            list_page.switch_window(direction="prepare")
            list_page.click_reports_all_button(report_name, all_button)
            list_page.switch_window(direction="forward")
            list_page.verify_report_opened()
        except Exception as e:
            list_page.logger.error(f"[FAILED]: {report_name} \n{e}")
            list_page.take_screenshot(filename=f"{report_name}")
            raise
        else:
            list_page.logger.info(f"[PASSED]: {report_name}")
        finally:
            list_page.switch_window(direction="back")

        order_list(driver)

    check_report_flow(report_name="Акт приёма-передачи ТМЦ для доставки", all_button=True)
    check_report_flow(report_name="Загрузочный лист")
    check_report_flow(report_name="Загрузочный лист для SAP")
    check_report_flow(report_name="Заявка на покупку запасных частей")
    check_report_flow(report_name="Лист заказов № 3")
    check_report_flow(report_name="Лист заказов № 6")
    check_report_flow(report_name="Лист заказов №1")
    check_report_flow(report_name="Накладная счет-фактура (2003)")
    check_report_flow(report_name="Накладная №3(2007)")
    # check_report_flow(report_name="Накладная №4(2012)")
    check_report_flow(report_name="Накладная №5 (2018)")
    check_report_flow(report_name="Накладная №7")
    check_report_flow(report_name="Общая сумма")
    check_report_flow(report_name="Общая сумма возврата")
    check_report_flow(report_name="Перечень форма 1")
    check_report_flow(report_name="Счет на оплату")
    check_report_flow(report_name="Счет-фактура с НДС")
    check_report_flow(report_name="Счет-фактура №1(2004)")
    check_report_flow(report_name="ТТН")
    check_report_flow(report_name="Требование на отпуск форма 1")
    # check_report_flow(report_name="Счет-фактура с наценкой")

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_A
@pytest.mark.order(310)
def test_check_report_for_order_history_list(driver, test_data):
    data = test_data["data"]
    client_name = f"{data['client_name']}-A"

    login_user(driver, test_data, url='trade/tdeal/order/order_history_list')

    list_page = OrdersHistoryList(driver)
    list_page.element_visible()
    list_page.find_row(client_name)

    def check_report_flow(report_name, all_button=None):
        try:
            list_page.switch_window(direction="prepare")
            list_page.click_reports_all_button(report_name, all_button)
            list_page.switch_window(direction="forward")
            list_page.verify_report_opened()
        except Exception as e:
            list_page.logger.error(f"[FAILED]: {report_name} \n{e}")
            list_page.take_screenshot(filename=f"{report_name}")
            raise
        else:
            list_page.logger.info(f"[PASSED]: {report_name}")
        finally:
            list_page.switch_window(direction="back")

        list_page.element_visible()

    check_report_flow(report_name="Акт приёма-передачи ТМЦ для доставки", all_button=True)
    check_report_flow(report_name="Загрузочный лист")
    check_report_flow(report_name="Загрузочный лист для SAP")
    check_report_flow(report_name="Заявка на покупку запасных частей")
    check_report_flow(report_name="Лист заказов № 3")
    check_report_flow(report_name="Лист заказов № 6")
    check_report_flow(report_name="Лист заказов №1")
    check_report_flow(report_name="Накладная счет-фактура (2003)")
    check_report_flow(report_name="Накладная №3(2007)")
    # check_report_flow(report_name="Накладная №4(2012)")
    check_report_flow(report_name="Накладная №5 (2018)")
    check_report_flow(report_name="Накладная №7")
    check_report_flow(report_name="Общая сумма")
    check_report_flow(report_name="Общая сумма возврата")
    check_report_flow(report_name="Перечень форма 1")
    check_report_flow(report_name="Счет на оплату")
    check_report_flow(report_name="Счет-фактура с НДС")
    check_report_flow(report_name="Счет-фактура №1(2004)")
    check_report_flow(report_name="ТТН")
    check_report_flow(report_name="Требование на отпуск форма 1")
    # check_report_flow(report_name="Счет-фактура с наценкой")

# ======================================================================================================================