import os
import random
import re
import time
import pytest
from datetime import datetime, timedelta

from autotest.anor.mdeal.order.order_add.order_request_add.order_request_add_final import OrderRequestAddFinal
from autotest.anor.mdeal.order.order_add.order_request_add.order_request_add_main import OrderRequestAddMain
from autotest.anor.mdeal.order.order_add.order_request_add.order_request_add_product import OrderRequestAddProduct
from autotest.anor.mdeal.order.order_add.order_request_view.order_request_view import OrderRequestView
from autotest.anor.mdeal.order.order_request_list.order_request_list import OrderRequestList
from autotest.anor.mk.currency_list.currency_list import CurrencyList
from autotest.anor.mk.currency_view.currency_view import CurrencyView
from autotest.anor.mkf.contract_add.contract_add import ContractAdd
from autotest.anor.mkf.contract_list.contract_list import ContractList
from autotest.anor.mkf.contract_view.contract_view import ContractView
from autotest.anor.mkr.margin_add.margin_add import MarginAdd
from autotest.anor.mkr.margin_list.margin_list import MarginList
from autotest.anor.mkr.margin_list_attach.margin_list_attach import MarginListAttach
from autotest.anor.mkr.payment_type_list.payment_type_list import PaymentTypeList
from autotest.anor.mkr.payment_type_list_attach.payment_type_list_attach import PaymentTypeListAttach
from autotest.anor.mkr.price_tag.price_tag import PriceTag
from autotest.anor.mkr.price_type_add.price_type_add import PriceTypeAdd
from autotest.anor.mkr.price_type_list.price_type_list import PriceTypeList
from autotest.anor.mkr.price_type_list_attach.price_type_list_attch import PriceTypeListAttach
from autotest.anor.mkr.price_type_view.price_type_id import PriceTypeIdView
from autotest.anor.mkw.balance.balance_list.balance_list import BalanceList
from autotest.anor.mkw.init_balance.init_inventory_balance_add.init_inventory_balance_add import InitInventoryBalanceAdd
from autotest.anor.mkw.init_balance.init_inventory_balance_list.init_inventory_balance_list import \
    InitInventoryBalanceList
from autotest.anor.mr.filial_add.filial_add import FilialAdd
from autotest.anor.mr.filial_list.filial_list import FilialList
from autotest.anor.mr.filial_view.filial_view import FilialView
from autotest.anor.mr.person.legal_person_add.legal_person_add import LegalPersonAdd
from autotest.anor.mr.person.legal_person_list.legal_person_list import LegalPersonList
from autotest.anor.mr.person.legal_person_view.legal_person_view import LegalPersonView
from autotest.anor.mr.person.natural_person_add.natural_person_add import NaturalPersonAdd
from autotest.anor.mr.person.natural_person_list.natural_person_list import NaturalPersonList
from autotest.anor.mr.person.natural_person_view.natural_person_view import NaturalPersonView
from autotest.anor.mr.product.inventory_add.inventory_new import InventoryNew
from autotest.anor.mr.product.inventory_list.inventory_list import InventoryList
from autotest.anor.mr.product.inventory_view.product_id import ProductId as ProductView
from autotest.anor.mr.product.product_set_price.product_set_price import ProductSetPrice
from autotest.anor.mr.sector_add.sector_add import SectorAdd
from autotest.anor.mr.sector_list.sector_list import SectorList
from autotest.anor.mr.sector_view.sector_view import SectorView
from autotest.anor.mr.user_add.user_add import UserAdd
from autotest.anor.mr.user_list.user_list import UserList
from autotest.anor.mr.user_view.user_view import UserView
from autotest.anor.mrf.client_add.client_add import ClientAdd
from autotest.anor.mrf.client_list.client_list import ClientList
from autotest.anor.mrf.client_view.client_view import ClientView
from autotest.anor.mrf.robot_add.robot_add import RobotAdd
from autotest.anor.mrf.robot_list.robot_list import RobotList
from autotest.anor.mrf.robot_view.robot_view import RobotView
from autotest.anor.mrf.room_attachment.room_attachment import RoomAttachment
from autotest.anor.mrf.subfilial_add.subfilial_add import SubFilialAdd
from autotest.anor.mrf.subfilial_list.subfilial_list import SubFilialList
from autotest.biruni.kl.license_list.license_list import LicenseList
from autotest.biruni.kl.license_user_list.license_user_list import LicenseUserList
from autotest.biruni.md.biruni.grid_setting.grid_setting import GridSetting
from autotest.core.md.base_page import BasePage
from autotest.core.md.change_password.change_password import ChangePassword
from autotest.core.md.company_add.company_add import CompanyAdd
from autotest.core.md.company_list.company_list import CompanyList
from autotest.core.md.company_view.company_view import CompanyView
from autotest.core.md.role_view.role_view import RoleView
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.main_navbar import MainNavbar
from autotest.trade.pref.system_setting.system_setting import SystemSetting
from autotest.trade.tdeal.order.order_list.orders_page import OrdersList
from autotest.trade.tr.role_edit.role_edit import RoleEdit
from autotest.trade.tr.role_list.role_list import RoleList
from autotest.trade.trf.room_add.room_add import RoomAdd
from autotest.trade.trf.room_list.room_list import RoomList
from autotest.trade.trf.room_view.room_view import RoomView
from tests.conftest import test_data
from tests.test_base.test_base import login, dashboard, login_admin, login_user, logout
from utils.driver_setup import driver
from utils.exception import log_exception_chain
from utils.screen_recorder import ScreenRecorder


def test_company_creat(driver, test_data):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_company_creat")

    # Test data
    data = test_data["data"]

    try:
        # Login
        login_admin(driver, test_data, data['email_company'], data['password_company'])

        # Dashboard
        dashboard(driver)
        dashboard_page = DashboardPage(driver)
        dashboard_page.click_main_button()

        # Main Navbar
        main_navbar = MainNavbar(driver)
        assert main_navbar.element_visible(), 'MainNavbar not open!'
        base_page.logger.info('MainNavbar successfully opened.')
        main_navbar.click_company_button()

        # Company List
        company_list = CompanyList(driver)
        assert company_list.element_visible(), 'CompanyList not open!'
        base_page.logger.info('CompanyList successfully opened.')
        company_list.click_add_button()

        # Company Add
        company_add = CompanyAdd(driver)
        assert company_add.element_visible(), 'CompanyAdd not open!'
        base_page.logger.info('CompanyAdd successfully opened.')
        company_add.input_code(data["code_input"])
        company_add.input_name(data["name_company"])
        company_add.input_plan_accounts(data["plan_account"])
        company_add.input_bank(data["bank_name"])
        company_add.input_checkbox()
        company_add.click_save_button()

        # Verify Company List
        assert company_list.element_visible(), 'CompanyList not open after save!'
        company_list.find_company(data["code_input"])
        company_list.click_view_button()

        # Company View
        company_view = CompanyView(driver)
        assert company_view.element_visible(), 'CompanyView not open!'
        text = company_view.check_filial_text()
        assert data["name_company"] == text, f'Expected company name "{data["name_company"]}", but got "{text}"'
        base_page.logger.info(f"Company name verified: '{data['name_company']}'")

        company_view.click_navbar_button()
        company_view.click_checkbox()
        company_view.click_close_button()
        base_page.logger.info(f"✅ Company '{data['name_company']}' successfully added!")

    except AssertionError as ae:
        base_page.logger.error(f'AssertionError: {str(ae)}')
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f'Unexpected error: {str(e)}')
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_legal_person_add(driver, test_data, legal_person_name=None):
    """Test adding a legal person"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_legal_person_add")

    # Test data
    data = test_data["data"]
    legal_person_name = legal_person_name or data["legal_person_name"]
    base_page.logger.info(f"Data: name='{legal_person_name}'")

    try:
        # Login
        login_admin(driver, test_data, url='anor/mr/person/legal_person_list')

        # Open Legal Person List
        legal_person_list = LegalPersonList(driver)
        assert legal_person_list.element_visible(), "LegalPersonList not open!"
        # legal_person_list.click_add_button()

        # Add Legal Person
        legal_person_add = LegalPersonAdd(driver)
        assert legal_person_add.element_visible(), "LegalPersonAdd not open!"

        legal_person_add.input_name(legal_person_name)
        tin_number = random.randint(1, 999999999)
        legal_person_add.input_tin(tin_number)
        legal_person_add.click_save_button()

        # Verify in List
        assert legal_person_list.element_visible(), "LegalPersonList not open after save!"
        legal_person_list.find_row(legal_person_name)
        legal_person_list.click_view_button()

        # Verify in View
        legal_person_view = LegalPersonView(driver)
        assert legal_person_view.element_visible(), "LegalPersonView not open!"
        text = legal_person_view.check_text()

        assert legal_person_name == text, f'Expected "{legal_person_name}", got "{text}"'
        base_page.logger.info(f"✅ Verified: '{legal_person_name}'")

    except AssertionError as ae:
        base_page.logger.error(f'❌ AssertionError: {str(ae)}')
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f'❌ Error: {str(e)}')
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_filial_create(driver, test_data):
    """Test adding a filial"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_filial_create")

    # Test data
    data = test_data["data"]
    filial_name = data["filial_name"]
    currency_code = data["base_currency_cod"]
    legal_person = data["legal_person_name"]

    try:
        # Login
        login_admin(driver, test_data, url='anor/mr/filial_list')

        # Open Filial List
        filial_list = FilialList(driver)
        assert filial_list.element_visible(), "FilialList not open!"
        filial_list.click_add_button()

        # Add Filial
        filial_add = FilialAdd(driver)
        assert filial_add.element_visible(), "FilialAdd not open!"
        filial_add.input_name(filial_name)
        filial_add.input_base_currency_name(currency_code)
        filial_add.input_person_name(legal_person)
        filial_add.click_save_button()

        # Verify in List
        assert filial_list.element_visible(), "FilialList not open after save!"
        filial_list.find_filial_row(filial_name)
        filial_list.click_view_button()

        # Verify in View
        filial_view = FilialView(driver)
        assert filial_view.element_visible(), "FilialView not open!"
        text = filial_view.check_filial_text()
        assert filial_name == text, f'Expected "{filial_name}", got "{text}"'

        filial_view.click_navbar_button()
        filial_view.click_project_checkbox()
        filial_view.click_checkbox_button()
        filial_view.click_close_button()

        base_page.logger.info(f"✅ Filial '{filial_name}' added successfully!")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_room_add(driver, test_data):
    """Test adding a room"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_room_add")

    # Test data
    data = test_data["data"]
    room_name = data["room_name"]
    filial_name = data["filial_name"]

    try:
        # Login
        login_admin(driver, test_data, filial_name=filial_name, url='trade/trf/room_list')

        # Open Room List
        room_list = RoomList(driver)
        assert room_list.element_visible(), "RoomList not open!"
        room_list.click_add_button()

        # Add Room
        room_add = RoomAdd(driver)
        assert room_add.element_visible(), "RoomAdd not open!"
        room_add.input_name(room_name)
        room_add.click_save_button()

        # Verify in List
        assert room_list.element_visible(), "RoomList not open after save!"
        room_list.find_row(room_name)
        room_list.click_view_button()

        # Verify in View
        room_view = RoomView(driver)
        assert room_view.element_visible(), "RoomView not open!"
        text = room_view.check_room_name()
        assert text == room_name, f'Expected "{room_name}", got "{text}"'
        room_view.click_close_button()

        base_page.logger.info(f"✅ Room '{room_name}' added successfully!")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_robot_add(driver, test_data):
    """Test adding a robot"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_robot_add")

    # Test data
    data = test_data["data"]
    filial_name = data["filial_name"]
    room_name = data["room_name"]
    robot_name = data["robot_name"]
    role_name = data["role_name"]
    # role_name = "Экспедитор"

    try:
        # Login
        login_admin(driver, test_data, filial_name=filial_name, url='anor/mrf/robot_list')

        # Open Robot List
        robot_list = RobotList(driver)
        assert robot_list.element_visible(), "RobotList not open!"
        robot_list.click_add_button()

        # Add Robot
        robot_add = RobotAdd(driver)
        assert robot_add.element_visible(), "RobotAdd not open!"
        robot_add.input_name(robot_name)
        robot_add.input_roles(role_name)
        robot_add.input_rooms(room_name)
        robot_add.click_save_button()

        # Verify in List
        assert robot_list.element_visible(), "RobotList not open after save!"
        robot_list.find_row(robot_name)
        robot_list.click_view_button()

        # Verify in View
        robot_view = RobotView(driver)
        assert robot_view.element_visible(), "RobotView not open!"
        text = robot_view.check_robot_name()
        assert text == robot_name, f'Expected "{robot_name}", got "{text}"'
        robot_view.click_close_button()
        base_page.logger.info(f"✅ Robot '{robot_name}' added successfully!")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_sub_filial_add(driver, test_data):
    """Test adding a sub-filial"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_sub_filial_add")

    # Test data
    data = test_data["data"]
    filial_name = data["filial_name"]
    room_name = data["room_name"]
    sub_filial_name = data["sub_filial_name"]

    try:
        # Login
        login_admin(driver, test_data, filial_name=filial_name, url='anor/mrf/subfilial_list')

        # Open Sub-Filial List
        sub_filial_list = SubFilialList(driver)
        assert sub_filial_list.element_visible(), "SubFilialList not open!"
        sub_filial_list.click_add_button()

        # Add Sub-Filial
        sub_filial_add = SubFilialAdd(driver)
        assert sub_filial_add.element_visible(), "SubFilialAdd not open!"
        sub_filial_add.input_name(sub_filial_name)
        sub_filial_add.input_rooms(room_name)
        sub_filial_add.click_save_button()

        # Verify in List
        assert sub_filial_list.element_visible(), "SubFilialList not open after save!"
        sub_filial_list.click_reload_button()
        sub_filial_list.find_row(sub_filial_name)

        base_page.logger.info(f"✅ Sub-Filial '{sub_filial_name}' added successfully!")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_natural_person_add(driver, test_data, person_name=None):
    """Test adding a natural person"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_natural_person_add")

    # Test data
    data = test_data["data"]
    filial_name = data["filial_name"]
    natural_person_name = person_name or data["natural_person_name"]

    try:
        # Login
        login_admin(driver, test_data, filial_name=filial_name, url='anor/mr/person/natural_person_list')

        # Open Natural Person List
        natural_person_list = NaturalPersonList(driver)
        assert natural_person_list.element_visible(), "NaturalPersonList not open!"
        natural_person_list.click_add_button()

        # Add Natural Person
        natural_person_add = NaturalPersonAdd(driver)
        assert natural_person_add.element_visible(), "NaturalPersonAdd not open!"
        natural_person_add.input_name(natural_person_name)
        natural_person_add.click_save_button()

        # Verify in List
        assert natural_person_list.element_visible(), "NaturalPersonList not open after save!"
        natural_person_list.find_row(natural_person_name)
        natural_person_list.click_view_button()

        # Verify in View
        natural_person_view = NaturalPersonView(driver)
        assert natural_person_view.element_visible(), "NaturalPersonView not open!"
        text = natural_person_view.check_text()
        assert text == natural_person_name, f'Expected "{natural_person_name}", got "{text}"'

        base_page.logger.info(f"✅ Natural Person '{natural_person_name}' added successfully!")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_user_create(driver, test_data):
    """Test adding a user"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_user_create")

    # Test data
    data = test_data["data"]
    filial_name = data["filial_name"]
    natural_person_name = data["natural_person_name"]
    password_user = data["password_user"]
    login_user = data["login_user"]
    robot_name = data["robot_name"]

    try:
        # Login
        login_admin(driver, test_data, filial_name=filial_name, url='anor/mr/user_list')

        # Open User List
        user_list = UserList(driver)
        assert user_list.element_visible(), "UserList not open!"
        user_list.click_add_button()

        # Add User
        user_add = UserAdd(driver)
        assert user_add.element_visible(), "UserAdd not open!"
        user_add.input_person_name(natural_person_name)
        user_add.input_password(password_user)
        user_add.click_mouse_down_button()
        user_add.input_login(login_user)
        user_add.input_robot(robot_name)
        user_add.click_save_button()

        # Verify in List
        assert user_list.element_visible(), "UserList not open after save!"
        user_list.find_natural_person_row(natural_person_name)
        user_list.click_view_button()

        # Verify in View
        user_view = UserView(driver)
        assert user_view.element_visible(), "UserView not open!"
        text = user_view.check_natural_person_text()
        assert text == natural_person_name, f'Expected "{natural_person_name}", got "{text}"'

        # Attach permissions
        user_view.click_navbar_button(navbar_button=2)

        user_view.click_tablist_button(tablist_button=1)
        user_view.click_detached_button(detached_button=1)
        user_view.attach_forms()

        user_view.click_tablist_button(tablist_button=2)
        user_view.click_detached_button(detached_button=1)
        user_view.attach_forms()

        user_view.click_tablist_button(tablist_button=3)
        user_view.click_detached_button(detached_button=1)
        user_view.attach_forms()

        user_view.click_tablist_button(tablist_button=5)
        user_view.click_detached_button(detached_button=1)
        user_view.attach_forms()

        user_view.click_close_button()

        base_page.logger.info(f"✅ User '{natural_person_name}' created successfully!")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_adding_permissions_to_user(driver, test_data):
    """Test adding permissions to a user"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_adding_permissions_to_user")

    # Test data
    data = test_data["data"]
    filial_name = data["filial_name"]
    role_name = data["role_name"]

    try:
        # Login
        login_admin(driver, test_data, filial_name=filial_name, url='trade/tr/role_list')

        # Open Role List
        role_list = RoleList(driver)
        assert role_list.element_visible(), "RoleList not open!"
        role_list.click_row_button(role_name)
        role_list.click_edit_button()

        # Edit Role
        role_edit = RoleEdit(driver)
        assert role_edit.element_visible(), "RoleEdit not open!"
        if not role_edit.check_checkbox():
            role_edit.click_checkboxes()
        role_edit.click_save_button()

        # Verify in List
        assert role_list.element_visible(), "RoleList not open after save!"
        role_list.click_row_button(role_name)
        role_list.click_view_button()

        # Verify in View
        role_view = RoleView(driver)
        assert role_view.element_visible(), "RoleView not open!"
        text = role_view.check_text()
        assert text == role_name, f'Expected "{role_name}", got "{text}"'

        # Grant all permissions
        role_view.click_navbar_button()
        role_view.click_detached_button()
        role_view.click_checkbox_form()
        role_view.click_access_all_button()
        time.sleep(2)
        role_view.click_close_button()

        base_page.logger.info(f"✅ Permissions added to role '{role_name}' successfully!")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_user_change_password(driver, test_data):
    """Test changing user password"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_user_change_password")

    # Test data
    data = test_data["data"]
    password_user = data["password_user"]

    try:
        # Login
        login_user(driver, test_data, filial_name=False, url=False)

        # Change Password
        change_password = ChangePassword(driver)
        assert change_password.element_visible(), "ChangePassword not open!"
        change_password.input_current_password(password_user)
        change_password.input_new_password(password_user)
        change_password.input_rewritten_password(password_user)
        change_password.click_save_button()
        time.sleep(2)

        base_page.logger.info(f"✅ Password changed successfully!")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


# ----------------------------------------------------------------------------------------------------------------------


def price_type_add(driver, test_data, price_type_name=None, currency_name=None, all_price=False,
                   sub_filial=False, sub_filial_name=None):
    """Test adding a price type"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: price_type_add")

    # Test data
    data = test_data["data"]
    room_name = data["room_name"]
    price_type_name_UZB = data["price_type_name_UZB"]
    price_type_name_USA = data["price_type_name_USA"]
    price_type_name = price_type_name_USA if price_type_name else price_type_name_UZB
    currency_name = currency_name or data["currency_name"]
    sub_filial_name = sub_filial_name or data["sub_filial_name"]

    try:
        # Login
        login_user(driver, test_data, url='anor/mkr/price_type_list')

        # Open Price Type List
        price_type_list = PriceTypeList(driver)
        assert price_type_list.element_visible(), "PriceTypeList not open!"
        price_type_list.click_add_button()

        # Add Price Type
        price_type_add = PriceTypeAdd(driver)
        assert price_type_add.element_visible(), "PriceTypeAdd not open!"
        price_type_add.input_name(price_type_name)
        price_type_add.input_rooms(room_name)
        price_type_add.input_currency(currency_name)
        if sub_filial:
            price_type_add.input_sub_filial(sub_filial_name)
        price_type_add.click_save_button()

        # Verify in List
        assert price_type_list.element_visible(), "PriceTypeList not open after save!"
        price_type_list.find_row(price_type_name)
        price_type_list.click_view_button()

        # Verify in View
        price_type_view = PriceTypeIdView(driver)
        assert price_type_view.element_visible(), "PriceTypeIdView not open!"
        text = price_type_view.get_elements()
        assert text == price_type_name, f'Expected "{price_type_name}", got "{text}"'
        price_type_view.click_close_button()

        if all_price:
            # Attach additional price types
            assert price_type_list.element_visible(), "PriceTypeList not open!"
            price_type_list.click_add_dropdown_button()

            # Attach price types
            price_type_list_attach = PriceTypeListAttach(driver)

            name_a = 'Промо'
            price_type_list_attach.find_rows(name_a)

            assert price_type_list.element_visible(), "PriceTypeList not open! after (Промо)"
            price_type_list.click_add_dropdown_button()
            name_b = 'Акция'
            price_type_list_attach.find_rows(name_b)

            assert price_type_list.element_visible(), "PriceTypeList not open! after (Акция)"
            price_type_list.click_add_dropdown_button()
            name_c = 'Возврат'
            price_type_list_attach.find_rows(name_c)

            assert price_type_list.element_visible(), "PriceTypeList not open! after (Возврат)"
            price_type_list.click_add_dropdown_button()
            name_d = 'Передача забаланс'
            price_type_list_attach.find_rows(name_d)

            assert price_type_list.element_visible(), "PriceTypeList not open! after (Передача забаланс)"
            price_type_list.click_add_dropdown_button()
            name_e = 'Обмен'
            price_type_list_attach.find_rows(name_e)

            assert price_type_list.element_visible(), "PriceTypeList not open! after (Обмен)"
            price_type_list.find_row(price_type_name)

        base_page.logger.info(f"✅ Price Type '{price_type_name}' added successfully!")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_price_type_add_UZB(driver, test_data):
    """Test adding a UZB price type"""

    currency_name = "Узбекский сум"
    price_type_add(driver, test_data, currency_name=currency_name, all_price=True)


def test_price_type_add_USA(driver, test_data):
    """Test adding a USA price type"""

    currency_name = "Доллар США"
    price_type_add(driver, test_data, price_type_name=True, sub_filial=True, currency_name=currency_name)


# ------------------------------------------------------------------------------------------------------------------


def test_payment_type_add(driver, test_data):
    """Test adding payment types"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_payment_type_add")

    try:
        # Login
        login_user(driver, test_data, url='anor/mkr/payment_type_list')

        # Open Payment Type List
        payment_type_list = PaymentTypeList(driver)
        assert payment_type_list.element_visible(), "PaymentTypeList not open!"
        payment_type_list.click_attach_button()

        # Attach Payment Types
        payment_type_list_attach = PaymentTypeListAttach(driver)
        assert payment_type_list_attach.element_visible(), "PaymentTypeListAttach not open!"
        payment_type_list_attach.click_checkbox_all()
        payment_type_list_attach.click_close_button()

        base_page.logger.info("✅ Payment types successfully attached!")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_sector_add(driver, test_data):
    """Test adding a sector"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_sector_add")

    # Test data
    data = test_data["data"]
    sector_name = data["sector_name"]
    room_name = data["room_name"]

    try:
        # Login
        login_user(driver, test_data, url='anor/mr/sector_list')

        # Open Sector List
        sector_list = SectorList(driver)
        assert sector_list.element_visible(), "SectorList not open!"
        sector_list.click_add_button()

        # Add Sector
        sector_add = SectorAdd(driver)
        assert sector_add.element_visible(), "SectorAdd not open!"
        sector_add.input_name(sector_name)
        sector_add.input_rooms(room_name)
        sector_add.click_save_button()

        # Verify in List
        assert sector_list.element_visible(), "SectorList not open after save!"
        sector_list.find_row(sector_name)
        sector_list.click_view_button()

        # Verify in View
        sector_view = SectorView(driver)
        assert sector_view.element_visible(), "SectorView not open!"
        text = sector_view.check_sector_name()
        assert text == sector_name, f'Expected "{sector_name}", got "{text}"'
        sector_view.click_close_button()

        base_page.logger.info(f"✅ Sector '{sector_name}' added successfully!")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_product_add(driver, test_data):
    """Test adding a product"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_product_add")

    # Test data
    data = test_data["data"]
    product_name = data["product_name"]
    measurement_name = data["measurement_name"]
    sector_name = data["sector_name"]
    product_price = data["product_price"]
    product_price_USA = data["product_price_USA"]
    price_type_name_UZB = data["price_type_name_UZB"]
    price_type_name_USA = data["price_type_name_USA"]

    try:
        # Login
        login_user(driver, test_data, url='anor/mr/product/inventory_list')

        # Open Inventory List
        inventory_list = InventoryList(driver)
        assert inventory_list.element_visible(), "InventoryList not open!"
        inventory_list.click_add_button()

        # Add Product (Inventory)
        inventory_add = InventoryNew(driver)
        assert inventory_add.element_visible(), "InventoryNew not open!"
        inventory_add.input_name(product_name)
        inventory_add.input_sectors(sector_name)
        inventory_add.input_measurement(measurement_name)
        inventory_add.click_goods_checkbox()
        inventory_add.click_save_button()

        # Checking error message
        error_code = inventory_add.error_massage()
        if error_code:
            base_page.logger.warning(f"⚠️ Xatolik aniqlandi!")
            assert error_code == data["error_massage_4"], f'Nomalum xatolik! -> "{error_code}"'
            base_page.refresh_page()
        else:
            base_page.logger.info("✅ Hech qanday xatolik yoq! -> Product saqlandi.")

        # Verify in List
        assert inventory_list.element_visible(), "InventoryList not open after save!"
        inventory_list.find_and_click_checkbox(product_name)
        inventory_list.click_view_button()

        # Verify in View
        product_view = ProductView(driver)
        assert product_view.element_visible(), "ProductView not open!"
        text = product_view.get_elements()
        assert text == product_name, f'Expected "{product_name}", got "{text}"'
        product_view.click_close_button()

        # Set Price
        assert inventory_list.element_visible(), "InventoryList not open!"
        inventory_list.find_and_click_checkbox(product_name)
        inventory_list.click_set_price_button()

        # Open Set Price Page
        product_set_price = ProductSetPrice(driver)
        assert product_set_price.element_visible(), "ProductSetPrice not open!"
        text = product_set_price.check_product()
        assert text == product_name, f'Expected "{product_name}", got "{text}"'
        product_set_price.input_prices(product_price, price_type_name_UZB)
        product_set_price.input_prices(product_price_USA, price_type_name_USA)
        product_set_price.click_save_button()

        base_page.logger.info(f"✅ Product '{product_name}' added successfully with prices:"
                              f" {price_type_name_UZB} = {product_price},"
                              f" {price_type_name_USA} = {product_price_USA}")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_check_price_tag(driver, test_data, minute_tolerance=1):
    """Test checking a price tag"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: check_price_tag")

    # Test data
    data = test_data["data"]
    product_name = data["product_name"]
    price_type_name = data["price_type_name_UZB"]
    price_tag_name = data["price_tag_name"]


    try:
        # Login
        login_user(driver, test_data, url='anor/mkr/price_type_list')

        # Price Type List
        price_type_list = PriceTypeList(driver)
        assert price_type_list.element_visible(), "PriceTypeList not open!"
        price_type_list.find_row(price_type_name)
        price_type_list.click_price_tag_button()

        # Price Tag
        price_tag = PriceTag(driver)
        assert price_tag.element_visible(), "PriceTag not open!"
        price_tag.input_product_name(product_name)

        # Hozirgi vaqtni oldin olish
        report_request_time = datetime.now()
        time.sleep(1)

        price_tag.click_run_button()
        time.sleep(3)

        downloads_path = os.path.join(os.environ["USERPROFILE"], "Downloads")

        # Yuklangan fayllarni olish va tekshirish
        files = os.listdir(downloads_path)
        files = [os.path.join(downloads_path, f) for f in files if f.endswith('.xlsx')]
        files.sort(key=os.path.getctime, reverse=True)

        latest_file = files[0] if files else None
        assert latest_file is not None, "❌ Price Tag file not download!"

        file_name = os.path.basename(latest_file)

        base_page.logger.info(f"✅ Loaded filename: {file_name}")

        # Regex
        regex_pattern = rf"{price_tag_name}\((\d{{2}}\.\d{{2}}\.\d{{4}})\+(\d{{2}}_\d{{2}}(?:_\d{{2}})?)\)\.xlsx"
        base_page.logger.info(f"🔎 Checked regex: {regex_pattern}")

        match = re.search(regex_pattern, file_name)
        assert match, f"❌ File name != regex: {file_name}"

        file_date = match.group(1)  # 04.03.2025
        file_time = match.group(2)  # 12_33 yoki 12_33_11
        file_time = file_time[:5]  # Sekundni olib tashlaymiz (faqat HH:MM qoldiramiz)

        file_datetime_str = f"{file_date} {file_time.replace('_', ':')}"  # "04.03.2025 12:33"
        file_datetime = datetime.strptime(file_datetime_str, "%d.%m.%Y %H:%M")

        lower_bound = report_request_time - timedelta(minutes=minute_tolerance)
        upper_bound = report_request_time + timedelta(minutes=minute_tolerance)

        base_page.logger.info(f"Checked time interval: {lower_bound.strftime('%d.%m.%Y %H:%M')} - {upper_bound.strftime('%d.%m.%Y %H:%M')}")
        base_page.logger.info(f"File time: {file_datetime.strftime('%d.%m.%Y %H:%M')}")

        assert lower_bound <= file_datetime <= upper_bound, (
            f"❌ Downloaded file time incorrect: {file_datetime}, expected range: "
            f"{lower_bound.strftime('%d.%m.%Y %H:%M')} - {upper_bound.strftime('%d.%m.%Y %H:%M')}")

        base_page.logger.info(f"✅ Last loaded file: {latest_file} (time is right)")
        base_page.logger.info(f"✅Test end: check_price_tag")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_currency_add(driver, test_data):
    """Test adding a currency exchange rate"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_currency_add")

    # Test data
    currency_name = "Доллар США"
    exchange_rate = 10_000

    try:
        # Login
        login_user(driver, test_data, url='anor/mk/currency_list')

        # Open Currency List
        currency_list = CurrencyList(driver)
        assert currency_list.element_visible(), "CurrencyList not open!"
        currency_list.find_row(currency_name)
        currency_list.click_view_button()

        # Open Currency View
        currency_view = CurrencyView(driver)
        assert currency_view.element_visible(), "CurrencyView not open!"
        currency_view.click_navbar_button(navbar_button=2)
        currency_view.click_add_rate_button()

        # Add Exchange Rate
        currency_view.input_exchange_rate_button(exchange_rate)
        currency_view.click_save_button()

        # Verify Exchange Rate
        assert currency_view.check_row(), "Exchange rate not found!"
        currency_view.click_close_button()

        base_page.logger.info(f"✅ Exchange rate for '{currency_name}' set to {exchange_rate} successfully!")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_margin_add(driver, test_data):
    """Test adding a margin"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_margin_add")

    # Test data
    data = test_data["data"]
    margin_name = data["margin_name"]
    percent_value = data["percent_value"]

    try:
        # Login as Admin
        login_admin(driver, test_data, url='anor/mkr/margin_list')

        # Open Margin List - Admin
        margin_list_attach = MarginListAttach(driver)
        assert margin_list_attach.element_visible(), "MarginList-Admin not open!"
        margin_list_attach.find_row('')
        margin_list_attach.click_delete_button()
        assert margin_list_attach.element_visible(), "MarginList-Admin not open!"

        logout(driver)

        # Login
        login_user(driver, test_data, url='anor/mkr/margin_list')

        # Open Margin List
        margin_list = MarginList(driver)
        assert margin_list.element_visible(), "MarginList not open!"
        margin_list.click_attach_button()

        # Open Margin List Attach
        margin_list_attach = MarginListAttach(driver)
        assert margin_list_attach.element_visible(), "MarginListAttach not open!"
        margin_list_attach.click_add_button()

        # Add Margin
        margin_add = MarginAdd(driver)
        assert margin_add.element_visible(), "MarginAdd not open!"
        margin_add.click_name_button(margin_name)
        margin_add.click_percent_button(percent_value)
        margin_add.click_percent_type_radio_button(percent_type=1)
        margin_add.click_save_button()

        # Verify in List
        assert margin_list.element_visible(), "MarginList not open after save!"
        margin_list.click_attach_button()

        # Attach Margin
        assert margin_list_attach.element_visible(), "MarginListAttach not open!"
        margin_list.find_row(margin_name)
        margin_list.click_attach_one_button()

        # Final Verification
        assert margin_list.element_visible(), "MarginList not open after attach!"
        margin_list.find_row(margin_name)

        base_page.logger.info(f"✅ Margin '{margin_name}' with {percent_value}% added successfully!")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


# ----------------------------------------------------------------------------------------------------------------------

def test_natural_person_client_add_A(driver, test_data):
    """Test adding natural person client A"""

    data = test_data["data"]
    client_name = f"{data['client_name']}-A"
    test_natural_person_add(driver, test_data, person_name=client_name)


def test_natural_person_client_add_B(driver, test_data):
    """Test adding natural person client B"""

    data = test_data["data"]
    client_name = f"{data['client_name']}-B"
    test_natural_person_add(driver, test_data, person_name=client_name)


def test_natural_person_client_add_C(driver, test_data):
    """Test adding natural person client C"""

    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    test_natural_person_add(driver, test_data, person_name=client_name)


# ----------------------------------------------------------------------------------------------------------------------

def client_add(driver, test_data, client_name=None):
    """Test adding a client"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: client_add")

    # Test data
    data = test_data["data"]
    client_name = client_name or data["client_name"]

    try:
        # Login
        login_user(driver, test_data, url='anor/mrf/client_list')

        # Open Client List
        client_list = ClientList(driver)
        assert client_list.element_visible(), "ClientList not open!"
        client_list.click_add_button()

        # Add Client
        client_add = ClientAdd(driver)
        assert client_add.element_visible(), "ClientAdd not open!"
        client_add.click_radio_button()
        client_add.input_name(client_name)
        client_add.click_save_button()

        # Verify in List
        assert client_list.element_visible(), "ClientList not open after save!"
        client_list.find_row(client_name)
        client_list.click_view_button()

        # Verify in View
        client_view = ClientView(driver)
        assert client_view.element_visible(), "ClientView not open!"
        client_view.check_client_name()
        client_view.click_close_button()

        base_page.logger.info(f"✅ Client '{client_name}' added successfully!")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_client_add_A(driver, test_data):
    """Test adding client A"""

    data = test_data["data"]
    client_name = f"{data['client_name']}-A"
    client_add(driver, test_data, client_name=client_name)


def test_client_add_B(driver, test_data):
    """Test adding client B"""

    data = test_data["data"]
    client_name = f"{data['client_name']}-B"
    client_add(driver, test_data, client_name=client_name)


def test_client_add_C(driver, test_data):
    """Test adding client C"""

    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    client_add(driver, test_data, client_name=client_name)


# ----------------------------------------------------------------------------------------------------------------------


def test_room_attachment(driver, test_data):
    """Test attaching different elements to a room."""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_room_attachment")

    # Test data
    data = test_data["data"]
    warehouse_name = data["warehouse_name"]
    cash_register_name = data["cash_register_name"]
    client_name = data["client_name"]
    room_name = data["room_name"]

    base_page.logger.info(f"Test data: room_name='{room_name}', warehouse_name='{warehouse_name}', "
                          f"cash_register_name='{cash_register_name}', client_name='{client_name}'")

    try:
        # Login
        login_user(driver, test_data, url='trade/trf/room_list')

        # Room List
        room_list = RoomList(driver)
        assert room_list.element_visible(), "RoomList not open!"
        room_list.find_row(room_name)
        room_list.click_attachment_button()

        # Room Attachment
        room_attachment = RoomAttachment(driver)
        assert room_attachment.element_visible(), "RoomAttachment not open!"

        # Attach payment types
        room_attachment.click_navbar_button(navbar_button=2)
        room_attachment.click_detach_button(detach_button=2)
        room_attachment.click_checkbox_all_price_type(attach_button=2)

        # Attach payment types
        room_attachment.click_navbar_button(navbar_button=3)
        room_attachment.click_detach_button(detach_button=3)
        room_attachment.click_checkbox_all_payment_type(attach_button=3)

        # Attach margin types
        room_attachment.click_navbar_button(navbar_button=5)
        room_attachment.click_detach_button(detach_button=5)
        room_attachment.click_checkbox_all_margin_type(attach_button=5)

        # Attach warehouse
        room_attachment.click_navbar_button(navbar_button=6)
        room_attachment.click_detach_button(detach_button=6)
        room_attachment.find_row(warehouse_name)
        room_attachment.click_attach_button(attach_button=6)

        # Attach cash register
        room_attachment.click_navbar_button(navbar_button=7)
        room_attachment.click_detach_button(detach_button=7)
        room_attachment.find_row(cash_register_name)
        room_attachment.click_attach_button(attach_button=7)

        # Attach clients
        room_attachment.click_navbar_button(navbar_button=11)
        room_attachment.click_detach_button(detach_button=11)
        room_attachment.find_row(f'{client_name}-A')
        room_attachment.click_attach_button(attach_button=11)
        room_attachment.find_row(f'{client_name}-B')
        room_attachment.click_attach_button(attach_button=11)
        room_attachment.find_row(f'{client_name}-C')
        room_attachment.click_attach_button(attach_button=11)

        # Close attachment
        room_attachment.click_close_button()

        base_page.logger.info(f"✅ Room '{room_name}' successfully attached.")

    except AssertionError as ae:
        base_page.logger.error(f'❌ AssertionError: {str(ae)}')
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        base_page.logger.error(f'❌ Error: {str(e)}')
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_init_balance(driver, test_data):
    """Test initializing inventory balance."""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_init_balance")

    # Test data
    data = test_data["data"]
    product_name = data['product_name']
    product_quantity = data['product_quantity']
    product_price = data['product_price']
    warehouse_name = data['warehouse_name']

    base_page.logger.info(f"Test data: product_name='{product_name}', product_quantity='{product_quantity}', "
                          f"product_price='{product_price}', warehouse_name='{warehouse_name}'")

    try:
        # Login
        login_user(driver, test_data, url='anor/mkw/init_balance/init_inventory_balance_list')

        # Open Init Inventory Balance List
        init_balance_list = InitInventoryBalanceList(driver)
        assert init_balance_list.element_visible(), "InitInventoryBalanceList not open!"
        init_balance_list.click_add_button()

        # Add Init Inventory Balance
        init_balance_add = InitInventoryBalanceAdd(driver)
        balance_number = random.randint(1, 99999)
        init_balance_add.input_balance_number(balance_number)
        init_balance_add.input_product_name(product_name)
        product_card_code = random.randint(1, 99999)
        init_balance_add.input_card_code(product_card_code)
        init_balance_add.input_quantity(product_quantity)
        init_balance_add.input_price(product_price)
        init_balance_add.click_save_button()

        # Open Init Inventory Balance List
        assert init_balance_list.element_visible(), "InitInventoryBalanceList not open!"
        init_balance_list.click_reload_button()
        init_balance_list.find_row(balance_number)
        init_balance_list.click_post_one_button()

        # Open Balance List
        cut_url = base_page.cut_url()
        base_page.open_new_window(cut_url + 'anor/mkw/balance/balance_list')

        balance_list = BalanceList(driver)
        assert balance_list.element_visible(), "BalanceList not open!"
        balance_list.click_reload_button()
        balance_list.find_row(product_name)
        balance_list.click_detail_button()
        time.sleep(2)

        balance = balance_list.check_balance_quantity()
        assert balance == product_quantity, f"Error: Balance '{balance}' != product_quantity '{product_quantity}'"

        base_page.logger.info(
            f"✅ Balance successfully updated: {balance} pieces of '{product_name}' in '{warehouse_name}'.")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        base_page.logger.error(f"❌ Unexpected error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_setting_consignment(driver, test_data):
    """Test enabling consignment settings."""

    base_page = BasePage(driver)
    system_setting = SystemSetting(driver)
    base_page.logger.info("▶️ Running: test_setting_consignment")

    try:
        # Login
        login_user(driver, test_data, url='trade/pref/system_setting')

        # Open System Setting
        assert system_setting.element_visible(), "SystemSetting not open!"
        system_setting.click_navbar_button(navbar_button=6)

        # Configure Consignment
        assert system_setting.element_visible_order(), "Order header not open!"
        if not system_setting.check_checkbox_text():
            system_setting.click_checkbox_consignment()
            system_setting.input_consignment_day_limit(day_limit=90)

        # Save Settings
        system_setting.click_save_button()

        base_page.logger.info("✅ Consignment settings successfully configured.")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        base_page.logger.error(f"❌ Unexpected error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_order_request(driver, test_data):
    """Test creating an order request."""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_order_request")

    # Test data
    data = test_data["data"]
    room_name = data["room_name"]
    robot_name = data["robot_name"]
    client_name = data["client_name"]
    product_name = data["product_name"]
    product_quantity = data["product_quantity"]

    base_page.logger.info(f"Test data: room_name='{room_name}', robot_name='{robot_name}', "
                          f"client_name='{client_name}', product_name='{product_name}', quantity='{product_quantity}'")

    try:
        # Login
        login_user(driver, test_data, url='anor/mdeal/order/order_request_list')

        # Open Order Request List
        order_request_list = OrderRequestList(driver)
        assert order_request_list.element_visible(), "OrderRequestList not open!"
        order_request_list.click_add_button()

        # Open Order Request Main
        order_request_add_main = OrderRequestAddMain(driver)
        assert order_request_add_main.element_visible(), "OrderRequestAddMain not open!"
        order_request_add_main.click_rooms_input(room_name)
        order_request_add_main.click_robots_input(robot_name)
        order_request_add_main.click_persons_input(client_name)
        order_request_add_main.click_next_step_button()

        # Open Order Request Product
        order_request_add_product = OrderRequestAddProduct(driver)
        assert order_request_add_product.element_visible(), "OrderRequestAddProduct not open!"
        order_request_add_product.input_name(product_name)
        order_request_add_product.input_quantity(product_quantity)
        order_request_add_product.click_next_step_button()

        # Open Order Request Final
        order_request_add_final = OrderRequestAddFinal(driver)
        assert order_request_add_final.element_visible(), "OrderRequestAddFinal not open!"
        request_number = random.randint(1, 99999)
        order_request_add_final.input_request_number(request_number)
        order_request_add_final.click_save_button()

        # Verify in Order Request List
        assert order_request_list.element_visible(), "OrderRequestList not open after save!"
        order_request_list.find_row(client_name)
        order_request_list.click_view_button()

        # Verify in Order Request View
        order_request_view = OrderRequestView(driver)
        assert order_request_view.element_visible(), "OrderRequestView not open!"
        text = order_request_view.check_number()
        assert text == request_number, f"Error: {text} != {request_number}"
        order_request_view.click_close_button()

        # Change status in Order Request List
        assert order_request_list.element_visible(), "OrderRequestList not open after view!"
        order_request_list.click_status_button()

        base_page.logger.info(f"✅ Order request '{request_number}' successfully created.")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        base_page.logger.error(f"❌ Unexpected error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


# ----------------------------------------------------------------------------------------------------------------------

def contract_add(driver, test_data, client_name=None, contract_name=None, initial_amount=None,
                 currency_cod=None, currency_name=None, sub_filial_name=None, sub_filial=False):
    """Test adding a contract."""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: contract_add")

    # Test data
    data = test_data["data"]
    client_name = client_name or data["client_name"]
    contract_name = contract_name or data["contract_name"]
    initial_amount = initial_amount or data["product_quantity"] * data["product_price"]
    base_currency_cod = currency_cod or data["base_currency_cod"]
    currency_name = currency_name or "Узбекский сум"
    sub_filial_name = sub_filial_name or data["sub_filial_name"]

    base_page.logger.info(f"Test data: client_name='{client_name}', contract_name='{contract_name}', "
                          f"initial_amount='{initial_amount}', base_currency_cod='{base_currency_cod}',"
                          f" sub_filial_name='{sub_filial_name}'")

    try:
        # Login
        login_user(driver, test_data, url='anor/mkf/contract_list')

        # Open Contract List
        contract_list = ContractList(driver)
        assert contract_list.element_visible(), "ContractList not open!"
        contract_list.click_add_button()

        # Open Contract Add
        contract_add = ContractAdd(driver)
        assert contract_add.element_visible(), "ContractAdd not open!"
        contract_number = random.randint(1, 999999)
        contract_add.input_contract_number(contract_number)
        contract_add.input_contract_name(contract_name)
        contract_add.click_radio_button()
        contract_add.input_person_name(client_name)
        contract_add.input_currency_name(base_currency_cod)
        contract_add.input_initial_amount(initial_amount)
        if sub_filial:
            contract_add.input_sub_filial(sub_filial_name)
        contract_add.click_is_main_checkbox()
        contract_add.click_save_button()

        # Verify in Contract List
        assert contract_list.element_visible(), "ContractList not open after save!"
        contract_list.find_row(contract_name)
        contract_list.click_view_button()

        # Verify in Contract View
        contract_view = ContractView(driver)
        assert contract_view.element_visible(), "ContractView not open!"
        get_contract_name = contract_view.check_contract_name()
        assert get_contract_name == contract_name, f"Error: {get_contract_name} != {contract_name}"
        get_currency_name = contract_view.check_currency_name()
        assert get_currency_name == currency_name, f"Error: {get_currency_name} != {currency_name}"
        contract_view.click_close_button()

        base_page.logger.info(f"✅ Contract '{contract_name}' successfully added. Contract Number: {contract_number}")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        base_page.logger.error(f"❌ Unexpected error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_add_contract_for_client_A_UZB(driver, test_data):
    """Test adding a contract for Client A in UZB currency."""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_contract_for_client_A_UZB")

    data = test_data["data"]
    client_name = f"{data['client_name']}-A"
    contract_name = f"{data['contract_name']}-A-UZB"
    contract_add(driver, test_data,
                 client_name=client_name,
                 contract_name=contract_name)


def test_add_contract_for_client_B_UZB(driver, test_data):
    """Test adding a contract for Client B in UZB currency with a higher initial amount."""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_contract_for_client_B_UZB")

    data = test_data["data"]
    client_name = f"{data['client_name']}-B"
    contract_name = f"{data['contract_name']}-B-UZB"
    initial_amount = 100 * data["product_price"]
    contract_add(driver, test_data,
                 client_name=client_name,
                 contract_name=contract_name,
                 initial_amount=initial_amount)


def test_add_contract_for_client_C_USA(driver, test_data):
    """Test adding a contract for Client C in USA currency."""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_contract_for_client_C_USA")

    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    contract_name = f"{data['contract_name']}-C-USA"
    currency_cod = 840
    currency_name = 'Доллар США'
    initial_amount = 100 * data["product_price_USA"]
    contract_add(driver, test_data,
                 client_name=client_name,
                 contract_name=contract_name,
                 currency_cod=currency_cod,
                 currency_name=currency_name,
                 initial_amount=initial_amount,
                 sub_filial=True)


# ----------------------------------------------------------------------------------------------------------------------

def setting_prepayment(driver, test_data, prepayment=True):
    """Test enabling and configuring prepayment settings."""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_setting_prepayment")

    # Test data
    data = test_data["data"]
    status_name = data['Delivered']

    system_setting = SystemSetting(driver)
    try:
        login_user(driver, test_data, url='trade/pref/system_setting')

        # System setting
        assert system_setting.element_visible(), "SystemSetting not open!"
        system_setting.click_navbar_button(navbar_button=6)
        assert system_setting.element_visible_order(), "order_navbar not open!"
        if prepayment:
            if not system_setting.check_checkbox_prepayment():
                system_setting.click_checkbox_prepayment()
                system_setting.input_prepayment(status_name)
                system_setting.input_prepayment_min_percent(payment_min_percent=50)
        if not prepayment:
            if system_setting.check_checkbox_prepayment():
                system_setting.click_checkbox_prepayment()
        system_setting.click_save_button()
        assert system_setting.element_visible_order(), "order_navbar not open!"
        base_page.logger.info(f"✅Test end: test_setting_prepayment ")

    except AssertionError as ae:
        base_page.logger.error(f'Assertion error: {str(ae)}')
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        base_page.logger.error(f"❌ Unexpected error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_setting_prepayment_on(driver, test_data):
    """Prepayment setting on"""

    setting_prepayment(driver, test_data, prepayment=True)


def test_setting_prepayment_off(driver, test_data):
    """Prepayment setting off"""

    setting_prepayment(driver, test_data, prepayment=False)


# ----------------------------------------------------------------------------------------------------------------------

def grid_setting(driver, test_data):
    """Test configuring grid settings."""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: grid_setting")

    # Test data
    option_name = "deal_id"

    try:
        login_user(driver, test_data, url='trade/tdeal/order/order_list')

        # Orders List
        order_list = OrdersList(driver)
        assert order_list.element_visible(), 'OrdersList not open!'
        order_list.click_group_button()

        # Grid Setting
        grid_setting = GridSetting(driver)
        assert grid_setting.element_visible(), 'GridSetting not open!'
        grid_setting.click_options_button(option_name)
        grid_setting.click_save_button()

        # Orders List
        assert order_list.element_visible(), 'OrdersList not open after save!'
        order_list.check_header_option(option_name)

        base_page.logger.info(f"✅Test end: grid_setting")

    except AssertionError as ae:
        log_exception_chain(base_page.logger, ae)
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        log_exception_chain(base_page.logger, e)
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_grid_setting(driver, test_data):
    """Grid setting"""

    grid_setting(driver, test_data)

# ----------------------------------------------------------------------------------------------------------------------

def test_add_user_license(driver, test_data):
    """Test configuring add user license."""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_user_license")

    # Test data
    data = test_data["data"]
    natural_person_name = data['natural_person_name']

    try:
        login_admin(driver, test_data, url='biruni/kl/license_list')

        # License List
        license_list = LicenseList(driver)
        assert license_list.element_visible(), 'LicenseList not open!'
        license_list.click_navbar_button()

        assert license_list.licence_visible(), 'License and Document not open!'
        license_list.click_tbl_row_button()
        license_list.click_bind_user_button()

        # License User List
        license_user_list = LicenseUserList(driver)
        assert license_user_list.element_visible(), 'LicenseUserList not open!'
        license_user_list.click_all_checkbox()

        assert license_user_list.element_visible(), 'LicenseUserList not open after user detach!'
        license_user_list.click_detach_button()

        assert license_user_list.attach_button_visible(), 'LicenseUserList not open! (Available users)'
        license_user_list.find_row(natural_person_name)
        license_user_list.click_attach_button()
        assert license_user_list.attach_button_visible(), 'LicenseUserList not open after attach user! (Available users)'

        base_page.logger.info(f"✅Test end: test_add_user_license ")

    except AssertionError as ae:
        log_exception_chain(base_page.logger, ae)
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        log_exception_chain(base_page.logger, e)
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))
# ----------------------------------------------------------------------------------------------------------------------

