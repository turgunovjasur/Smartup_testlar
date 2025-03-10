import os
import re
import time
from datetime import datetime, timedelta

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
from autotest.trade.tdeal.order.order_list.orders_page import OrdersList
from tests.conftest import test_data
from utils.driver_setup import driver


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
        assert order_list.element_visible(), "order_list not open!"
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
        assert order_history_list.element_visible(), "order_history_list not open!"
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
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_template_for_order_invoice_report")

    # Test data
    data = test_data["data"]
    template_name = data["template_name"]
    role_name = data["role_name"]
    form_name = 'Накладная (заказ)'

    try:
        login_admin(driver, test_data, url='anor/mr/template_list')

        template_list = TemplateList(driver)
        assert template_list.element_visible(), "TemplateList not open!"
        template_list.click_add_button()

        setting_add = SettingAdd(driver)
        assert setting_add.element_visible(), "SettingAdd not open!"
        setting_add.input_form_name(form_name)
        setting_add.input_template_name(template_name)
        setting_add.click_template_input()
        setting_add.click_windows_file()
        setting_add.click_windows_download_file()
        setting_add.click_save_button()

        assert template_list.element_visible(), "TemplateList not open after save!"
        template_list.find_row(template_name)
        template_list.click_attach_role_button()
        template_list.click_detach_role_button()

        template_role_list = TemplateRoleList(driver)
        assert template_role_list.element_visible(), "TemplateRoleList not open!"
        template_role_list.find_row(role_name)
        template_role_list.click_attach_button()
        template_role_list.click_close_button()
        assert template_list.element_visible(), "TemplateRoleList not open after save!"

        base_page.logger.info(f"✅ Test end: test_add_template_for_order_invoice_report")

    except AssertionError as ae:
        base_page.logger.error(f'Assertion error: {str(ae)}')
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        pytest.fail(str(e))


def test_check_invoice_report_for_order_list(driver, test_data, minute_tolerance=5):
    """`minute_tolerance` - oxirgi necha minut oralig'idagi fayllarni tekshirish uchun parametr."""

    base_page = BasePage(driver)
    base_page.logger.info(f"▶️ Running: test_check_invoice_report_for_order_list (Tolerance: {minute_tolerance} minut)")

    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    invoice_report_name = data["template_name"]

    try:
        login_user(driver, test_data, url='trade/tdeal/order/order_list')

        order_list = OrdersList(driver)
        assert order_list.element_visible(), "❌ order_list sahifasi ochilmadi!"
        order_list.find_row(client_name)

        # Hozirgi vaqtni oldin olish
        report_request_time = datetime.now()
        time.sleep(1)

        order_list.click_invoice_reports_all_button(invoice_report_name)
        time.sleep(3)

        downloads_path = os.path.join(os.environ["USERPROFILE"], "Downloads")

        # Yuklangan fayllarni olish va tekshirish
        files = os.listdir(downloads_path)
        files = [os.path.join(downloads_path, f) for f in files if f.endswith('.xlsx')]
        files.sort(key=os.path.getctime, reverse=True)

        latest_file = files[0] if files else None
        assert latest_file is not None, "❌ Invoice fayli yuklanmadi!"

        file_name = os.path.basename(latest_file)

        base_page.logger.info(f"✅ Yuklangan fayl nomi: {file_name}")

        # Regex
        regex_pattern = rf"{invoice_report_name}\((\d{{2}}\.\d{{2}}\.\d{{4}})\+(\d{{2}}_\d{{2}}(?:_\d{{2}})?)\)\.xlsx"
        base_page.logger.info(f"🔎 Tekshirilayotgan regex: {regex_pattern}")

        match = re.search(regex_pattern, file_name)
        assert match, f"❌ Fayl nomi regexga mos kelmadi: {file_name}"

        file_date = match.group(1)  # 04.03.2025
        file_time = match.group(2)  # 12_33 yoki 12_33_11
        file_time = file_time[:5]  # Sekundni olib tashlaymiz (faqat HH:MM qoldiramiz)

        file_datetime_str = f"{file_date} {file_time.replace('_', ':')}"  # "04.03.2025 12:33"
        file_datetime = datetime.strptime(file_datetime_str, "%d.%m.%Y %H:%M")

        lower_bound = report_request_time - timedelta(minutes=minute_tolerance)
        upper_bound = report_request_time + timedelta(minutes=minute_tolerance)

        base_page.logger.info(f"Tekshirilayotgan vaqt oralig'i: {lower_bound.strftime('%d.%m.%Y %H:%M')} - {upper_bound.strftime('%d.%m.%Y %H:%M')}")
        base_page.logger.info(f"Fayl vaqti: {file_datetime.strftime('%d.%m.%Y %H:%M')}")

        assert lower_bound <= file_datetime <= upper_bound, (
            f"❌ Yuklangan fayl vaqti noto‘g‘ri: {file_datetime}, kutilgan oraliq: "
            f"{lower_bound.strftime('%d.%m.%Y %H:%M')} - {upper_bound.strftime('%d.%m.%Y %H:%M')}")

        base_page.logger.info(f"✅ Oxirgi yuklangan fayl: {latest_file} (vaqti to‘g‘ri)")

    except AssertionError as ae:
        base_page.logger.error(f'❌ Assertion error: {str(ae)}')
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        base_page.logger.error(f'❌ Xatolik: {str(e)}')
        pytest.fail(str(e))













