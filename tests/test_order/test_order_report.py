import time
import pytest
import requests
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from autotest.anor.mr.template_list.template_list import TemplateList
from autotest.biruni.ker.setting_add.setting_add import SettingAdd
from autotest.biruni.ker.template_role_list.template_role_list import TemplateRoleList
from autotest.core.md.base_page import BasePage
from autotest.trade.tdeal.order.order_history_list.order_history_list import OrdersHistoryList
from tests.test_base.test_base import login_user, login_admin
from autotest.trade.tdeal.order.order_list.orders_list import OrdersList
from tests.conftest import driver, test_data
from tests.test_rep.integration.rep_main_funksiya import generate_and_verify_download


def test_check_report_for_order_list(driver, test_data, timeout=60):
    base_page = BasePage(driver)
    base_page.logger.info("▶️Run test: test_check_report_for_order_list")

    data = test_data["data"]
    client_name = f"{data['client_name']}-A"
    report_names = [
        "Загрузочный лист",
        "Лист заказов № 3",
        "Лист заказов № 6",
        "Лист заказов №1",
        "Накладная №3(2007)",
        "Накладная №7",
        "Общая сумма",
        "Общая сумма возврата",
        "Счет на оплату",
        "Счет-фактура с НДС",
        "Счет-фактура №1(2004)",
        "ТТН",
        "Требование на отпуск форма 1",
    ]

    errors = []
    try:
        driver.execute_script("WebGLRenderingContext = function() {};")
        base_page.logger.info("🟢 GPU va WebGL temporarily deleted!")

        login_user(driver, test_data, url='trade/tdeal/order/order_list')

        order_list = OrdersList(driver)
        order_list.element_visible()
        order_list.find_row(client_name)

        for index, report_name in enumerate(report_names):
            old_windows = driver.window_handles
            time.sleep(1)
            order_list.click_reports_all_button(report_name=report_name, all_button=(index == 0))

            # YANGI OYNA OCHILISHINI ANIQLASH UCHUN TO'G'RI JOY:
            try:
                WebDriverWait(driver, timeout).until(
                    lambda d: len(d.window_handles) > len(old_windows),
                    message=f"❌ -> ({report_name}) new window not open!")
            except TimeoutException as e:
                base_page.logger.error(str(e))
                errors.append(str(e))
                continue

            new_windows = driver.window_handles
            new_window = [w for w in new_windows if w not in old_windows][0]
            driver.switch_to.window(new_window)

            WebDriverWait(driver, timeout).until(lambda d: d.execute_script("return document.readyState") == "complete")

            session = requests.Session()
            cookies = driver.get_cookies()
            for cookie in cookies:
                session.cookies.set(cookie['name'], cookie['value'])

            try:
                time.sleep(1)
                response = session.get(driver.current_url, timeout=timeout)
                if response.status_code != 200:
                    error_msg = f"❌ -> ({report_name}) report page not download! Status cod: {response.status_code}"
                    base_page.logger.error(error_msg)
                    errors.append(error_msg)
                else:
                    base_page.logger.info(f"✅ {report_name} report open!")

            except requests.RequestException as e:
                error_msg = f"❌ -> ({report_name}) report HTTP request error: {str(e)}"
                base_page.logger.error(error_msg)
                errors.append(error_msg)

            driver.close()
            driver.switch_to.window(old_windows[1])

    except AssertionError as ae:
        base_page.logger.error(f'Assertion error: {str(ae)}')
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        pytest.fail(str(e))

    finally:
        driver.execute_script("WebGLRenderingContext = undefined;")
        base_page.logger.info("🔴 GPU va WebGL restored!")
        if errors:
            errors_joined = "\n".join(errors)
            base_page.logger.error(f"Test errors:\n{errors_joined}")
            pytest.fail(f"Test_errors:\n{errors_joined}")


def test_check_report_for_order_history_list(driver, test_data, timeout=60):
    base_page = BasePage(driver)
    base_page.logger.info("▶️Run test: test_check_invoices_report_for_order_history_list")

    data = test_data["data"]
    client_name = f"{data['client_name']}-A"
    report_names = [
        "Загрузочный лист",
        "Лист заказов № 3",
        "Лист заказов № 6",
        "Лист заказов №1",
        "Накладная №3(2007)",
        "Накладная №7",
        "Общая сумма",
        "Общая сумма возврата",
        "Счет на оплату",
        "Счет-фактура с НДС",
        "Счет-фактура №1(2004)",
        "ТТН",
        "Требование на отпуск форма 1",
    ]

    errors = []
    try:
        driver.execute_script("WebGLRenderingContext = function() {};")
        base_page.logger.info("🟢 GPU va WebGL temporarily deleted!")

        login_user(driver, test_data, url='trade/tdeal/order/order_history_list')

        order_history_list = OrdersHistoryList(driver)
        order_history_list.element_visible()
        order_history_list.find_row(client_name)

        for index, report_name in enumerate(report_names):
            old_windows = driver.window_handles
            order_history_list.click_reports_all_button(report_name=report_name, all_button=(index == 0))

            try:
                time.sleep(1)
                WebDriverWait(driver, timeout).until(
                    lambda d: len(d.window_handles) > len(old_windows),
                    message=f"❌ -> ({report_name}) new window not open!")
            except TimeoutException as e:
                base_page.logger.error(str(e))
                errors.append(str(e))
                continue

            new_windows = driver.window_handles
            new_window = [w for w in new_windows if w not in old_windows][0]
            driver.switch_to.window(new_window)
            time.sleep(1)
            WebDriverWait(driver, timeout).until(lambda d: d.execute_script("return document.readyState") == "complete")

            session = requests.Session()
            cookies = driver.get_cookies()
            for cookie in cookies:
                session.cookies.set(cookie['name'], cookie['value'])

            try:
                response = session.get(driver.current_url, timeout=timeout)
                if response.status_code != 200:
                    error_msg = f"❌ -> ({report_name}) report page not download! Status cod: {response.status_code}"
                    base_page.logger.error(error_msg)
                    errors.append(error_msg)
                else:
                    base_page.logger.info(f"✅ {report_name} report open!")

            except requests.RequestException as e:
                error_msg = f"❌ -> ({report_name}) report HTTP request error: {str(e)}"
                base_page.logger.error(error_msg)
                errors.append(error_msg)

            driver.close()
            driver.switch_to.window(old_windows[1])

    except AssertionError as ae:
        base_page.logger.error(f'Assertion error: {str(ae)}')
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        pytest.fail(str(e))

    finally:
        driver.execute_script("WebGLRenderingContext = undefined;")
        base_page.logger.info("🔴 GPU va WebGL restored!")

        if errors:
            errors_joined = "\n".join(errors)
            base_page.logger.error(f"Test errors:\n{errors_joined}")
            pytest.fail(f"Test_errors:\n{errors_joined}")


# Invoice report
def test_add_template_for_order_invoice_report(driver, test_data):
    # Test data
    data = test_data["data"]
    template_name = data["template_name"]
    role_name = data["role_name"]
    form_name = 'Накладная (заказ)'
    report_path = r"C:\Users\jasur.turgunov\Desktop\ish\Smartup_testlar\data"

    login_admin(driver, test_data, url='anor/mr/template_list')

    template_list = TemplateList(driver)
    template_list.element_visible()
    template_list.click_add_button()

    setting_add = SettingAdd(driver)
    setting_add.element_visible()
    setting_add.input_form_name(form_name)
    setting_add.input_template_name(template_name)
    setting_add.click_template_input()
    setting_add.click_windows_file(report_path)
    setting_add.click_windows_download_file()
    setting_add.click_save_button()

    template_list.element_visible()
    template_list.find_row(template_name)
    template_list.click_attach_role_button()
    template_list.click_detach_role_button()

    template_role_list = TemplateRoleList(driver)
    template_role_list.element_visible()
    template_role_list.find_row(role_name)
    template_role_list.click_attach_button()
    template_role_list.click_close_button()
    template_list.element_visible()


def test_check_invoice_report_for_order_list(driver, test_data):
    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    invoice_report_name = data["template_name"]

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_list = OrdersList(driver)
    order_list.element_visible()
    order_list.find_row(client_name)

    order_list.click_invoice_reports_all_button(invoice_report_name)
    generate_and_verify_download(driver, file_name='invoice_report', file_type='xlsx')