import random
import time

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
from tests.test_base.test_base import test_data, login, dashboard, open_new_window
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
    # Test data
    data = test_data()["data"]

    legal_person_name = legal_person_name if legal_person_name is not None else data["legal_person_name"]

    # Login
    login(driver, data["email"], data["password"])

    # Dashboard
    dashboard(driver)
    dashboard_page = DashboardPage(driver)
    dashboard_page.find_filial(data["Administration_name"])

    # Open natural_person_list
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'anor/mr/person/legal_person_list')

    # Legal Person List
    legal_person_list = LegalPersonList(driver)
    assert legal_person_list.element_visible(), 'LegalPersonList not open!'
    legal_person_list.click_add_button()

    # Legal Person Add
    legal_person_add = LegalPersonAdd(driver)
    assert legal_person_add.element_visible(), 'LegalPersonAdd not open!'
    legal_person_add.input_name(legal_person_name)
    legal_person_add.click_save_button()

    # Legal Person List
    assert legal_person_list.element_visible(), 'LegalPersonList not open!'
    legal_person_list.find_row(legal_person_name)
    legal_person_list.click_view_button()

    # Legal Person View
    time.sleep(2)
    legal_person_view = LegalPersonView(driver)
    assert legal_person_view.element_visible(), 'LegalPersonView not open!'
    text = legal_person_view.check_text()
    assert legal_person_name == text, f'Error: {legal_person_name} != {text}'
    print(f"Legal Person: '{legal_person_name}' successfully added!")


def test_filial_creat(driver):
    # Test data
    data = test_data()["data"]

    filial_name = data["filial_name"]

    # Login
    login(driver, data["email"], data["password"])

    # Dashboard
    dashboard(driver)
    dashboard_page = DashboardPage(driver)
    dashboard_page.find_filial(data["Administration_name"])

    # Open filial_list
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'anor/mr/filial_list')

    filial_list = FilialList(driver)
    assert filial_list.element_visible(), 'FilialList not open!'
    filial_list.click_add_button()

    # FilialAdd
    time.sleep(2)
    filial_add = FilialAdd(driver)
    assert filial_add.element_visible(), 'FilialAdd not open!'
    filial_add.input_name(filial_name)
    filial_add.input_base_currency_name(data["base_currency_cod"])
    filial_add.input_person_name(data['legal_person_name'])
    filial_add.click_save_button()

    # FilialList
    time.sleep(2)
    assert filial_list.element_visible(), 'FilialList not open!'
    filial_list.find_filial_row(data["filial_name"])
    filial_list.click_view_button()

    # FilialView
    time.sleep(2)
    filial_view = FilialView(driver)
    assert filial_view.element_visible(), 'FilialView not open!'
    text = filial_view.check_filial_text()
    assert data["filial_name"] == text, f'Error: {data["filial_name"]} != {text}'
    filial_view.click_close_button()
    print(f"Filial: '{data['filial_name']}' successfully added!")


def test_room_add(driver):
    # Test data
    data = test_data()["data"]

    # Login
    login(driver, data["email"], data["password"])

    # Dashboard
    dashboard(driver)
    dashboard_page = DashboardPage(driver)
    dashboard_page.find_filial(data["filial_name"])

    # Open room list
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'trade/trf/room_list')
    room_list = RoomList(driver)
    assert room_list.element_visible(), 'RoomList not open!'
    room_list.click_add_button()

    # Add room
    room_add = RoomAdd(driver)
    assert room_add.element_visible(), 'RoomAdd not open!'
    room_add.input_name(data["room_name"])
    room_add.click_save_button()
    time.sleep(2)

    # List room
    assert room_list.element_visible(), 'RoomList not open!'
    room_list.find_row(data["room_name"])
    room_list.click_view_button()

    # View room
    room_view = RoomView(driver)
    assert room_view.element_visible(), 'RoomView not open!'
    get_text = room_view.check_room_name()
    assert get_text == data["room_name"], f"{get_text} != {data['room_name']}"
    room_view.click_close_button()
    print(f'Room: "{data["room_name"]}" successfully added to filial "{data["filial_name"]}"!')


def test_robot_add(driver):
    # Test data
    data = test_data()["data"]

    # Login
    login(driver, data["email"], data["password"])

    # Dashboard
    dashboard(driver)
    dashboard_page = DashboardPage(driver)
    dashboard_page.find_filial(data["filial_name"])

    # Open robot list
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'anor/mrf/robot_list')
    robot_list = RobotList(driver)
    assert robot_list.element_visible(), 'RobotList not open!'
    robot_list.click_add_button()

    # Add robot
    robot_add = RobotAdd(driver)
    assert robot_add.element_visible(), 'RobotAdd not open!'
    robot_add.input_name(data["robot_name"])
    robot_add.input_roles(data["role_name"])
    robot_add.input_rooms(data["room_name"])
    robot_add.click_save_button()
    time.sleep(2)

    # List robot
    assert robot_list.element_visible(), 'RobotList not open!'
    robot_list.find_row(data["robot_name"])
    robot_list.click_view_button()

    # Check robot
    robot_view = RobotView(driver)
    assert robot_view.element_visible(), 'RobotView not open!'
    get_text = robot_view.check_robot_name()
    assert get_text == data["robot_name"], f"{get_text} != {data['robot_name']}"
    robot_view.click_close_button()
    print(f'Robot: "{data["robot_name"]}" successfully added to filial "{data["filial_name"]}"!')


def test_natural_person_add(driver, person_name=None):
    # Test data
    data = test_data()["data"]
    natural_person_name = person_name if person_name is not None else data["natural_person_name"]

    # Login
    login(driver, data["email"], data["password"])

    # Dashboard
    dashboard(driver)
    dashboard_page = DashboardPage(driver)
    dashboard_page.find_filial(data["filial_name"])

    # Open natural_person_list
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'anor/mr/person/natural_person_list')

    # Natural Person List
    natural_person_list = NaturalPersonList(driver)
    assert natural_person_list.element_visible(), 'NaturalPersonList not open!'
    natural_person_list.click_add_button()

    # Natural Person Add
    natural_person_add = NaturalPersonAdd(driver)
    assert natural_person_add.element_visible(), 'NaturalPersonAdd not open!'
    natural_person_add.input_name(natural_person_name)
    natural_person_add.click_save_button()

    # Natural Person List
    assert natural_person_list.element_visible(), 'NaturalPersonList not open!'
    natural_person_list.find_row(natural_person_name)
    natural_person_list.click_view_button()

    # Natural Person View
    time.sleep(2)
    natural_person_view = NaturalPersonView(driver)
    assert natural_person_view.element_visible(), 'NaturalPersonView not open!'
    text = natural_person_view.check_text()
    assert natural_person_name == text, f'Error: {natural_person_name} != {text}'
    print(f"Natural Person: '{natural_person_name}' successfully added!")


def test_user_creat(driver):
    # Test data
    data = test_data()["data"]

    email = data["email"]
    password = data["password"]
    filial_name = data["filial_name"]

    # Login
    login(driver, email, password)

    # Dashboard
    dashboard(driver)
    dashboard_page = DashboardPage(driver)
    dashboard_page.find_filial(filial_name)

    # Open user list
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'anor/mr/user_list')

    # User create:
    user_list = UserList(driver)
    assert user_list.element_visible(), 'UserList not open!'
    user_list.click_add_button()

    # UserAdd
    time.sleep(2)
    user_add = UserAdd(driver)
    assert user_add.element_visible(), 'UserAdd not open!'
    user_add.input_person_name(data["natural_person_name"])
    user_add.input_password(data["password_user"])
    user_add.click_mouse_down_button()
    user_add.input_login(data["login_user"])
    user_add.input_robot(data["robot_name"])
    user_add.click_save_button()

    # UserList
    time.sleep(2)
    assert user_list.element_visible(), 'UserList not open!'
    user_list.find_natural_person_row(data["natural_person_name"])
    user_list.click_view_button()

    # UserView
    time.sleep(2)
    user_view = UserView(driver)
    assert user_view.element_visible(), 'UserView not open!'
    text = user_view.check_natural_person_text()
    assert data["natural_person_name"] == text, f'Error: {data["natural_person_name"]} != {text}'
    print('User: successfully added!')

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

    # user_view.click_tablist_button(tablist_button=4)
    # user_view.click_detached_button(detached_button=1)
    # if not user_view.text_check():
    #     user_view.attach_forms()
    #     user_view.text_check()

    user_view.click_tablist_button(tablist_button=5)
    user_view.click_detached_button(detached_button=1)
    user_view.attach_forms()

    user_view.click_close_button()
    print('Forms: Permissions added to user forms!')


def test_adding_permissions_to_user(driver):
    # Test data
    data = test_data()["data"]

    # Login
    login(driver, data["email"], data["password"])

    # Dashboard
    dashboard(driver)
    dashboard_page = DashboardPage(driver)
    dashboard_page.find_filial(data["filial_name"])

    # Open role list
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'trade/tr/role_list')

    # Role List
    role_list = RoleList(driver)
    assert role_list.element_visible(), 'RoleList not open!'
    role_list.click_row_button(data['role_name'])
    role_list.click_edit_button()

    # Role Edit
    time.sleep(2)
    role_edit = RoleEdit(driver)
    assert role_edit.element_visible(), 'RoleEdit not open!'
    role_edit.click_checkboxes()
    role_edit.click_save_button()

    # Role List
    time.sleep(2)
    assert role_list.element_visible(), 'RoleList not open!'
    role_list.element_visible()
    role_list.click_row_button(data['role_name'])
    role_list.click_view_button()

    # Role View
    role_view = RoleView(driver)
    assert role_view.element_visible(), 'RoleView not open!'
    text = role_view.check_text()
    assert data['role_name'] == text, f"{data['role_name']} != {text}"

    # Access all
    role_view.click_navbar_button()
    role_view.click_detached_button()
    role_view.click_checkbox_form()
    role_view.click_access_all_button()
    time.sleep(2)
    role_view.click_close_button()
    print('Roles: Permissions added to user role!')


def test_user_change_password(driver):
    # Test data
    data = test_data()["data"]

    # Login
    login(driver, data["email_user"], data["password_user"])

    # Change Password
    change_password = ChangePassword(driver)
    assert change_password.element_visible(), 'ChangePassword not open!'
    change_password.input_current_password(data["password_user"])
    change_password.input_new_password(data["password_user"])
    change_password.input_rewritten_password(data["password_user"])
    change_password.click_save_button()
    time.sleep(2)


def test_price_type_add(driver):
    # Test data
    data = test_data()["data"]

    # Login
    login(driver, data["email_user"], data["password_user"])

    # Dashboard
    dashboard(driver)

    # Open price_type list
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'anor/mkr/price_type_list')
    price_type_list = PriceTypeList(driver)
    assert price_type_list.element_visible(), 'PriceTypeList not open!'
    price_type_list.click_add_button()

    # Price Type Add
    price_type_add = PriceTypeAdd(driver)
    assert price_type_add.element_visible(), 'PriceTypeAdd not open!'
    price_type_add.input_name(data["price_type_name"])
    price_type_add.input_rooms(data["room_name"])
    price_type_add.click_save_button()

    # Price Type List
    assert price_type_list.element_visible(), 'PriceTypeList not open!'
    price_type_list.find_row(data["price_type_name"])
    price_type_list.click_view_button()

    # Price Type View
    price_type_view = PriceTypeIdView(driver)
    assert price_type_view.element_visible(), 'PriceTypeIdView not open!'
    text = price_type_view.get_elements()
    assert data["price_type_name"] == text, f'"{data["price_type_name"]}" != "{text}"!'
    price_type_view.click_close_button()
    print(f'Price type: "{data["price_type_name"]}" successfully joined!')


def test_payment_type_add(driver):
    # Test data
    data = test_data()["data"]

    # Login
    login(driver, data["email_user"], data["password_user"])

    # Dashboard
    dashboard(driver)

    # Open Payment Type List
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'anor/mkr/payment_type_list')
    payment_type_list = PaymentTypeList(driver)
    assert payment_type_list.element_visible(), 'PaymentTypeList not open!'
    payment_type_list.click_attach_button()

    # Payment Type List Attach
    payment_type_list_attach = PaymentTypeListAttach(driver)
    assert payment_type_list_attach.element_visible(), 'PaymentTypeListAttach not open!'
    payment_type_list_attach.click_checkbox_all()
    payment_type_list_attach.click_close_button()
    print(f'Payment type: successfully joined!')


def test_sector_add(driver):
    # Test data
    data = test_data()["data"]

    # Login
    login(driver, data["email_user"], data["password_user"])

    # Dashboard
    dashboard(driver)

    # Open sector list
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'anor/mr/sector_list')
    sector_list = SectorList(driver)
    assert sector_list.element_visible(), 'SectorList not open!'
    sector_list.click_add_button()

    # Add sectors
    sector_add = SectorAdd(driver)
    assert sector_add.element_visible(), 'SectorAdd not open!'
    sector_add.input_name(data["sector_name"])
    sector_add.input_rooms(data["room_name"])
    sector_add.click_save_button()

    # SectorList
    assert sector_list.element_visible(), 'SectorList not open!'
    sector_list.find_row(data["sector_name"])
    sector_list.click_view_button()

    # SectorView
    sector_view = SectorView(driver)
    assert sector_view.element_visible(), 'SectorView not open!'
    get_name = sector_view.check_sector_name()
    assert data["sector_name"] == get_name, f"Error: {data['sector_name']} != {get_name}"
    sector_view.click_close_button()
    print(f"Sector: {data['sector_name']} successfully joined!")


def test_product_add(driver):
    # Test data
    data = test_data()["data"]

    # Login
    login(driver, data["email_user"], data["password_user"])

    # Dashboard
    dashboard(driver)

    # Open inventory list
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'anor/mr/product/inventory_list')
    inventory_list = InventoryList(driver)
    assert inventory_list.element_visible(), 'InventoryList not open!'
    inventory_list.click_add_button()

    # Add Inventory
    inventory_add = InventoryNew(driver)
    assert inventory_add.element_visible(), 'InventoryNew not open!'
    inventory_add.input_name(data["product_name"])
    inventory_add.input_measurement(data['measurement_name'])
    inventory_add.input_sectors(data['sector_name'])
    inventory_add.click_goods_checkbox()
    inventory_add.click_save_button()

    # Inventory_list
    assert inventory_list.element_visible(), 'InventoryList not open!'
    inventory_list.find_and_click_checkbox(data["product_name"])
    inventory_list.click_view_button()

    # ProductView
    product_id = ProductView(driver)
    assert product_id.element_visible(), 'ProductView not open!'
    get_name = product_id.get_elements()
    assert data["product_name"] == get_name, f"Error: {data['product_name']} != {get_name}"
    product_id.click_close_button()

    # Inventory_list
    assert inventory_list.element_visible(), 'InventoryList not open!'
    inventory_list.find_and_click_checkbox(data["product_name"])
    inventory_list.click_set_price_button()

    # Product Set Price
    product_set_price = ProductSetPrice(driver)
    assert product_set_price.element_visible(), 'ProductSetPrice not open!'
    text = product_set_price.check_product()
    assert data["product_name"] == text, f'"{data["product_name"]}" != "{text}"'
    product_set_price.input_prices(data["product_price"])
    product_set_price.click_save_button()
    print(f'Product: {data["product_name"]} with {data["product_price"]} price successfully joined!')


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
    # Test data
    data = test_data()["data"]

    client_name = client_name if client_name is not None else data["client_name"]

    # Login
    login(driver, data["email_user"], data["password_user"])

    # Dashboard
    dashboard(driver)

    # Open init balance
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'anor/mrf/client_list')

    # Client List
    client_list = ClientList(driver)
    assert client_list.element_visible(), 'ClientList not open!'
    client_list.click_add_button()

    # Client Add
    client_add = ClientAdd(driver)
    assert client_add.element_visible(), 'ClientAdd not open!'
    client_add.click_radio_button()
    client_add.input_name(client_name)
    client_add.click_save_button()

    # Client List
    assert client_list.element_visible(), 'ClientList not open!'
    client_list.find_row(client_name)
    client_list.click_view_button()

    # Client View
    client_view = ClientView(driver)
    assert client_view.element_visible(), 'ClientView not open!'
    client_view.check_client_name()
    client_view.click_close_button()
    print(f"Client: '{client_name}' successfully added!")
    time.sleep(2)


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
    # Test data
    data = test_data()["data"]

    # Login
    login(driver, data["email"], data["password"])

    # Dashboard
    dashboard(driver)
    dashboard_page = DashboardPage(driver)
    dashboard_page.find_filial(data["filial_name"])

    # Open room list
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'trade/trf/room_list')
    room_list = RoomList(driver)
    assert room_list.element_visible(), 'RoomList not open!'
    room_list.find_row(data["room_name"])
    room_list.click_attachment_button()

    # Room Attachment
    room_attachment = RoomAttachment(driver)
    assert room_attachment.element_visible(), 'RoomAttachment not open!'

    # Attachment: payment_type
    room_attachment.click_navbar_button(navbar_button=3)
    room_attachment.click_detach_button(detach_button=3)
    room_attachment.click_checkbox_all(attach_button=3)

    # Attachment: warehouse_name
    room_attachment.click_navbar_button(navbar_button=6)
    room_attachment.click_detach_button(detach_button=6)
    room_attachment.find_row(data["warehouse_name"])
    room_attachment.click_attach_button(attach_button=6)

    # Attachment: cash_register_name
    room_attachment.click_navbar_button(navbar_button=7)
    room_attachment.click_detach_button(detach_button=7)
    room_attachment.find_row(data["cash_register_name"])
    room_attachment.click_attach_button(attach_button=7)

    # Attachment: client_name
    room_attachment.click_navbar_button(navbar_button=11)
    room_attachment.click_detach_button(detach_button=11)
    room_attachment.find_row(f'{data["client_name"]}-A')
    room_attachment.click_attach_button(attach_button=11)
    room_attachment.find_row(f'{data["client_name"]}-B')
    room_attachment.click_attach_button(attach_button=11)
    room_attachment.find_row(f'{data["client_name"]}-C')
    room_attachment.click_attach_button(attach_button=11)

    room_attachment.click_close_button()
    time.sleep(2)
    print(f'Room: "{data["room_name"]}" successfully added to: \n"payment_type", \n"{data["warehouse_name"]}", '
          f'\n"{data["cash_register_name"]}", \n"{data["client_name"]}-A,B,C"')


def test_init_balance(driver):
    # Test data
    data = test_data()["data"]

    # Login
    login(driver, data["email_user"], data["password_user"])

    # Dashboard
    dashboard(driver)

    # Open init balance
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'anor/mkw/init_balance/init_inventory_balance_list')
    init_balance = InitInventoryBalanceList(driver)
    assert init_balance.element_visible(), 'InitInventoryBalanceList not open!'
    init_balance.click_add_button()

    # Add init balance
    init_balance_add = InitInventoryBalanceAdd(driver)
    balance_number = random.randint(1, 99999)
    init_balance_add.input_balance_number(balance_number)
    init_balance_add.input_product_name(data['product_name'])
    product_card_code = random.randint(1, 99999)
    init_balance_add.input_card_code(product_card_code)
    init_balance_add.input_quantity(data['product_quantity'])
    init_balance_add.input_price(data['product_price'])
    init_balance_add.click_save_button()
    assert init_balance_add.find_row(balance_number), f"{balance_number} balance number not found!"
    init_balance_add.click_post_one_button()
    time.sleep(1)

    # balance_list
    open_new_window(driver, cut_url + 'anor/mkw/balance/balance_list')
    balance_list = BalanceList(driver)
    assert balance_list.element_visible(), 'BalanceList not open!'

    try:
        balance_list.find_row(data['product_name'])
    except:
        balance_list.click_reload_button()
        balance_list.find_row(data['product_name'])

    balance_list.click_detail_button()
    time.sleep(2)
    balance = balance_list.check_balance_quantity()
    assert balance == data['product_quantity'], f"balance: {balance} != product_quantity: {data['product_quantity']}"
    print(f"{balance} pieces of '{data['product_name']}' added to the '{data['warehouse_name']}'")
    time.sleep(1)


def test_order_request(driver):
    # Test data
    data = test_data()["data"]

    email_user = data["email_user"]
    password_user = data["password_user"]

    # Login
    login(driver, email_user, password_user)

    # Dashboard
    dashboard(driver)

    # Open Order Request List
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'anor/mdeal/order/order_request_list')
    order_request_list = OrderRequestList(driver)
    assert order_request_list.element_visible()
    order_request_list.click_add_button()

    # Order Request Main
    order_request_add_main = OrderRequestAddMain(driver)
    assert order_request_add_main.element_visible()
    order_request_add_main.click_rooms_input(data["room_name"])
    order_request_add_main.click_robots_input(data["robot_name"])
    order_request_add_main.click_persons_input(data["client_name"])
    order_request_add_main.click_next_step_button()

    # Order Request Product
    order_request_add_product = OrderRequestAddProduct(driver)
    assert order_request_add_product.element_visible()
    order_request_add_product.input_name(data["product_name"])
    order_request_add_product.input_quantity(data["product_quantity"])
    order_request_add_product.click_next_step_button()

    # Order Request Final
    order_request_add_final = OrderRequestAddFinal(driver)
    assert order_request_add_final.element_visible()
    request_number = random.randint(1, 99999)
    order_request_add_final.input_request_number(request_number)
    order_request_add_final.click_save_button()

    # Order Request List
    assert order_request_list.element_visible()
    order_request_list.find_row(data["client_name"])
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

    # Login
    login(driver, data["email_user"], data["password_user"])

    # Dashboard
    dashboard(driver)
    dashboard_page = DashboardPage(driver)
    dashboard_page.find_filial(data["filial_name"])

    # Open contract list
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'anor/mkf/contract_list')

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
    contract_add.input_currency_name(data["base_currency_cod"])
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
