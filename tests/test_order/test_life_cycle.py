import random
import time
import logging

from autotest.anor.mdeal.order.order_add.order_request_add.order_request_add_final import OrderRequestAddFinal
from autotest.anor.mdeal.order.order_add.order_request_add.order_request_add_main import OrderRequestAddMain
from autotest.anor.mdeal.order.order_add.order_request_add.order_request_add_product import OrderRequestAddProduct
from autotest.anor.mdeal.order.order_add.order_request_view.order_request_view import OrderRequestView
from autotest.anor.mdeal.order.order_request_list.order_request_list import OrderRequestList
from autotest.anor.mkf.contract_add.contract_add import ContractAdd
from autotest.anor.mkf.contract_list.contract_list import ContractList
from autotest.anor.mkf.contract_view.contract_view import ContractView
from autotest.anor.mkr.payment_type_list.payment_type_list import PaymentTypeList
from autotest.anor.mkr.payment_type_list_attach.payment_type_list_attach import PaymentTypeListAttach
from autotest.anor.mkr.price_type_add.price_type_add import PriceTypeAdd
from autotest.anor.mkr.price_type_list.price_type_list import PriceTypeList
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
from autotest.core.md.base_page import BasePage
from autotest.core.md.change_password.change_password import ChangePassword
from autotest.core.md.company_add.company_add import CompanyAdd
from autotest.core.md.company_list.company_list import CompanyList
from autotest.core.md.company_view.company_view import CompanyView
from autotest.core.md.role_view.role_view import RoleView
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.main_navbar import MainNavbar
from autotest.trade.tr.role_edit.role_edit import RoleEdit
from autotest.trade.tr.role_list.role_list import RoleList
from autotest.trade.trf.room_add.room_add import RoomAdd
from autotest.trade.trf.room_list.room_list import RoomList
from autotest.trade.trf.room_view.room_view import RoomView
from tests.test_base.test_base import test_data, login, dashboard, open_new_window, login_admin, login_user
from utils.driver_setup import driver


def test_company_creat(driver):
    # Test data
    data = test_data()["data"]

    # Login
    login(driver, data['email_company'], data['password_company'])

    # Dashboard
    dashboard(driver)
    dashboard_page = DashboardPage(driver)
    dashboard_page.click_main_button()

    # MainNavbar
    time.sleep(2)
    main_navbar = MainNavbar(driver)
    assert main_navbar.element_visible(), 'MainNavbar not open!'
    main_navbar.click_company_button()

    # Company created:
    time.sleep(2)
    company_list = CompanyList(driver)
    assert company_list.element_visible(), 'CompanyList not open!'
    company_list.click_add_button()

    # CompanyAdd
    time.sleep(2)
    company_add = CompanyAdd(driver)
    assert company_add.element_visible(), 'CompanyAdd not open!'
    company_add.input_code(data["code_input"])
    company_add.input_name(data["name_company"])
    company_add.input_plan_accounts(data["plan_account"])
    company_add.input_bank(data["bank_name"])
    company_add.input_checkbox()
    company_add.click_save_button()

    # CompanyList
    time.sleep(2)
    assert company_list.element_visible(), 'CompanyList not open!'
    company_list.find_company(data["code_input"])
    company_list.click_view_button()

    # CompanyView
    time.sleep(2)
    company_view = CompanyView(driver)
    assert company_view.element_visible(), 'CompanyView not open!'
    text = company_view.check_filial_text()
    assert data["name_company"] == text, f'Error: {data["name_company"]} != {text}'
    company_view.click_navbar_button()
    company_view.click_checkbox()
    company_view.click_close_button()
    time.sleep(2)
    print(f"Company: '{data['name_company']}' successfully added!")


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
        base_page.logger.info("Successful access to the system.")

        # Legal Person List
        legal_person_list = LegalPersonList(driver)
        assert legal_person_list.element_visible(), 'LegalPersonList not open!'
        base_page.logger.info("LegalPersonList: page opened.")
        legal_person_list.click_add_button()
        base_page.logger.info("LegalPersonList: add button pressed.")

        # Legal Person Add
        legal_person_add = LegalPersonAdd(driver)
        assert legal_person_add.element_visible(), 'LegalPersonAdd not open!'
        base_page.logger.info("LegalPersonAdd: page opened.")
        legal_person_add.input_name(legal_person_name)
        base_page.logger.info(f"LegalPersonAdd: name inputted: '{legal_person_name}'")
        legal_person_add.click_save_button()
        base_page.logger.info("LegalPersonAdd: save button pressed.")

        # Legal Person List
        assert legal_person_list.element_visible(), 'LegalPersonList not open!'
        legal_person_list.find_row(legal_person_name)
        base_page.logger.info(f"LegalPersonList: row found with name: '{legal_person_name}'")
        legal_person_list.click_view_button()
        base_page.logger.info("LegalPersonList: view button pressed.")

        # Legal Person View
        legal_person_view = LegalPersonView(driver)
        assert legal_person_view.element_visible(), 'LegalPersonView not open!'
        base_page.logger.info("LegalPersonView: page opened.")
        text = legal_person_view.check_text()
        assert legal_person_name == text, f'Error: {legal_person_name} != {text}'
        base_page.logger.info(f"LegalPersonView: name success checked '{legal_person_name}'")
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
        base_page.logger.info("Successful access to the system.")

        # Filial List
        filial_list = FilialList(driver)
        assert filial_list.element_visible(), 'FilialList not open!'
        base_page.logger.info("FilialList: page opened.")
        filial_list.click_add_button()
        base_page.logger.info("FilialList: add button pressed.")

        # FilialAdd
        filial_add = FilialAdd(driver)
        assert filial_add.element_visible(), 'FilialAdd not open!'
        base_page.logger.info("FilialAdd: page opened.")
        filial_add.input_name(filial_name)
        base_page.logger.info(f"FilialAdd: name inputted: '{filial_name}'")
        filial_add.input_base_currency_name(base_currency_cod)
        base_page.logger.info(f"FilialAdd: base currency code inputted: '{base_currency_cod}'")
        filial_add.input_person_name(legal_person_name)
        base_page.logger.info(f"FilialAdd: legal person name inputted: '{legal_person_name}'")
        filial_add.click_save_button()
        base_page.logger.info("FilialAdd: save button pressed.")

        # FilialList
        assert filial_list.element_visible(), 'FilialList not open!'
        filial_list.find_filial_row(filial_name)
        base_page.logger.info(f"FilialList: row found with name: '{filial_name}'")
        filial_list.click_view_button()
        base_page.logger.info("FilialList: view button pressed.")

        # FilialView
        filial_view = FilialView(driver)
        assert filial_view.element_visible(), 'FilialView not open!'
        base_page.logger.info("FilialView: page opened.")
        text = filial_view.check_filial_text()
        assert filial_name == text, f'Error: {filial_name} != {text}'
        base_page.logger.info(f"FilialView: name success checked '{filial_name}'")
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
        base_page.logger.info("Successful access to the system.")

        # Room List
        room_list = RoomList(driver)
        assert room_list.element_visible(), 'RoomList not open!'
        base_page.logger.info("RoomList: page opened.")
        room_list.click_add_button()
        base_page.logger.info("RoomList: add button pressed.")

        # Add room
        room_add = RoomAdd(driver)
        assert room_add.element_visible(), 'RoomAdd not open!'
        base_page.logger.info("RoomAdd: page opened.")
        room_add.input_name(room_name)
        base_page.logger.info(f"RoomAdd: name inputted: '{room_name}'")
        room_add.click_save_button()
        base_page.logger.info("RoomAdd: save button pressed.")

        # List room
        assert room_list.element_visible(), 'RoomList not open!'
        room_list.find_row(room_name)
        base_page.logger.info(f"RoomList: row found with name: '{room_name}'")
        room_list.click_view_button()
        base_page.logger.info("RoomList: view button pressed.")

        # View room
        room_view = RoomView(driver)
        assert room_view.element_visible(), 'RoomView not open!'
        base_page.logger.info("RoomView: page opened.")
        get_text = room_view.check_room_name()
        assert get_text == room_name, f"{get_text} != {room_name}"
        base_page.logger.info(f"RoomView: name success checked '{room_name}'")
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
        base_page.logger.info("Successful access to the system.")

        # Robot List
        robot_list = RobotList(driver)
        assert robot_list.element_visible(), 'RobotList not open!'
        base_page.logger.info("RobotList: page opened.")
        robot_list.click_add_button()
        base_page.logger.info("RobotList: add button pressed.")

        # Add robot
        robot_add = RobotAdd(driver)
        assert robot_add.element_visible(), 'RobotAdd not open!'
        base_page.logger.info("RobotAdd: page opened.")
        robot_add.input_name(robot_name)
        base_page.logger.info(f"RobotAdd: name inputted: '{robot_name}'")
        robot_add.input_roles(role_name)
        base_page.logger.info(f"RobotAdd: role inputted: '{role_name}'")
        robot_add.input_rooms(room_name)
        base_page.logger.info(f"RobotAdd: room inputted: '{room_name}'")
        robot_add.click_save_button()
        base_page.logger.info("RobotAdd: save button pressed.")

        # List robot
        assert robot_list.element_visible(), 'RobotList not open!'
        robot_list.find_row(robot_name)
        base_page.logger.info(f"RobotList: row found with name: '{robot_name}'")
        robot_list.click_view_button()
        base_page.logger.info("RobotList: view button pressed.")

        # Check robot
        robot_view = RobotView(driver)
        assert robot_view.element_visible(), 'RobotView not open!'
        base_page.logger.info("RobotView: page opened.")
        get_text = robot_view.check_robot_name()
        assert get_text == robot_name, f"{get_text} != {robot_name}"
        base_page.logger.info(f"RobotView: name success checked '{robot_name}'")
        robot_view.click_close_button()
        base_page.logger.info(f"Robot(✅): '{robot_name}' successfully added to filial '{filial_name}'!")

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("test_robot_add_error")
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
        base_page.logger.info("Successful access to the system.")

        # Natural Person List
        natural_person_list = NaturalPersonList(driver)
        assert natural_person_list.element_visible(), 'NaturalPersonList not open!'
        base_page.logger.info("NaturalPersonList: page opened.")
        natural_person_list.click_add_button()
        base_page.logger.info("NaturalPersonList: add button pressed.")

        # Natural Person Add
        natural_person_add = NaturalPersonAdd(driver)
        assert natural_person_add.element_visible(), 'NaturalPersonAdd not open!'
        base_page.logger.info("NaturalPersonAdd: page opened.")
        natural_person_add.input_name(natural_person_name)
        base_page.logger.info(f"NaturalPersonAdd: name inputted: '{natural_person_name}'")
        natural_person_add.click_save_button()
        base_page.logger.info("NaturalPersonAdd: save button pressed.")

        # Natural Person List
        assert natural_person_list.element_visible(), 'NaturalPersonList not open!'
        natural_person_list.find_row(natural_person_name)
        base_page.logger.info(f"NaturalPersonList: row found with name: '{natural_person_name}'")
        natural_person_list.click_view_button()
        base_page.logger.info("NaturalPersonList: view button pressed.")

        # Natural Person View
        natural_person_view = NaturalPersonView(driver)
        assert natural_person_view.element_visible(), 'NaturalPersonView not open!'
        base_page.logger.info("NaturalPersonView: page opened.")
        text = natural_person_view.check_text()
        assert natural_person_name == text, f"Error: {natural_person_name} != {text}"
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
        base_page.logger.info("Successful access to the system.")

        # User List:
        user_list = UserList(driver)
        # assert user_list.element_visible(), 'UserList not open!'
        # base_page.logger.info("UserList: page opened.")
        # user_list.click_add_button()
        # base_page.logger.info("UserList: add button pressed.")
        #
        # # User Add
        # user_add = UserAdd(driver)
        # assert user_add.element_visible(), 'UserAdd not open!'
        # base_page.logger.info("UserAdd: page opened.")
        # user_add.input_person_name(natural_person_name)
        # base_page.logger.info(f"UserAdd: natural person name inputted: '{natural_person_name}'")
        # user_add.input_password(password_user)
        # base_page.logger.info("UserAdd: password inputted.")
        # user_add.click_mouse_down_button()
        # user_add.input_login(login_user)
        # base_page.logger.info(f"UserAdd: login inputted: '{login_user}'")
        # user_add.input_robot(robot_name)
        # base_page.logger.info(f"UserAdd: robot name inputted: '{robot_name}'")
        # user_add.click_save_button()
        # base_page.logger.info("UserAdd: save button pressed.")

        # User List
        assert user_list.element_visible(), 'UserList not open!'
        user_list.find_natural_person_row(natural_person_name)
        base_page.logger.info(f"UserList: row found with name: '{natural_person_name}'")
        user_list.click_view_button()
        base_page.logger.info("UserList: view button pressed.")

        # User View
        user_view = UserView(driver)
        assert user_view.element_visible(), 'UserView not open!'
        base_page.logger.info("UserView: page opened.")
        text = user_view.check_natural_person_text()
        assert natural_person_name == text, f'Error: {natural_person_name} != {text}'
        base_page.logger.info(f"UserView: name success checked '{natural_person_name}'")

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
        base_page.logger.info("Successful access to the system.")

        # Role List
        role_list = RoleList(driver)
        assert role_list.element_visible(), 'RoleList not open!'
        base_page.logger.info("RoleList: page opened.")
        role_list.click_row_button(role_name)
        base_page.logger.info(f"RoleList: role row selected with name: '{role_name}'")
        role_list.click_edit_button()
        base_page.logger.info("RoleList: edit button pressed.")

        # Role Edit
        role_edit = RoleEdit(driver)
        assert role_edit.element_visible(), 'RoleEdit not open!'
        base_page.logger.info("RoleEdit: page opened.")
        if not role_edit.check_checkbox():
            role_edit.click_checkboxes()
            base_page.logger.info("RoleEdit: all checkboxes selected.")
        role_edit.click_save_button()
        base_page.logger.info("RoleEdit: save button pressed.")

        # Role List
        assert role_list.element_visible(), 'RoleList not open!'
        role_list.click_row_button(role_name)
        base_page.logger.info(f"RoleList: role row re-selected with name: '{role_name}'")
        role_list.click_view_button()
        base_page.logger.info("RoleList: view button pressed.")

        # Role View
        role_view = RoleView(driver)
        assert role_view.element_visible(), 'RoleView not open!'
        base_page.logger.info("RoleView: page opened.")
        text = role_view.check_text()
        assert role_name == text, f"{role_name} != {text}"
        base_page.logger.info(f"RoleView: name success checked '{role_name}'")

        # Access all
        role_view.click_navbar_button()
        role_view.click_detached_button()
        role_view.click_checkbox_form()
        role_view.click_access_all_button()
        base_page.logger.info("RoleView: 'Access all' permissions granted.")
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

    base_page.logger.info(f"Test data: password_user='******'")

    try:
        # Login
        login_user(driver, filial_name=False, url=False)
        base_page.logger.info("Successful access to the system.")

        # Change Password
        change_password = ChangePassword(driver)
        assert change_password.element_visible(), 'ChangePassword not open!'
        base_page.logger.info("ChangePassword: page opened.")
        change_password.input_current_password(password_user)
        base_page.logger.info("ChangePassword: current password inputted.")
        change_password.input_new_password(password_user)
        base_page.logger.info("ChangePassword: new password inputted.")
        change_password.input_rewritten_password(password_user)
        base_page.logger.info("ChangePassword: rewritten password inputted.")
        change_password.click_save_button()
        base_page.logger.info("ChangePassword: save button pressed.")
        time.sleep(2)
        base_page.logger.info(f"Password(✅): successfully changed!")

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("test_user_change_password_error")
        raise


def test_price_type_add(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_price_type_add")

    # Test data
    data = test_data()["data"]
    price_type_name = data["price_type_name"]
    room_name = data["room_name"]

    base_page.logger.info(f"Test data: price_type_name='{price_type_name}', room_name='{room_name}'")

    try:
        # Login
        login_user(driver, url='anor/mkr/price_type_list')
        base_page.logger.info("Successful access to the system.")

        # Price Type List
        price_type_list = PriceTypeList(driver)
        assert price_type_list.element_visible(), 'PriceTypeList not open!'
        base_page.logger.info("PriceTypeList: page opened.")
        price_type_list.click_add_button()
        base_page.logger.info("PriceTypeList: add button pressed.")

        # Price Type Add
        price_type_add = PriceTypeAdd(driver)
        assert price_type_add.element_visible(), 'PriceTypeAdd not open!'
        base_page.logger.info("PriceTypeAdd: page opened.")
        price_type_add.input_name(price_type_name)
        base_page.logger.info(f"PriceTypeAdd: name inputted: '{price_type_name}'")
        price_type_add.input_rooms(room_name)
        base_page.logger.info(f"PriceTypeAdd: room inputted: '{room_name}'")
        price_type_add.click_save_button()
        base_page.logger.info("PriceTypeAdd: save button pressed.")

        # Price Type List
        assert price_type_list.element_visible(), 'PriceTypeList not open!'
        price_type_list.find_row(price_type_name)
        base_page.logger.info(f"PriceTypeList: row found with name: '{price_type_name}'")
        price_type_list.click_view_button()
        base_page.logger.info("PriceTypeList: view button pressed.")

        # Price Type View
        price_type_view = PriceTypeIdView(driver)
        assert price_type_view.element_visible(), 'PriceTypeIdView not open!'
        base_page.logger.info("PriceTypeIdView: page opened.")
        text = price_type_view.get_elements()
        assert price_type_name == text, f'"{price_type_name}" != "{text}"!'
        base_page.logger.info(f"PriceTypeIdView: name successfully verified '{price_type_name}'")
        price_type_view.click_close_button()
        base_page.logger.info(f"PriceType(✅): '{price_type_name}' successfully added!")

    except Exception as e:
        base_page.logger.error(f"Error message(❌): {e}")
        base_page.take_screenshot("test_price_type_add_error")
        raise


def test_payment_type_add(driver):
    # Log
    base_page = BasePage(driver)
    base_page.logger.info("Test run(▶️): test_payment_type_add")

    try:
        # Login
        login_user(driver, url='anor/mkr/payment_type_list')
        base_page.logger.info("Successful access to the system.")

        # Payment Type List
        payment_type_list = PaymentTypeList(driver)
        assert payment_type_list.element_visible(), 'PaymentTypeList not open!'
        base_page.logger.info("PaymentTypeList: page opened.")
        payment_type_list.click_attach_button()
        base_page.logger.info("PaymentTypeList: attach button pressed.")

        # Payment Type List Attach
        payment_type_list_attach = PaymentTypeListAttach(driver)
        assert payment_type_list_attach.element_visible(), 'PaymentTypeListAttach not open!'
        base_page.logger.info("PaymentTypeListAttach: page opened.")
        payment_type_list_attach.click_checkbox_all()
        base_page.logger.info("PaymentTypeListAttach: all checkboxes selected.")
        payment_type_list_attach.click_close_button()
        base_page.logger.info("PaymentTypeListAttach: close button pressed.")
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

    base_page.logger.info(f"Test data: product_name='{product_name}', "
                          f"measurement_name='{measurement_name}', "
                          f"sector_name='{sector_name}', product_price='{product_price}'")

    try:
        # Login
        login_user(driver, url='anor/mr/product/inventory_list')
        base_page.logger.info("Successful access to the system.")

        # Inventory List
        inventory_list = InventoryList(driver)
        assert inventory_list.element_visible(), 'InventoryList not open!'
        base_page.logger.info("InventoryList: page opened.")
        inventory_list.click_add_button()
        base_page.logger.info("InventoryList: add button pressed.")

        # Add Inventory
        inventory_add = InventoryNew(driver)
        assert inventory_add.element_visible(), 'InventoryNew not open!'
        base_page.logger.info("InventoryNew: page opened.")
        inventory_add.input_name(product_name)
        base_page.logger.info(f"InventoryNew: product name inputted: '{product_name}'")
        inventory_add.input_measurement(measurement_name)
        base_page.logger.info(f"InventoryNew: measurement name inputted: '{measurement_name}'")
        inventory_add.input_sectors(sector_name)
        base_page.logger.info(f"InventoryNew: sector name inputted: '{sector_name}'")
        inventory_add.click_goods_checkbox()
        base_page.logger.info("InventoryNew: goods checkbox selected.")
        inventory_add.click_save_button()
        base_page.logger.info("InventoryNew: save button pressed.")

        # Inventory List
        assert inventory_list.element_visible(), 'InventoryList not open!'
        inventory_list.find_and_click_checkbox(product_name)
        base_page.logger.info(f"InventoryList: checkbox selected for product '{product_name}'.")
        inventory_list.click_view_button()
        base_page.logger.info("InventoryList: view button pressed.")

        # Product View
        product_id = ProductView(driver)
        assert product_id.element_visible(), 'ProductView not open!'
        base_page.logger.info("ProductView: page opened.")
        get_name = product_id.get_elements()
        assert product_name == get_name, f"Error: {product_name} != {get_name}"
        base_page.logger.info(f"ProductView: name successfully verified '{product_name}'.")
        product_id.click_close_button()
        base_page.logger.info("ProductView: close button pressed.")

        # Inventory List - Set Price
        assert inventory_list.element_visible(), 'InventoryList not open!'
        inventory_list.find_and_click_checkbox(product_name)
        base_page.logger.info(f"InventoryList: checkbox re-selected for product '{product_name}'.")
        inventory_list.click_set_price_button()
        base_page.logger.info("InventoryList: set price button pressed.")

        # Product Set Price
        product_set_price = ProductSetPrice(driver)
        assert product_set_price.element_visible(), 'ProductSetPrice not open!'
        base_page.logger.info("ProductSetPrice: page opened.")
        text = product_set_price.check_product()
        assert product_name == text, f'"{product_name}" != "{text}"'
        base_page.logger.info(f"ProductSetPrice: product name verified '{product_name}'.")
        product_set_price.input_prices(product_price)
        base_page.logger.info(f"ProductSetPrice: price inputted: '{product_price}'.")
        product_set_price.click_save_button()
        base_page.logger.info("ProductSetPrice: save button pressed.")
        base_page.logger.info(f"Product(✅): '{product_name}' with price '{product_price}' successfully added!")

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
        base_page.logger.info("Successful access to the system.")

        # Room List
        room_list = RoomList(driver)
        assert room_list.element_visible(), 'RoomList not open!'
        base_page.logger.info("RoomList: page opened.")
        room_list.find_row(room_name)
        base_page.logger.info(f"RoomList: row found for room '{room_name}'.")
        room_list.click_attachment_button()
        base_page.logger.info("RoomList: attachment button pressed.")

        # Room Attachment
        room_attachment = RoomAttachment(driver)
        assert room_attachment.element_visible(), 'RoomAttachment not open!'
        base_page.logger.info("RoomAttachment: page opened.")

        # Attach payment types
        room_attachment.click_navbar_button(navbar_button=3)
        room_attachment.click_detach_button(detach_button=3)
        base_page.logger.info("RoomAttachment: payment types detached.")
        room_attachment.click_checkbox_all(attach_button=3)
        base_page.logger.info("RoomAttachment: payment types attached.")

        # Attach warehouse
        room_attachment.click_navbar_button(navbar_button=6)
        room_attachment.click_detach_button(detach_button=6)
        room_attachment.find_row(warehouse_name)
        base_page.logger.info(f"RoomAttachment: warehouse '{warehouse_name}' found.")
        room_attachment.click_attach_button(attach_button=6)
        base_page.logger.info(f"RoomAttachment: warehouse '{warehouse_name}' attached.")

        # Attach cash register
        room_attachment.click_navbar_button(navbar_button=7)
        room_attachment.click_detach_button(detach_button=7)
        room_attachment.find_row(cash_register_name)
        base_page.logger.info(f"RoomAttachment: cash register '{cash_register_name}' found.")
        room_attachment.click_attach_button(attach_button=7)
        base_page.logger.info(f"RoomAttachment: cash register '{cash_register_name}' attached.")

        # Attach clients
        room_attachment.click_navbar_button(navbar_button=11)
        room_attachment.click_detach_button(detach_button=11)
        base_page.logger.info("RoomAttachment: clients detached.")
        room_attachment.find_row(f'{client_name}-A')
        room_attachment.click_attach_button(attach_button=11)
        base_page.logger.info(f"RoomAttachment: client '{client_name}-A' attached.")
        room_attachment.find_row(f'{client_name}-B')
        room_attachment.click_attach_button(attach_button=11)
        base_page.logger.info(f"RoomAttachment: client '{client_name}-B' attached.")
        room_attachment.find_row(f'{client_name}-C')
        room_attachment.click_attach_button(attach_button=11)
        base_page.logger.info(f"RoomAttachment: client '{client_name}-C' attached.")

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
        base_page.logger.info(f"Balance(✅): {balance} pieces of '{product_name}' successfully added to '{warehouse_name}'!")

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

def contract_add(driver, client_name=None, contract_name=None, initial_amount=None):
    # Test data
    data = test_data()["data"]
    client_name = client_name if client_name is not None else data["client_name"]
    contract_name = contract_name if contract_name is not None else data["contract_name"]
    initial_amount = initial_amount if initial_amount is not None else data["product_quantity"] * data["product_price"]
    base_currency_cod = data["base_currency_cod"]

    login_user(driver, url='anor/mkf/contract_list')

    # Client List
    contract_list = ContractList(driver)
    assert contract_list.element_visible(), 'ContractList not open!'
    contract_list.click_add_button()

    # Client Add
    contract_add = ContractAdd(driver)
    assert contract_add.element_visible(), 'ContractAdd not open!'
    contract_number = random.randint(1, 999999)
    contract_add.input_contract_number(contract_number)
    contract_add.input_contract_name(contract_name)
    contract_add.click_radio_button()
    contract_add.input_person_name(client_name)
    contract_add.input_currency_name(base_currency_cod)
    contract_add.input_initial_amount(initial_amount)
    contract_add.click_checkbox_button()
    contract_add.click_save_button()

    # Client List
    assert contract_list.element_visible(), 'ContractList not open!'
    contract_list.find_row(contract_name)
    contract_list.click_view_button()

    # Contract View
    contract_view = ContractView(driver)
    contract_view.element_visible()
    contract_view.click_close_button()
    print(f'Contract: {contract_name} successfully joined!')


def test_contract_add_A(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-A"
    contract_name = f"{data['contract_name']}-A"
    contract_add(driver, client_name=client_name, contract_name=contract_name)


def test_contract_add_B(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-B"
    contract_name = f"{data['contract_name']}-B"
    initial_amount = 100 * data["product_price"]
    contract_add(driver,
                 client_name=client_name,
                 contract_name=contract_name,
                 initial_amount=initial_amount)


def test_contract_add_C(driver):
    data = test_data()["data"]
    client_name = f"{data['client_name']}-C"
    contract_name = f"{data['contract_name']}-C"
    contract_add(driver, client_name=client_name, contract_name=contract_name)
