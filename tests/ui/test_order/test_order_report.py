import time
import pyautogui
import pytest
import requests
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from pages.anor.mr.template_list.template_list import TemplateList
from pages.biruni.ker.setting_add.setting_add import SettingAdd
from pages.biruni.ker.template_role_list.template_role_list import TemplateRoleList
from pages.core.md.base_page import BasePage
from pages.trade.rep.mbi.tdeal.order.sales_report_constructor import SalesReportConstructor
from pages.trade.tdeal.order.order_history_list.order_history_list import OrdersHistoryList
from flows.auth_flow import login_user, login_admin
from pages.trade.tdeal.order.order_list.orders_list import OrdersList
from tests.ui.test_rep.integration.rep_main_funksiya import generate_and_verify_download, clear_old_download, DOWNLOAD_DIR

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_A
@pytest.mark.order(260)
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

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_A
@pytest.mark.order(310)
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

# ======================================================================================================================
import os

def get_data_file_path(filename, folder, subfolder):
    """
    Test fayli joylashgan katalogdan nisbiy yo‘l orqali faylning to‘liq pathini qaytaradi.
    Funksiya har doim test bilan bir joyda bo'lsin!
    """
    current_file_dir = os.path.dirname(os.path.abspath(__file__))

    # Smartup_testlar/data ni qidirish
    while True:
        potential_path = os.path.join(current_file_dir, folder, subfolder, filename)
        if os.path.isfile(potential_path):
            return potential_path

        # Bir katalog yuqoriga chiqamiz
        parent_dir = os.path.dirname(current_file_dir)
        if parent_dir == current_file_dir:
            break  # Root katalogga chiqib ketdi
        current_file_dir = parent_dir

    raise FileNotFoundError(f"{folder}/{subfolder}/{filename} topilmadi.")

# Invoice report
@pytest.mark.regression
@pytest.mark.order_group_D
@pytest.mark.order(440)
def test_add_template_for_order_invoice_report(driver, test_data):
    # Test data
    data = test_data["data"]
    template_name = data["template_name"]
    role_name = data["role_name"]
    form_name = 'Накладная (заказ)'
    filename = "test_invoice_report.xlsx"
    folder = "Smartup_testlar"
    subfolder = "data"

    login_admin(driver, test_data, url='anor/mr/template_list')

    template_list = TemplateList(driver)
    template_list.element_visible()
    template_list.click_add_button()

    setting_add = SettingAdd(driver)
    setting_add.element_visible()
    setting_add.input_form_name(form_name)
    setting_add.input_template_name(template_name)
    setting_add.click_template_input()

    report_path = get_data_file_path(filename, folder, subfolder)
    time.sleep(2)
    pyautogui.write(os.path.dirname(report_path), interval=0.2)
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.write("test_invoice_report.xlsx", interval=0.2)
    pyautogui.press('enter')

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

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_D
@pytest.mark.order(460)
def test_check_invoice_report_for_order_list(driver, test_data):
    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    invoice_report_name = data["template_name"]

    login_user(driver, test_data, url='trade/tdeal/order/order_list')

    order_list = OrdersList(driver)
    order_list.element_visible()
    order_list.find_row(client_name)

    base_page = BasePage(driver)
    clear_old_download(base_page, expected_name="Test_invoice_report", file_type="xlsx")
    before_files = set(os.listdir(DOWNLOAD_DIR))
    order_list.click_invoice_reports_all_button(invoice_report_name)
    generate_and_verify_download(base_page, before_files=before_files, expected_name="Test_invoice_report", file_type="xlsx")

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_A
@pytest.mark.order(290)
def test_sales_report_constructor(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_sales_report_constructor")

    login_user(driver, test_data, url='trade/rep/mbi/tdeal/order')

    sales_report_constructor = SalesReportConstructor(driver)
    sales_report_constructor.input_search_option(option_name="Заказ")

    sales_report_constructor.click_source_and_target(option_name="Заказ", field_name="row")

    sales_report_constructor.input_filter_fields(option_name="Статус", clear=True)

    sales_report_constructor.click_view_button()

    sales_report_constructor.switch_to_iframe()
    order_ids = sales_report_constructor.get_order_id_list()

    base_page.logger.info(f"order_ids: {order_ids}")

    order_id_1 = load_data("order_id_1")
    order_id_2 = load_data("order_id_2")

    assert order_id_1 in order_ids, f"Error: {order_id_1} not found!"
    assert order_id_2 in order_ids, f"Error: {order_id_2} not found!"

    time.sleep(2)

# ======================================================================================================================
