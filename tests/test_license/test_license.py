from datetime import date
import pytest
from autotest.biruni.kl.license_list.license_list import LicenseList
from autotest.core.md.base_page import BasePage
from autotest.core.md.login_page import LoginPage
from flows.auth_flow import login_admin, login
from tests.test_license.flow_license import balance_flow, document_flow, attach_user_flow, purchase_flow, \
    get_modal_content_flow

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order(9)
def test_check_user_license(driver, test_data):
    data = test_data["data"]

    login(driver, email=data["email_user"], password=data["password_user"])

    login_page = LoginPage(driver)
    login_page.element_visible_retry_button()
    login_page.click_back_button()

    login(driver, email=data["email"], password=data["password"])

    base_page = BasePage(driver)
    base_page.switch_window(direction="prepare")
    cut_url = base_page.cut_url()
    base_page.switch_window(direction="new", url=cut_url + 'biruni/kl/license_list')

    test_add_user_license(driver, test_data, login_system=False)

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order(9)
def test_add_user_license(driver, test_data, login_system=True):
    """Test configuring add user license."""

    if test_data["data"]["url"] != "https://smartup.online/login.html":
        pytest.skip("⚠️ Faqat Online saytida ishlaydi")

    data = test_data["data"]
    natural_person_name = data['natural_person_name']

    if login_system:
        login_admin(driver, test_data, url='biruni/kl/license_list')

    balance_flow(driver, navbar_name="Лицензии и документы")

    document_flow(driver, element_name="ERP users", data="13.12.2024")

    attach_user_flow(driver, find_row=natural_person_name)

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order(9)
def test_add_purchase_license(driver, test_data, assertions):
    login_admin(driver, test_data, url='biruni/kl/license_list')

    balance_flow(driver, navbar_name="Покупка")

    today = date.today()
    begin_date = today.strftime("%d%m%Y")  # 22.08.2025

    purchase_flow(driver,
                  payer_name="TEST GWS FIZIK",
                  contract_name="Договор № bn от 01.01.2025",
                  begin_date=begin_date,
                  license_count=1)

    _list = LicenseList(driver)
    get_purchase_balance = _list.get_purchase_balance()
    get_purchase_total_amount = _list.get_purchase_total_amount()
    after_purchase_balance = get_purchase_balance - get_purchase_total_amount

    get_modal_content_flow(driver)

    get_payer_balance_new = balance_flow(driver, navbar_name="Баланс", payer_name="TEST GWS FIZIK")
    assertions.assert_equals(actual=get_payer_balance_new,
                             expected=after_purchase_balance,
                             message="License: Payer balance -> after purchase")

# ======================================================================================================================