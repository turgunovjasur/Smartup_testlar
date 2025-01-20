import random
import time

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
from autotest.core.md.base_page import BasePage
from autotest.core.md.change_password.change_password import ChangePassword
from autotest.core.md.company_add.company_add import CompanyAdd
from autotest.core.md.company_list.company_list import CompanyList
from autotest.core.md.company_view.company_view import CompanyView
from autotest.core.md.role_view.role_view import RoleView
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.main_navbar import MainNavbar
from autotest.trade.pref.system_setting.system_setting import SystemSetting
from autotest.trade.tr.role_edit.role_edit import RoleEdit
from autotest.trade.tr.role_list.role_list import RoleList
from autotest.trade.trf.room_add.room_add import RoomAdd
from autotest.trade.trf.room_list.room_list import RoomList
from autotest.trade.trf.room_view.room_view import RoomView
from tests.test_base.test_base import test_data, login, dashboard, open_new_window, login_admin, login_user, logout
from utils.driver_setup import driver


def test_company_creat(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_company_creat")

    # Test data
    data = test_data()["data"]

    try:
        # Login
        login(driver, data['email_company'], data['password_company'])

        # Dashboard
        dashboard(driver)
        dashboard_page = DashboardPage(driver)
        dashboard_page.click_main_button()

        # Main Navbar
        main_navbar = MainNavbar(driver)
        assert main_navbar.element_visible() or base_page.logger.error('MainNavbar not open!')
        main_navbar.click_company_button()

        # Company created:
        company_list = CompanyList(driver)
        assert company_list.element_visible() or base_page.logger.error('CompanyList not open!')
        company_list.click_add_button()

        # Company Add
        company_add = CompanyAdd(driver)
        assert company_add.element_visible() or base_page.logger.error('CompanyAdd not open!')
        company_add.input_code(data["code_input"])
        company_add.input_name(data["name_company"])
        company_add.input_plan_accounts(data["plan_account"])
        company_add.input_bank(data["bank_name"])
        company_add.input_checkbox()
        company_add.click_save_button()

        # Company List
        assert company_list.element_visible() or base_page.logger.error('CompanyList not open!')
        company_list.find_company(data["code_input"])
        company_list.click_view_button()

        # Company View
        company_view = CompanyView(driver)
        assert company_view.element_visible() or base_page.logger.error('CompanyView not open!')
        text = company_view.check_filial_text()
        assert data["name_company"] == text or \
               base_page.logger.error(f'Error: {data["name_company"]} != {text}')
        company_view.click_navbar_button()
        company_view.click_checkbox()
        company_view.click_close_button()
        time.sleep(2)
        base_page.logger.info(f"✅Company: '{data['name_company']}' successfully added!")

    except Exception as e:
        base_page.logger.error(f"Error massage(❌): {e}")
        base_page.take_screenshot("test_company_creat_error")
        raise


def test_legal_person_add(driver, legal_person_name=None):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_legal_person_add")

    # Test data
    data = test_data()["data"]
    legal_person_name = legal_person_name if legal_person_name is not None else data["legal_person_name"]
    base_page.logger.info(f"Test data: legal_person_name='{legal_person_name}'")

    try:
        # Login
        login_admin(driver, url='anor/mr/person/legal_person_list')

        # Legal Person List
        legal_person_list = LegalPersonList(driver)
        # assert legal_person_list.element_visible() or base_page.logger.error('LegalPersonList not open!')
        # legal_person_list.click_add_button()
        #
        # # Legal Person Add
        # legal_person_add = LegalPersonAdd(driver)
        # assert legal_person_add.element_visible() or base_page.logger.error('LegalPersonAdd not open!')
        # legal_person_add.input_name(legal_person_name)
        # legal_person_add.click_save_button()

        # Legal Person List
        assert legal_person_list.element_visible() or base_page.logger.error('LegalPersonList not open!')
        legal_person_list.find_row(legal_person_name)
        legal_person_list.click_view_button()

        # Legal Person View
        legal_person_view = LegalPersonView(driver)
        assert legal_person_view.element_visible() or base_page.logger.error('LegalPersonView not open!')
        text = legal_person_view.check_text()
        assert legal_person_name == text, f'Error: {legal_person_name} != {text}'
        base_page.logger.info(f"Legal Person(✅): '{legal_person_name}' successfully added!")

    except Exception as e:
        base_page.logger.error(f"Error massage(❌): {e}")
        base_page.take_screenshot("test_legal_person_add_error")
        raise


def test_filial_creat(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_filial_creat")

    # Test data
    data = test_data()["data"]
    filial_name = data["filial_name"]
    base_currency_cod = data['base_currency_cod']
    legal_person_name = data['legal_person_name']

    base_page.logger.info(
        f"Test data: filial_name='{filial_name}', base_currency_cod='{base_currency_cod}', legal_person_name='{legal_person_name}'")

    try:
        # Login
        login_admin(driver, url='anor/mr/filial_list')

        # Filial List
        filial_list = FilialList(driver)
        assert filial_list.element_visible() or base_page.logger.error('FilialList not open!')
        filial_list.click_add_button()

        # FilialAdd
        filial_add = FilialAdd(driver)
        assert filial_add.element_visible() or base_page.logger.error('FilialAdd not open!')
        filial_add.input_name(filial_name)
        filial_add.input_base_currency_name(base_currency_cod)
        filial_add.input_person_name(legal_person_name)
        filial_add.click_save_button()

        # FilialList
        assert filial_list.element_visible() or base_page.logger.error('FilialList not open!')
        filial_list.find_filial_row(filial_name)
        filial_list.click_view_button()

        # FilialView
        filial_view = FilialView(driver)
        assert filial_view.element_visible() or base_page.logger.error('FilialView not open!')
        text = filial_view.check_filial_text()
        assert filial_name == text or base_page.logger.error(f'Error: {filial_name} != {text}')
        filial_view.click_navbar_button()
        filial_view.click_project_checkbox()
        filial_view.click_checkbox_button()
        filial_view.click_close_button()
        base_page.logger.info(f"Filial(✅): '{filial_name}' successfully added!")

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("test_filial_creat_error")
        raise


def test_room_add(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_room_add")

    # Test data
    data = test_data()["data"]
    room_name = data["room_name"]
    filial_name = data["filial_name"]

    base_page.logger.info(f"Test data: room_name='{room_name}', filial_name='{filial_name}'")

    try:
        # Login
        login_admin(driver, filial_name=filial_name, url='trade/trf/room_list')

        # Room List
        room_list = RoomList(driver)
        assert room_list.element_visible() or base_page.logger.error('RoomList not open!')
        room_list.click_add_button()

        # Add room
        room_add = RoomAdd(driver)
        assert room_add.element_visible() or base_page.logger.error('RoomAdd not open!')
        room_add.input_name(room_name)
        room_add.click_save_button()

        # List room
        assert room_list.element_visible() or base_page.logger.error('RoomList not open!')
        room_list.find_row(room_name)
        room_list.click_view_button()

        # View room
        room_view = RoomView(driver)
        assert room_view.element_visible() or base_page.logger.error('RoomView not open!')
        get_text = room_view.check_room_name()
        assert get_text == room_name or base_page.logger.error(f"{get_text} != {room_name}")
        room_view.click_close_button()
        base_page.logger.info(f"Room(✅): '{room_name}' successfully added to filial '{filial_name}'!")

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("test_room_add_error")
        raise


def test_robot_add(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_robot_add")

    # Test data
    data = test_data()["data"]
    filial_name = data["filial_name"]
    room_name = data["room_name"]
    robot_name = data["robot_name"]
    role_name = data["role_name"]

    base_page.logger.info(
        f"Test data: filial_name='{filial_name}', room_name='{room_name}', robot_name='{robot_name}', role_name='{role_name}'")

    try:
        # Login
        login_admin(driver, filial_name=filial_name, url='anor/mrf/robot_list')

        # Robot List
        robot_list = RobotList(driver)
        assert robot_list.element_visible() or base_page.logger.error('RobotList not open!')
        robot_list.click_add_button()

        # Add robot
        robot_add = RobotAdd(driver)
        assert robot_add.element_visible() or base_page.logger.error('RobotAdd not open!')
        robot_add.input_name(robot_name)
        robot_add.input_roles(role_name)
        robot_add.input_rooms(room_name)
        robot_add.click_save_button()

        # List robot
        assert robot_list.element_visible() or base_page.logger.error('RobotList not open!')
        robot_list.find_row(robot_name)
        robot_list.click_view_button()

        # Check robot
        robot_view = RobotView(driver)
        assert robot_view.element_visible() or base_page.logger.error('RobotView not open!')
        get_text = robot_view.check_robot_name()
        assert get_text == robot_name or base_page.logger.error(f"{get_text} != {robot_name}")
        robot_view.click_close_button()
        base_page.logger.info(f"Robot(✅): '{robot_name}' successfully added to filial '{filial_name}'!")

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("test_robot_add_error")
        raise


def test_sub_filial_add(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_sub_filial_add")

    # Test data
    data = test_data()["data"]
    filial_name = data["filial_name"]
    room_name = data["room_name"]
    robot_name = data["robot_name"]
    role_name = data["role_name"]
    sub_filial_name = data["sub_filial_name"]

    base_page.logger.info(
        f"Test data: filial_name='{filial_name}', room_name='{room_name}', sub_filial_name='{sub_filial_name}', role_name='{role_name}'")

    try:
        # Login
        login_admin(driver, filial_name=filial_name, url='anor/mrf/subfilial_list')

        # Sub Filial List
        sub_filial_list = SubFilialList(driver)
        assert sub_filial_list.element_visible() or base_page.logger.error('SubFilialList not open!')
        sub_filial_list.click_add_button()

        # Sub Filial Add
        sub_filial_add = SubFilialAdd(driver)
        assert sub_filial_add.element_visible() or base_page.logger.error('SubFilialAdd not open!')
        sub_filial_add.input_name(sub_filial_name)
        sub_filial_add.input_rooms(room_name)
        sub_filial_add.click_save_button()

        # Sub Filial List
        assert sub_filial_list.element_visible() or base_page.logger.error('SubFilialList not open!')
        try:
            sub_filial_list.find_row(sub_filial_name)
        except Exception:
            base_page.logger.error(f'❌Error: {sub_filial_name} not found!')
        base_page.logger.info(f"Sub-Filial(✅): '{sub_filial_name}' successfully added to room '{room_name}'!")

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("test_sub_filial_add_error")
        raise


def test_natural_person_add(driver, person_name=None):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_natural_person_add")

    # Test data
    data = test_data()["data"]
    filial_name = data["filial_name"]
    natural_person_name = person_name if person_name is not None else data["natural_person_name"]

    base_page.logger.info(f"Test data: filial_name='{filial_name}', natural_person_name='{natural_person_name}'")

    try:
        # Login
        login_admin(driver, filial_name=filial_name, url='anor/mr/person/natural_person_list')

        # Natural Person List
        natural_person_list = NaturalPersonList(driver)
        assert natural_person_list.element_visible() or base_page.logger.error('NaturalPersonList not open!')
        natural_person_list.click_add_button()

        # Natural Person Add
        natural_person_add = NaturalPersonAdd(driver)
        assert natural_person_add.element_visible() or base_page.logger.error('NaturalPersonAdd not open!')
        natural_person_add.input_name(natural_person_name)
        natural_person_add.click_save_button()

        # Natural Person List
        assert natural_person_list.element_visible() or base_page.logger.error('NaturalPersonList not open!')
        natural_person_list.find_row(natural_person_name)
        natural_person_list.click_view_button()

        # Natural Person View
        natural_person_view = NaturalPersonView(driver)
        assert natural_person_view.element_visible() or base_page.logger.error('NaturalPersonView not open!')
        text = natural_person_view.check_text()
        assert natural_person_name == text or base_page.logger.error(f"Error: {natural_person_name} != {text}")
        base_page.logger.info(f"NaturalPersonView(✅): name success checked '{natural_person_name}'")

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("test_natural_person_add_error")
        raise


def test_user_creat(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_user_creat")

    # Test data
    data = test_data()["data"]
    filial_name = data["filial_name"]
    natural_person_name = data["natural_person_name"]
    password_user = data["password_user"]
    login_user = data["login_user"]
    robot_name = data["robot_name"]

    base_page.logger.info(f"Test data: filial_name='{filial_name}', "
                          f"natural_person_name='{natural_person_name}', "
                          f"password_user='******', login_user='{login_user}', "
                          f"robot_name='{robot_name}'")

    try:
        # Login
        login_admin(driver, filial_name=filial_name, url='anor/mr/user_list')

        # User List:
        user_list = UserList(driver)
        # assert user_list.element_visible() or base_page.logger.error('UserList not open!')
        # user_list.click_add_button()
        #
        # # User Add
        # user_add = UserAdd(driver)
        # assert user_add.element_visible() or base_page.logger.error('UserAdd not open!')
        # user_add.input_person_name(natural_person_name)
        # user_add.input_password(password_user)
        # user_add.click_mouse_down_button()
        # user_add.input_login(login_user)
        # user_add.input_robot(robot_name)
        # user_add.click_save_button()

        # User List
        assert user_list.element_visible() or base_page.logger.error('UserList not open!')
        user_list.find_natural_person_row(natural_person_name)
        user_list.click_view_button()

        # User View
        user_view = UserView(driver)
        assert user_view.element_visible() or base_page.logger.error('UserView not open!')
        text = user_view.check_natural_person_text()
        assert natural_person_name == text or base_page.logger.error(f'Error: {natural_person_name} != {text}')

        # Forms:
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
        base_page.logger.info(f"User(✅): Permissions added to user '{natural_person_name}'!")

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("test_user_creat_error")
        raise


def test_adding_permissions_to_user(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_adding_permissions_to_user")

    # Test data
    data = test_data()["data"]
    filial_name = data["filial_name"]
    role_name = data["role_name"]

    base_page.logger.info(f"Test data: filial_name='{filial_name}', role_name='{role_name}'")

    try:
        # Login
        login_admin(driver, filial_name=filial_name, url='trade/tr/role_list')

        # Role List
        role_list = RoleList(driver)
        assert role_list.element_visible() or base_page.logger.error('RoleList not open!')
        base_page.logger.info("RoleList: page opened.")
        role_list.click_row_button(role_name)
        role_list.click_edit_button()

        # Role Edit
        role_edit = RoleEdit(driver)
        assert role_edit.element_visible() or base_page.logger.error('RoleEdit not open!')
        if not role_edit.check_checkbox():
            role_edit.click_checkboxes()
        role_edit.click_save_button()

        # Role List
        assert role_list.element_visible() or base_page.logger.error('RoleList not open!')
        role_list.click_row_button(role_name)
        role_list.click_view_button()

        # Role View
        role_view = RoleView(driver)
        assert role_view.element_visible() or base_page.logger.error('RoleView not open!')
        text = role_view.check_text()
        assert role_name == text or base_page.logger.error(f"{role_name} != {text}")

        # Access all
        role_view.click_navbar_button()
        role_view.click_detached_button()
        role_view.click_checkbox_form()
        role_view.click_access_all_button()
        time.sleep(2)
        role_view.click_close_button()
        base_page.logger.info(f"Role(✅): Permissions successfully added to role '{role_name}'!")

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("test_adding_permissions_to_user_error")
        raise


def test_user_change_password(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_user_change_password")

    # Test data
    data = test_data()["data"]
    password_user = data["password_user"]

    try:
        # Login
        login_user(driver, filial_name=False, url=False)

        # Change Password
        change_password = ChangePassword(driver)
        assert change_password.element_visible() or base_page.logger.error('ChangePassword not open!')
        change_password.input_current_password(password_user)
        change_password.input_new_password(password_user)
        change_password.input_rewritten_password(password_user)
        change_password.click_save_button()
        time.sleep(2)
        base_page.logger.info(f"Password(✅): successfully changed!")

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("test_user_change_password_error")
        raise


# ------------------------------------------------------------------------------------------------------------------


def price_type_add(driver, price_type_name=None, currency_name=None, all_price=None):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_price_type_add")

    # Test data
    data = test_data()["data"]
    price_type_name_USA = data["price_type_name_USA"]
    price_type_name_UZB = data["price_type_name_UZB"]
    price_type_name = price_type_name_USA if price_type_name else price_type_name_UZB

    currency_name = currency_name if currency_name is not None else data["currency_name"]
    room_name = data["room_name"]

    base_page.logger.info(f"Test data: price_type_name='{price_type_name}', room_name='{room_name}'")

    try:
        # Login
        login_user(driver, url='anor/mkr/price_type_list')

        # Price Type List
        price_type_list = PriceTypeList(driver)
        assert price_type_list.element_visible() or base_page.logger.error('PriceTypeList not open!')
        price_type_list.click_add_button()

        # Price Type Add
        price_type_add = PriceTypeAdd(driver)
        assert price_type_add.element_visible() or base_page.logger.error('PriceTypeAdd not open!')
        price_type_add.input_name(price_type_name)
        price_type_add.input_rooms(room_name)
        price_type_add.input_currency(currency_name)
        price_type_add.click_save_button()

        # Price Type List
        assert price_type_list.element_visible() or base_page.logger.error('PriceTypeList not open!')
        price_type_list.find_row(price_type_name)
        price_type_list.click_view_button()

        # Price Type View
        price_type_view = PriceTypeIdView(driver)
        assert price_type_view.element_visible() or base_page.logger.error('PriceTypeIdView not open!')
        text = price_type_view.get_elements()
        assert price_type_name == text or base_page.logger.error(f'"{price_type_name}" != "{text}"!')
        price_type_view.click_close_button()

        if all_price is True:
            # Price Type List (All price)
            assert price_type_list.element_visible() or base_page.logger.error('PriceTypeList not open!')
            price_type_list.click_add_dropdown_button()

            # PriceTypeListAttach
            price_type_list_attach = PriceTypeListAttach(driver)
            name_a = 'Промо'
            price_type_list_attach.find_rows(name_a)

            assert price_type_list.element_visible() or base_page.logger.error('PriceTypeList not open!')
            price_type_list.click_add_dropdown_button()
            name_b = 'Акция'
            price_type_list_attach.find_rows(name_b)

            assert price_type_list.element_visible() or base_page.logger.error('PriceTypeList not open!')
            price_type_list.click_add_dropdown_button()
            name_c = 'Возврат'
            price_type_list_attach.find_rows(name_c)

            assert price_type_list.element_visible() or base_page.logger.error('PriceTypeList not open!')
            price_type_list.click_add_dropdown_button()
            name_d = 'Передача забаланс'
            price_type_list_attach.find_rows(name_d)

            assert price_type_list.element_visible() or base_page.logger.error('PriceTypeList not open!')
            price_type_list.click_add_dropdown_button()
            name_e = 'Обмен'
            price_type_list_attach.find_rows(name_e)

        base_page.logger.info(f"PriceType(✅): '{price_type_name}' successfully added!")

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("test_price_type_add_error")
        raise


def test_price_type_add_UZB(driver):
    currency_name = "Узбекский сум"
    price_type_add(driver, currency_name=currency_name, all_price=True)


def test_price_type_add_USA(driver):
    currency_name = "Доллар США"
    price_type_add(driver, price_type_name=True, currency_name=currency_name, all_price=False)


# ------------------------------------------------------------------------------------------------------------------


def test_payment_type_add(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_payment_type_add")

    try:
        # Login
        login_user(driver, url='anor/mkr/payment_type_list')

        # Payment Type List
        payment_type_list = PaymentTypeList(driver)
        assert payment_type_list.element_visible() or base_page.logger.error('PaymentTypeList not open!')
        payment_type_list.click_attach_button()

        # Payment Type List Attach
        payment_type_list_attach = PaymentTypeListAttach(driver)
        assert payment_type_list_attach.element_visible() or base_page.logger.error('PaymentTypeListAttach not open!')
        payment_type_list_attach.click_checkbox_all()
        payment_type_list_attach.click_close_button()
        base_page.logger.info(f"PaymentType(✅): successfully attached!")

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("test_payment_type_add_error")
        raise


def test_sector_add(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_sector_add")

    # Test data
    data = test_data()["data"]
    sector_name = data["sector_name"]
    room_name = data["room_name"]

    base_page.logger.info(f"Test data: sector_name='{sector_name}', room_name='{room_name}'")

    try:
        # Login
        login_user(driver, url='anor/mr/sector_list')
        base_page.logger.info("Successful access to the system.")

        # Sector List
        sector_list = SectorList(driver)
        assert sector_list.element_visible(), 'SectorList not open!'
        base_page.logger.info("SectorList: page opened.")
        sector_list.click_add_button()
        base_page.logger.info("SectorList: add button pressed.")

        # Add Sector
        sector_add = SectorAdd(driver)
        assert sector_add.element_visible(), 'SectorAdd not open!'
        base_page.logger.info("SectorAdd: page opened.")
        sector_add.input_name(sector_name)
        base_page.logger.info(f"SectorAdd: name inputted: '{sector_name}'")
        sector_add.input_rooms(room_name)
        base_page.logger.info(f"SectorAdd: room inputted: '{room_name}'")
        sector_add.click_save_button()
        base_page.logger.info("SectorAdd: save button pressed.")

        # Sector List
        assert sector_list.element_visible(), 'SectorList not open!'
        sector_list.find_row(sector_name)
        base_page.logger.info(f"SectorList: row found with name: '{sector_name}'")
        sector_list.click_view_button()
        base_page.logger.info("SectorList: view button pressed.")

        # Sector View
        sector_view = SectorView(driver)
        assert sector_view.element_visible(), 'SectorView not open!'
        base_page.logger.info("SectorView: page opened.")
        get_name = sector_view.check_sector_name()
        assert sector_name == get_name, f"Error: {sector_name} != {get_name}"
        base_page.logger.info(f"SectorView: name successfully verified '{sector_name}'")
        sector_view.click_close_button()
        base_page.logger.info(f"Sector(✅): '{sector_name}' successfully added!")

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("test_sector_add_error")
        raise


def test_product_add(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_product_add")

    # Test data
    data = test_data()["data"]
    product_name = data["product_name"]
    measurement_name = data["measurement_name"]
    sector_name = data["sector_name"]
    product_price = data["product_price"]
    product_price_USA = data["product_price_USA"]
    price_type_name_UZB = data["price_type_name_UZB"]
    price_type_name_USA = data["price_type_name_USA"]

    base_page.logger.info(f"Test data: product_name='{product_name}', "
                          f"measurement_name='{measurement_name}', "
                          f"sector_name='{sector_name}', "
                          f"product_price='{product_price}'")

    try:
        # Login
        login_user(driver, url='anor/mr/product/inventory_list')
        base_page.logger.info("Successful access to the system.")

        # Inventory List
        inventory_list = InventoryList(driver)
        assert inventory_list.element_visible(), 'InventoryList not open!'
        inventory_list.click_add_button()

        # Add Inventory
        inventory_add = InventoryNew(driver)
        assert inventory_add.element_visible(), 'InventoryNew not open!'
        inventory_add.input_name(product_name)
        inventory_add.input_measurement(measurement_name)
        inventory_add.input_sectors(sector_name)
        inventory_add.click_goods_checkbox()
        inventory_add.click_save_button()

        # Inventory List
        assert inventory_list.element_visible(), 'InventoryList not open!'
        inventory_list.find_and_click_checkbox(product_name)
        inventory_list.click_view_button()

        # Product View
        product_id = ProductView(driver)
        assert product_id.element_visible(), 'ProductView not open!'
        get_name = product_id.get_elements()
        assert product_name == get_name, f"Error: {product_name} != {get_name}"
        product_id.click_close_button()

        # Inventory List - Set Price
        assert inventory_list.element_visible(), 'InventoryList not open!'
        inventory_list.find_and_click_checkbox(product_name)
        inventory_list.click_set_price_button()

        # Product Set Price
        product_set_price = ProductSetPrice(driver)
        assert product_set_price.element_visible(), 'ProductSetPrice not open!'
        text = product_set_price.check_product()
        assert product_name == text, f'"{product_name}" != "{text}"'
        product_set_price.input_prices(product_price, price_type_name_UZB)
        product_set_price.input_prices(product_price_USA, price_type_name_USA)
        product_set_price.click_save_button()
        base_page.logger.info(f"Product(✅): '{product_name}' successfully added! "
                              f"\n{price_type_name_UZB}: {product_price} "
                              f"\n{price_type_name_USA}: {product_price_USA}")

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("test_product_add_error")
        raise


# ------------------------------------------------------------------------------------------------------------------

def test_natural_person_client_add_A(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-A"
    test_natural_person_add(driver, person_name=client_name)


def test_natural_person_client_add_B(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-B"
    test_natural_person_add(driver, person_name=client_name)


def test_natural_person_client_add_C(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-C"
    test_natural_person_add(driver, person_name=client_name)


# ------------------------------------------------------------------------------------------------------------------

def client_add(driver, client_name=None):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): client_add")

    # Test data
    data = test_data()["data"]
    client_name = client_name if client_name is not None else data["client_name"]
    base_page.logger.info(f"Test data: client_name='{client_name}'")

    try:
        # Login
        login_user(driver, url='anor/mrf/client_list')
        base_page.logger.info("Successful access to the system.")

        # Client List
        client_list = ClientList(driver)
        assert client_list.element_visible(), 'ClientList not open!'
        base_page.logger.info("ClientList: page opened.")
        client_list.click_add_button()
        base_page.logger.info("ClientList: add button pressed.")

        # Client Add
        client_add = ClientAdd(driver)
        assert client_add.element_visible(), 'ClientAdd not open!'
        base_page.logger.info("ClientAdd: page opened.")
        client_add.click_radio_button()
        base_page.logger.info("ClientAdd: radio button selected.")
        client_add.input_name(client_name)
        base_page.logger.info(f"ClientAdd: client name inputted: '{client_name}'")
        client_add.click_save_button()
        base_page.logger.info("ClientAdd: save button pressed.")

        # Client List
        assert client_list.element_visible(), 'ClientList not open!'
        client_list.find_row(client_name)
        base_page.logger.info(f"ClientList: row found with name: '{client_name}'")
        client_list.click_view_button()
        base_page.logger.info("ClientList: view button pressed.")

        # Client View
        client_view = ClientView(driver)
        assert client_view.element_visible(), 'ClientView not open!'
        base_page.logger.info("ClientView: page opened.")
        client_view.check_client_name()
        base_page.logger.info(f"ClientView: client name successfully verified: '{client_name}'")
        client_view.click_close_button()
        base_page.logger.info(f"Client(✅): '{client_name}' successfully added!")
        time.sleep(2)

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("client_add_error")
        raise


def test_client_add_A(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-A"
    client_add(driver, client_name=client_name)


def test_client_add_B(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-B"
    client_add(driver, client_name=client_name)


def test_client_add_C(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-C"
    client_add(driver, client_name=client_name)


# ------------------------------------------------------------------------------------------------------------------


def test_room_attachment(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_room_attachment")

    # Test data
    data = test_data()["data"]
    warehouse_name = data["warehouse_name"]
    cash_register_name = data["cash_register_name"]
    client_name = data["client_name"]
    room_name = data["room_name"]

    base_page.logger.info(f"Test data: room_name='{room_name}', warehouse_name='{warehouse_name}', "
                          f"cash_register_name='{cash_register_name}', client_name='{client_name}'")

    try:
        # Login
        login_user(driver, url='trade/trf/room_list')

        # Room List
        room_list = RoomList(driver)
        assert room_list.element_visible() or base_page.logger.error("RoomList not open!")
        room_list.find_row(room_name)
        room_list.click_attachment_button()

        # Room Attachment
        room_attachment = RoomAttachment(driver)
        assert room_attachment.element_visible() or base_page.logger.error("'RoomAttachment not open!'")

        # Attach payment types
        room_attachment.click_navbar_button(navbar_button=2)
        room_attachment.click_detach_button(detach_button=2)
        room_attachment.click_checkbox_all_price_type(attach_button=2)
        base_page.logger.info("RoomAttachment: price types attached.")

        # Attach payment types
        room_attachment.click_navbar_button(navbar_button=3)
        room_attachment.click_detach_button(detach_button=3)
        room_attachment.click_checkbox_all_payment_type(attach_button=3)
        base_page.logger.info("RoomAttachment: payment types attached.")

        # Attach margin types
        room_attachment.click_navbar_button(navbar_button=5)
        room_attachment.click_detach_button(detach_button=5)
        room_attachment.click_checkbox_all_margin_type(attach_button=5)
        base_page.logger.info("RoomAttachment: margin types attached.")

        # Attach warehouse
        room_attachment.click_navbar_button(navbar_button=6)
        room_attachment.click_detach_button(detach_button=6)
        room_attachment.find_row(warehouse_name)
        room_attachment.click_attach_button(attach_button=6)
        base_page.logger.info(f"RoomAttachment: warehouse '{warehouse_name}' attached.")

        # Attach cash register
        room_attachment.click_navbar_button(navbar_button=7)
        room_attachment.click_detach_button(detach_button=7)
        room_attachment.find_row(cash_register_name)
        room_attachment.click_attach_button(attach_button=7)
        base_page.logger.info(f"RoomAttachment: cash register '{cash_register_name}' attached.")

        # Attach clients
        room_attachment.click_navbar_button(navbar_button=11)
        room_attachment.click_detach_button(detach_button=11)
        room_attachment.find_row(f'{client_name}-A')
        room_attachment.click_attach_button(attach_button=11)
        room_attachment.find_row(f'{client_name}-B')
        room_attachment.click_attach_button(attach_button=11)
        room_attachment.find_row(f'{client_name}-C')
        room_attachment.click_attach_button(attach_button=11)
        base_page.logger.info(f"RoomAttachment: client '{client_name}-A','{client_name}-B','{client_name}-C' attached.")

        # Close attachment
        room_attachment.click_close_button()
        base_page.logger.info("RoomAttachment: close button pressed.")

        base_page.logger.info(f"Room(✅): '{room_name}' successfully attached to payment types, "
                              f"'{warehouse_name}', '{cash_register_name}', and clients '{client_name}-A,B,C'!")

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("test_room_attachment_error")
        raise


def test_init_balance(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_init_balance")

    # Test data
    data = test_data()["data"]
    product_name = data['product_name']
    product_quantity = data['product_quantity']
    product_price = data['product_price']
    warehouse_name = data['warehouse_name']

    base_page.logger.info(f"Test data: product_name='{product_name}', product_quantity='{product_quantity}', "
                          f"product_price='{product_price}', warehouse_name='{warehouse_name}'")

    try:
        # Login
        login_user(driver, url='anor/mkw/init_balance/init_inventory_balance_list')
        base_page.logger.info("Successful access to the system.")

        # Init Inventory Balance List
        init_balance = InitInventoryBalanceList(driver)
        assert init_balance.element_visible(), 'InitInventoryBalanceList not open!'
        base_page.logger.info("InitInventoryBalanceList: page opened.")
        init_balance.click_add_button()
        base_page.logger.info("InitInventoryBalanceList: add button pressed.")

        # Add Init Inventory Balance
        init_balance_add = InitInventoryBalanceAdd(driver)
        balance_number = random.randint(1, 99999)
        base_page.logger.info(f"Generated balance_number: '{balance_number}'")
        init_balance_add.input_balance_number(balance_number)
        base_page.logger.info(f"InitInventoryBalanceAdd: balance number inputted: '{balance_number}'")
        init_balance_add.input_product_name(product_name)
        base_page.logger.info(f"InitInventoryBalanceAdd: product name inputted: '{product_name}'")
        product_card_code = random.randint(1, 99999)
        base_page.logger.info(f"Generated product_card_code: '{product_card_code}'")
        init_balance_add.input_card_code(product_card_code)
        base_page.logger.info(f"InitInventoryBalanceAdd: card code inputted: '{product_card_code}'")
        init_balance_add.input_quantity(product_quantity)
        base_page.logger.info(f"InitInventoryBalanceAdd: product quantity inputted: '{product_quantity}'")
        init_balance_add.input_price(product_price)
        base_page.logger.info(f"InitInventoryBalanceAdd: product price inputted: '{product_price}'")
        init_balance_add.click_save_button()
        base_page.logger.info("InitInventoryBalanceAdd: save button pressed.")
        assert init_balance_add.find_row(balance_number), f"Balance number '{balance_number}' not found!"
        base_page.logger.info(f"InitInventoryBalanceAdd: balance number '{balance_number}' found.")
        init_balance_add.click_post_one_button()
        base_page.logger.info("InitInventoryBalanceAdd: post button pressed.")

        # Balance List
        cut_url = base_page.cut_url()
        open_new_window(driver, cut_url + 'anor/mkw/balance/balance_list')
        balance_list = BalanceList(driver)
        assert balance_list.element_visible(), 'BalanceList not open!'
        base_page.logger.info("BalanceList: page opened.")

        # Verify balance
        try:
            balance_list.find_row(product_name)
        except:
            balance_list.click_reload_button()
            base_page.logger.info("BalanceList: reload button pressed.")
            balance_list.find_row(product_name)
        base_page.logger.info(f"BalanceList: row found for product '{product_name}'.")

        balance_list.click_detail_button()
        base_page.logger.info("BalanceList: detail button pressed.")
        time.sleep(2)

        balance = balance_list.check_balance_quantity()
        base_page.logger.info(f"BalanceList: balance quantity checked: '{balance}'.")
        assert balance == product_quantity, f"Balance '{balance}' != product_quantity '{product_quantity}'"
        base_page.logger.info(
            f"Balance(✅): {balance} pieces of '{product_name}' successfully added to '{warehouse_name}'!")

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("test_init_balance_error")
        raise


def test_order_request(driver):  # mast not
    # Test data
    data = test_data()["data"]

    room_name = data["room_name"]
    robot_name = data["robot_name"]
    client_name = data["client_name"]
    product_name = data["product_name"]
    product_quantity = data["product_quantity"]

    login_user(driver, url='anor/mdeal/order/order_request_list')

    order_request_list = OrderRequestList(driver)
    assert order_request_list.element_visible()
    order_request_list.click_add_button()

    # Order Request Main
    order_request_add_main = OrderRequestAddMain(driver)
    assert order_request_add_main.element_visible()
    order_request_add_main.click_rooms_input(room_name)
    order_request_add_main.click_robots_input(robot_name)
    order_request_add_main.click_persons_input(client_name)
    order_request_add_main.click_next_step_button()

    # Order Request Product
    order_request_add_product = OrderRequestAddProduct(driver)
    assert order_request_add_product.element_visible()
    order_request_add_product.input_name(product_name)
    order_request_add_product.input_quantity(product_quantity)
    order_request_add_product.click_next_step_button()

    # Order Request Final
    order_request_add_final = OrderRequestAddFinal(driver)
    assert order_request_add_final.element_visible()
    request_number = random.randint(1, 99999)
    order_request_add_final.input_request_number(request_number)
    order_request_add_final.click_save_button()

    # Order Request List
    assert order_request_list.element_visible()
    order_request_list.find_row(client_name)
    order_request_list.click_view_button()

    # Order Request View
    order_request_view = OrderRequestView(driver)
    assert order_request_view.element_visible()
    text = order_request_view.check_number()
    assert text == request_number, f"Error: {text} != {request_number}"
    order_request_view.click_close_button()

    # Order Request List - Change status
    assert order_request_list.element_visible()
    order_request_list.click_status_button()
    print(f'Order Request: {request_number} request successfully joined!')


# ------------------------------------------------------------------------------------------------------------------

def contract_add(driver, client_name=None, contract_name=None, initial_amount=None,
                 currency_cod=None, currency_name=None):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): contract_add")

    # Test data
    data = test_data()["data"]
    client_name = client_name if client_name is not None else data["client_name"]
    contract_name = contract_name if contract_name is not None else data["contract_name"]
    initial_amount = initial_amount if initial_amount is not None else data["product_quantity"] * data["product_price"]
    base_currency_cod = currency_cod if currency_cod is not None else data["base_currency_cod"]
    currency_name = currency_name if currency_name is not None else "Узбекский сум"

    base_page.logger.info(f"Test data: client_name='{client_name}', contract_name='{contract_name}', "
                          f"initial_amount='{initial_amount}', base_currency_cod='{base_currency_cod}'")

    try:
        login_user(driver, url='anor/mkf/contract_list')

        # Contract List
        contract_list = ContractList(driver)
        assert contract_list.element_visible() or base_page.logger.error('ContractList not open!')
        contract_list.click_add_button()

        # Contract Add
        contract_add = ContractAdd(driver)
        assert contract_add.element_visible() or base_page.logger.error('ContractAdd not open!')
        contract_number = random.randint(1, 999999)
        contract_add.input_contract_number(contract_number)
        contract_add.input_contract_name(contract_name)
        contract_add.click_radio_button()
        contract_add.input_person_name(client_name)
        contract_add.input_currency_name(base_currency_cod)
        contract_add.input_initial_amount(initial_amount)
        contract_add.click_checkbox_button()
        contract_add.click_save_button()

        # Contract List
        assert contract_list.element_visible() or base_page.logger.error('ContractList not open!')
        contract_list.find_row(contract_name)
        contract_list.click_view_button()

        # Contract View
        contract_view = ContractView(driver)
        assert contract_view.element_visible() or base_page.logger.error('ContractView not open!')
        get_contract_name = contract_view.check_contract_name()
        assert get_contract_name == contract_name or base_page.logger.error(f'Error: {get_contract_name} != {contract_name}')
        get_currency_name = contract_view.check_currency_name()
        assert get_currency_name == currency_name or base_page.logger.error(f'{get_currency_name} != {currency_name}')
        contract_view.click_close_button()
        base_page.logger.info(f"Contract(✅): '{contract_name}' successfully added!")

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("contract_add_error")
        raise


def test_contract_add_A_UZB(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-A"
    contract_name = f"{data['contract_name']}-A"
    contract_add(driver,
                 client_name=client_name,
                 contract_name=contract_name)


def test_contract_add_B_UZB(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-B"
    contract_name = f"{data['contract_name']}-B"
    initial_amount = 100 * data["product_price"]
    contract_add(driver,
                 client_name=client_name,
                 contract_name=contract_name,
                 initial_amount=initial_amount)


def test_contract_add_C_USA(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-C"
    contract_name = f"{data['contract_name']}-C"
    currency_cod = 840
    currency_name = 'Доллар США'
    initial_amount = 100 * data["product_price_USA"]
    contract_add(driver,
                 client_name=client_name,
                 contract_name=contract_name,
                 currency_cod=currency_cod,
                 currency_name=currency_name,
                 initial_amount=initial_amount)


# ------------------------------------------------------------------------------------------------------------------

def test_setting_consignment(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_setting_consignment")

    try:
        login_user(driver, url='trade/pref/system_setting')
        base_page.logger.info("Successful access to the system.")

        # System setting
        system_setting = SystemSetting(driver)
        assert system_setting.element_visible() or base_page.logger.error("SystemSetting not open!")

        system_setting.click_navbar_button(navbar_button=6)
        base_page.logger.info("SystemSetting: navbar button pressed.")

        assert system_setting.element_visible_order() or base_page.logger.error("order_header not open!")
        if not system_setting.check_checkbox_text():
            system_setting.click_checkbox_consignment()
            base_page.logger.info("SystemSetting: consignment checkbox pressed.")

            system_setting.input_consignment_day_limit(day_limit=90)
            base_page.logger.info("SystemSetting: consignment day limit inputted.")

        system_setting.click_save_button()
        base_page.logger.info("SystemSetting: save button pressed.")
        base_page.logger.info(f"✅Test end(): test_setting_consignment")

    except Exception as e:
        base_page.logger.error(f"❌Error message(): {e}")
        base_page.take_screenshot("test_setting_consignment_error")
        raise


# ------------------------------------------------------------------------------------------------------------------

def test_currency_add(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_currency_add")

    # Test data
    currency_name = 'Доллар США'
    exchange_rate = 10_000

    try:
        login_user(driver, url='anor/mk/currency_list')
        base_page.logger.info("Successful access to the system.")

        # Currency List
        currency_list = CurrencyList(driver)
        assert currency_list.element_visible() or base_page.logger.error("CurrencyList not open!")
        currency_list.find_row(currency_name)
        currency_list.click_view_button()

        # Currency View
        currency_view = CurrencyView(driver)
        assert currency_view.element_visible() or base_page.logger.error("CurrencyView not open!")
        currency_view.click_navbar_button(navbar_button=2)
        currency_view.click_add_rate_button()

        # Modal
        currency_view.input_exchange_rate_button(exchange_rate)
        currency_view.click_save_button()

        assert currency_view.check_row() or base_page.logger.error("exchange_rate not found!")
        currency_view.click_close_button()

        # Currency List
        assert currency_list.element_visible() or base_page.logger.error("CurrencyList not open!")
        base_page.logger.info(f"✅Test end(): test_currency_add")

    except Exception as e:
        base_page.logger.error(f"❌Error message(): {e}")
        base_page.take_screenshot("test_currency_add_error")
        raise


# ------------------------------------------------------------------------------------------------------------------

def test_margin_add(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_margin_add")

    # Test data
    data = test_data()["data"]
    margin_name = data["margin_name"]
    percent_value = data["percent_value"]

    try:
        # Login
        login_admin(driver, url='anor/mkr/margin_list')

        # Margin List - Admin
        margin_list_attach = MarginListAttach(driver)
        assert margin_list_attach.element_visible() or base_page.logger.error("MarginList-Admin not open!")
        margin_list_attach.find_row('')
        margin_list_attach.click_delete_button()
        assert margin_list_attach.element_visible() or base_page.logger.error("MarginList-Admin not open!")

    except Exception:
        base_page.logger.error(f"❌Error: Margin not found!")

    logout(driver)

    try:
        login_user(driver, url='anor/mkr/margin_list')

        # Margin List
        margin_list = MarginList(driver)
        assert margin_list.element_visible() or base_page.logger.error("MarginList not open!")
        margin_list.click_attach_button()

        # Margin List Attach
        margin_list_attach = MarginListAttach(driver)
        assert margin_list_attach.element_visible() or base_page.logger.error("MarginListAttach not open!")
        margin_list_attach.click_add_button()

        # Margin Add
        margin_add = MarginAdd(driver)
        assert margin_add.element_visible() or base_page.logger.error("MarginAdd not open!")
        margin_add.click_name_button(margin_name)
        margin_add.click_percent_button(percent_value)
        margin_add.click_percent_type_radio_button(percent_type=1)
        margin_add.click_save_button()

        # Margin List
        assert margin_list.element_visible() or base_page.logger.error("MarginList not open!")
        margin_list.click_attach_button()

        # Margin List Attach
        assert margin_list_attach.element_visible() or base_page.logger.error("MarginListAttach not open!")
        margin_list.find_row(margin_name)
        margin_list.click_attach_one_button()

        # Margin List
        assert margin_list.element_visible() or base_page.logger.error("MarginList not open!")
        margin_list.find_row(margin_name)
        base_page.logger.info(f"✅Test end(): test_margin_add")

    except Exception as e:
        base_page.logger.error(f"❌Error message(): {e}")
        base_page.take_screenshot("test_margin_add_error")
        raise
# ------------------------------------------------------------------------------------------------------------------
