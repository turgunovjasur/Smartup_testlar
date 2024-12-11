import random
import time

from autotest.anor.mdeal.order.offset.offset.offset import Offset
from autotest.anor.mdeal.order.offset.offset_detail_list.offset_detail_list import OffsetDetailList
from autotest.anor.mdeal.order.offset.offset_list.offset_list import OffsetList
from autotest.core.md.base_page import BasePage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.tcs.cashin_add.cashin_add import CashinAdd
from autotest.trade.tcs.cashin_list.cashin_list import CashinList
from autotest.trade.tcs.cashin_view.cashin_view import CashinView
from tests.test_base.test_base import test_data, login, dashboard, open_new_window, get_driver
from utils.driver_setup import driver


def cashin_add(driver, client_name=None):
    # Test data
    data = test_data()["data"]

    email_user = data["email_user"]
    password_user = data["password_user"]
    filial_name = data["filial_name"]
    client_name = client_name if client_name is not None else data["client_name"]
    payment_type_name = data["payment_type_name"]
    cashbox_name = data["cash_register_name"]

    # Login
    login(driver, email_user, password_user)

    # Dashboard
    dashboard(driver)
    dashboard_page = DashboardPage(driver)
    dashboard_page.find_filial(filial_name)

    # Open Cashin List
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'trade/tcs/cashin_list')
    cashin_list = CashinList(driver)
    assert cashin_list.element_visible(), 'CashinList not open!'
    cashin_list.click_add_button()

    # Cashin Add
    cashin_add = CashinAdd(driver)
    assert cashin_add.element_visible(), 'CashinAdd not open!'
    cashin_number = random.randint(1, 999999)
    cashin_add.input_cashin_number(cashin_number)
    cashin_add.input_clients(client_name)

    get_amount = cashin_add.get_amount()
    cashin_add.input_amount(get_amount)

    cashin_add.input_payment_types(payment_type_name)
    cashin_add.input_cashbox(cashbox_name)
    cashin_add.click_save_button()
    cashin_add.click_close_button()

    # Cashin List
    assert cashin_list.element_visible(), 'CashinList not open!'
    cashin_list.find_row(cashin_number)
    cashin_list.click_view_button()

    # Cashin View
    cashin_view = CashinView(driver)
    assert cashin_view.element_visible(), 'CashinView not open!'
    text = cashin_view.check_cashin_number()
    assert cashin_number == text, f'cashin_number: {cashin_number} != text: {text}'
    cashin_view.click_close_button()

    # Cashin List
    assert cashin_list.element_visible(), 'CashinList not open!'
    cashin_list.find_row(cashin_number)
    cashin_list.click_post_button()
    print("-" * 50)
    print(f'Cashin Add: \nCashin number: {cashin_number} \nAmount cashin: {get_amount}')


def test_cashin_add_A(driver):
    data = test_data()["data"]
    client_name = f'{data["client_name"]}-A'
    cashin_add(driver, client_name=client_name)
    print(f'Client name: "{client_name}"')
    print("-" * 50)


def test_cashin_add_B(driver):
    data = test_data()["data"]
    client_name = f'{data["client_name"]}-B'
    cashin_add(driver, client_name=client_name)
    print(f'Client name: "{client_name}"')
    print("-" * 50)


def test_cashin_add_C(driver):
    data = test_data()["data"]
    client_name = f'{data["client_name"]}-C'
    cashin_add(driver, client_name=client_name)
    print(f'Client name: "{client_name}"')
    print("-" * 50)


# ------------------------------------------------------------------------------------------------------------------

def offset_add(driver, client_name=None, payment=False):
    # Test data
    data = test_data()["data"]

    email_user = data["email_user"]
    password_user = data["password_user"]
    filial_name = data["filial_name"]
    client_name = client_name if client_name is not None else data["client_name"]
    cash_register_name = data["cash_register_name"]

    # Login
    login(driver, email_user, password_user)

    # Dashboard
    dashboard(driver)
    dashboard_page = DashboardPage(driver)
    dashboard_page.find_filial(filial_name)

    # Open Offset List
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'anor/mdeal/order/offset/offset_list')
    offset_list = OffsetList(driver)
    assert offset_list.element_visible(), 'OffsetList not open!'
    offset_list.find_row(client_name)
    offset_list.click_detail_button()

    # Offset Detail List
    offset_detail_list = OffsetDetailList(driver)
    assert offset_detail_list.element_visible(), 'OffsetDetailList not open!'
    offset_detail_list.find_row(client_name)

    if payment is False:
        offset_detail_list.click_offset_button()

        # Offset Detail List
        offset = Offset(driver)
        assert offset.element_visible(), 'Offset not open!'
        assert offset.find_row(client_name), f'Error: Automatic price button did not work'
        check_balance = offset.check_balance(client_name)
        assert check_balance == 0, f'Error: Balance is not equal to zero. -> {check_balance} != {0}'

        print("-" * 50)
        print(f'Offset Add: \nOffset balance: {check_balance}')
        offset.click_post_button()
        offset.click_close_button()
        time.sleep(2)

    if payment is True:
        offset_detail_list.click_payment_button()

        # Offset Detail List
        offset = Offset(driver)
        assert offset.element_visible(), 'Offset not open!'
        assert offset.find_row(client_name), f'Error: Automatic price button did not work'
        offset.input_cashboxes(cash_register_name)
        check_balance_payment = offset.check_balance_payment(client_name)
        offset.click_post_button()
        offset.click_yes_button()
        offset.click_close_button()

        # Cashin List
        open_new_window(driver, cut_url + 'trade/tcs/cashin_list')
        cashin_list = CashinList(driver)
        assert cashin_list.element_visible(), 'CashinList not open!'
        cashin_list.find_row(client_name)
        cashin_list.click_view_button()

        # Cashin View
        cashin_view = CashinView(driver)
        assert cashin_view.element_visible(), 'CashinView not open!'
        get_cashin_number = cashin_view.check_cashin_number()
        get_client_name = cashin_view.check_client_name()
        assert client_name == get_client_name, f'client_name: {client_name} != get_client_name: {get_client_name}'
        get_total_price = cashin_view.check_total_price()
        assert check_balance_payment == get_total_price, f'check_balance_payment: {check_balance_payment} != get_total_price: {get_total_price}'
        print("-" * 50)
        print(f'Offset Add: \nCashin Number: {get_cashin_number} \nOffset balance: {check_balance_payment}')
        cashin_view.click_close_button()


def test_offset_add_A(driver):
    data = test_data()["data"]
    client_name = f'{data["client_name"]}-A'
    offset_add(driver, client_name=client_name)
    print(f'Client name: "{client_name}"')
    print("-" * 50)


def test_offset_add_B(driver):
    data = test_data()["data"]
    client_name = f'{data["client_name"]}-B'
    offset_add(driver,
               client_name=client_name,
               payment=True)
    print(f'Client name: "{client_name}"')
    print("-" * 50)


def test_offset_add_C(driver):
    data = test_data()["data"]
    client_name = f'{data["client_name"]}-C'
    offset_add(driver, client_name=client_name)
    print(f'Client name: "{client_name}"')
    print("-" * 50)


# All ------------------------------------------------------------------------------------------------------------------

# pytest tests/test_order/test_cashin.py::test_all -v --html=report.html --self-contained-html
def test_all():
    """Cashin and Offset test runner"""
    tests = [
        # Cashin Add
        {"name": "Cashin Add-A", "func": test_cashin_add_A},
        {"name": "Cashin Add-B", "func": test_cashin_add_B},
        {"name": "Cashin Add-C", "func": test_cashin_add_C},

        # Offset Add
        {"name": "Offset Add-A", "func": test_offset_add_A},
        {"name": "Offset Add-B", "func": test_offset_add_B},
        {"name": "Offset Add-C", "func": test_offset_add_C},
    ]

    passed_tests = []
    failed_tests = []
    total_tests = len(tests)

    print("\n=== Test Execution Summary ===")

    for test in tests:
        try:
            driver = get_driver()
            if driver is None:
                raise Exception("WebDriver initialization failed")

            test['func'](driver)
            passed_tests.append(test['name'])
            print(f"✅ {test['name']}: PASSED")
            print("*" * 50)
        except Exception as e:
            failed_tests.append({"name": test['name'], "error": str(e)})
            print(f"❌ {test['name']}: FAILED")
            print(f"   Error: {str(e)}")
            print("*" * 50)
        finally:
            if driver:
                driver.quit()
            time.sleep(1)

    print("\n=== Final Results ===")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {len(passed_tests)}")
    print(f"Failed: {len(failed_tests)}")

    if failed_tests:
        print("\nFailed Tests Details:")
        for test in failed_tests:
            print(f"❌ {test['name']}")
            print(f"   Error: {test['error']}\n")

    # Agar birorta test muvaffaqiyatsiz bo'lsa, pytest uchun xatolikni ko'rsatamiz
    assert len(failed_tests) == 0, "Some tests failed"
