import random
import time

from autotest.anor.mdeal.order.order_add.order_request_add.order_request_add_final import OrderRequestAddFinal
from autotest.anor.mdeal.order.order_add.order_request_add.order_request_add_main import OrderRequestAddMain
from autotest.anor.mdeal.order.order_add.order_request_add.order_request_add_product import OrderRequestAddProduct
from autotest.anor.mdeal.order.order_add.order_request_view.order_request_view import OrderRequestView
from autotest.anor.mdeal.order.order_request_list.order_request_list import OrderRequestList

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
from autotest.anor.mkw.init_balance.init_inventory_balance_list.init_inventory_balance_list import InitInventoryBalanceList
from autotest.anor.mr.filial_add.filial_add import FilialAdd
from autotest.anor.mr.filial_list.filial_list import FilialList
from autotest.anor.mr.filial_view.filial_view import FilialView
from autotest.anor.mr.sector_add.sector_add import SectorAdd
from autotest.anor.mr.sector_list.sector_list import SectorList
from autotest.anor.mr.sector_view.sector_view import SectorView
from autotest.anor.mr.user_add.user_add import UserAdd
from autotest.anor.mr.user_list.user_list import UserList
from autotest.anor.mr.user_view.user_view import UserView
from autotest.anor.mrf.robot_add.robot_add import RobotAdd
from autotest.anor.mrf.robot_list.robot_list import RobotList
from autotest.anor.mrf.robot_view.robot_view import RobotView
from autotest.anor.mrf.room_attachment.room_attachment import RoomAttachment
from autotest.anor.mrf.subfilial_add.subfilial_add import SubFilialAdd
from autotest.anor.mrf.subfilial_list.subfilial_list import SubFilialList
from autotest.anor.mrf.van_add.van_add import VanAdd
from autotest.anor.mrf.van_list.van_list import VanList
from autotest.biruni.kl.license_list.license_list import LicenseList
from autotest.biruni.kl.license_user_list.license_user_list import LicenseUserList
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
from tests.conftest import driver, test_data
from tests.test_base.test_base import dashboard, login_admin, login_user, logout
from tests.test_rep.integration.rep_main_funksiya import generate_and_verify_download
from utils.exception import ElementNotFoundError


def test_company_create(driver, test_data):
    # Test data
    data = test_data["data"]
    email = data['email_company']
    password = data['password_company']
    code_input = data["code_input"]
    name_company = data["name_company"]
    plan_account = data["plan_account"]
    bank_name = data["bank_name"]

    # Login
    login_admin(driver, test_data, email, password,
                dashboard_check=False, change_password_check=False, url=False)

    # Dashboard
    dashboard(driver)
    dashboard_page = DashboardPage(driver)
    dashboard_page.click_main_button()

    # Main Navbar
    main_navbar = MainNavbar(driver)
    main_navbar.element_visible()
    main_navbar.click_company_button()

    # Company List
    company_list = CompanyList(driver)
    company_list.element_visible()
    company_list.click_add_button()

    # Company Add
    company_add = CompanyAdd(driver)
    company_add.element_visible()
    company_add.input_code(code_input)
    company_add.input_name(name_company)
    company_add.input_plan_accounts(plan_account)
    company_add.input_bank(bank_name)
    company_add.input_checkbox()
    company_add.click_save_button()

    # Verify Company List
    company_list.element_visible()
    company_list.find_company(code_input)
    company_list.click_view_button()

    # Company View
    company_view = CompanyView(driver)
    company_view.element_visible()
    text = company_view.check_filial_text()
    assert name_company == text, f'Error: {name_company} != {text}'

    company_view.click_navbar_button()
    company_view.click_checkbox()
    company_view.click_close_button()


def test_filial_create(driver, test_data):
    """Test adding a filial"""
    # Test data
    data = test_data["data"]
    filial_name = data["filial_name"]
    currency_code = data["base_currency_cod"]
    legal_person = data["legal_person_name"]

    # Login
    login_admin(driver, test_data, url='anor/mr/filial_list')

    # Open Filial List
    filial_list = FilialList(driver)
    filial_list.element_visible()
    filial_list.click_add_button()

    # Add Filial
    filial_add = FilialAdd(driver)
    filial_add.element_visible()
    filial_add.input_name(filial_name)
    filial_add.input_base_currency_name(currency_code)
    filial_add.input_person_name(legal_person)
    filial_add.click_save_button()

    # Verify in List
    filial_list.element_visible()
    filial_list.find_filial_row(filial_name)
    filial_list.click_view_button()

    # Verify in View
    filial_view = FilialView(driver)
    filial_view.element_visible()
    text = filial_view.check_filial_text()
    assert filial_name == text, f'Expected "{filial_name}", got "{text}"'

    filial_view.click_navbar_button()
    filial_view.click_project_checkbox()
    filial_view.click_checkbox_button()
    filial_view.click_save_button()
    filial_view.click_close_button()

    # Verify in List
    filial_list.element_visible()


def test_room_add(driver, test_data):
    """Test adding a room"""
    # Test data
    data = test_data["data"]
    room_name = data["room_name"]
    filial_name = data["filial_name"]

    # Login
    login_admin(driver, test_data, filial_name=filial_name, url='trade/trf/room_list')

    # Open Room List
    room_list = RoomList(driver)
    room_list.element_visible()
    room_list.click_add_button()

    # Add Room
    room_add = RoomAdd(driver)
    room_add.element_visible()
    room_add.input_name(room_name)
    room_add.click_save_button()

    # Verify in List
    room_list.element_visible()
    room_list.find_row(room_name)
    room_list.click_view_button()

    # Verify in View
    room_view = RoomView(driver)
    room_view.element_visible()
    text = room_view.check_room_name()
    assert text == room_name, f'Expected "{room_name}", got "{text}"'
    room_view.click_close_button()


def test_robot_add(driver, test_data):
    """Test adding a robot"""
    # Test data
    data = test_data["data"]
    filial_name = data["filial_name"]
    room_name = data["room_name"]
    robot_name = data["robot_name"]
    role_name = data["role_name"]

    # Login
    login_admin(driver, test_data, filial_name=filial_name, url='anor/mrf/robot_list')

    # Open Robot List
    robot_list = RobotList(driver)
    robot_list.element_visible()
    robot_list.click_add_button()

    # Add Robot
    robot_add = RobotAdd(driver)
    robot_add.element_visible()
    robot_add.input_name(robot_name)
    robot_add.input_roles(role_name)
    robot_add.input_rooms(room_name)
    robot_add.click_save_button()

    # Verify in List
    robot_list.element_visible()
    robot_list.find_row(robot_name)
    robot_list.click_view_button()

    # Verify in View
    robot_view = RobotView(driver)
    robot_view.element_visible()
    text = robot_view.check_robot_name()
    assert text == robot_name, f'Expected "{robot_name}", got "{text}"'
    robot_view.click_close_button()


def test_sub_filial_add(driver, test_data):
    """Test adding a sub-filial"""
    # Test data
    data = test_data["data"]
    filial_name = data["filial_name"]
    room_name = data["room_name"]
    sub_filial_name = data["sub_filial_name"]

    # Login
    login_admin(driver, test_data, filial_name=filial_name, url='anor/mrf/subfilial_list')

    # Open Sub-Filial List
    sub_filial_list = SubFilialList(driver)
    sub_filial_list.element_visible()
    sub_filial_list.click_add_button()

    # Add Sub-Filial
    sub_filial_add = SubFilialAdd(driver)
    sub_filial_add.element_visible()
    sub_filial_add.input_name(sub_filial_name)
    sub_filial_add.input_rooms(room_name)
    sub_filial_add.click_save_button()

    # Verify in List
    sub_filial_list.element_visible()
    sub_filial_list.click_reload_button()
    sub_filial_list.find_row(sub_filial_name)


def test_user_create(driver, test_data):
    """Test adding a user"""
    # Test data
    data = test_data["data"]
    filial_name = data["filial_name"]
    natural_person_name = data["natural_person_name"]
    password_user = data["password_user"]
    login_user = data["login_user"]
    robot_name = data["robot_name"]

    # Login
    login_admin(driver, test_data, filial_name=filial_name, url='anor/mr/user_list')

    # Open User List
    user_list = UserList(driver)
    user_list.element_visible()
    user_list.click_add_button()

    # Add User
    user_add = UserAdd(driver)
    user_add.element_visible()
    user_add.input_person_name(natural_person_name)
    user_add.input_password(password_user)
    user_add.click_mouse_down_button()
    user_add.input_login(login_user)
    user_add.input_robot(robot_name)
    user_add.click_save_button()

    # Verify in List
    user_list.element_visible()
    user_list.find_natural_person_row(natural_person_name)
    user_list.click_view_button()

    # Verify in View
    user_view = UserView(driver)
    user_view.element_visible()
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


def test_adding_permissions_to_user(driver, test_data):
    """Test adding permissions to a user"""
    # Test data
    data = test_data["data"]
    filial_name = data["filial_name"]
    role_name = data["role_name"]

    # Login
    login_admin(driver, test_data, filial_name=filial_name, url='trade/tr/role_list')

    # Open Role List
    role_list = RoleList(driver)
    role_list.element_visible()
    role_list.click_row_button(role_name)
    role_list.click_edit_button()

    # Edit Role
    role_edit = RoleEdit(driver)
    role_edit.element_visible()
    role_edit.checkbox_quantity()
    role_edit.click_checkboxes()
    role_edit.click_save_button()

    # Verify in List
    role_list.element_visible()
    role_list.click_row_button(role_name)
    role_list.click_view_button()

    # Verify in View
    role_view = RoleView(driver)
    role_view.element_visible()
    text = role_view.check_text()
    assert text == role_name, f'Expected "{role_name}", got "{text}"'

    # Grant all permissions
    role_view.click_navbar_button()
    role_view.click_detached_button()
    role_view.click_checkbox_form()
    role_view.click_access_all_button()
    time.sleep(2)
    role_view.click_close_button()


def test_user_change_password(driver, test_data):
    """Test changing user password"""
    # Test data
    data = test_data["data"]
    password_user = data["password_user"]

    # Login
    login_user(driver, test_data, dashboard_check=False, change_password_check=True,
                                  filial_name=False, url=False)
    # Change Password
    change_password = ChangePassword(driver)
    change_password.element_visible()
    change_password.input_new_password(password_user)
    change_password.input_rewritten_password(password_user)
    change_password.input_current_password(password_user)
    time.sleep(2)
    change_password.click_save_button()
    time.sleep(2)

# ----------------------------------------------------------------------------------------------------------------------

def price_type_add(driver, test_data, price_type_name=None, currency_name=None, all_price=False,
                   sub_filial=False, sub_filial_name=None):
    """Test adding a price type"""
    # Test data
    data = test_data["data"]
    room_name = data["room_name"]
    price_type_name_UZB = data["price_type_name_UZB"]
    price_type_name_USA = data["price_type_name_USA"]
    price_type_name = price_type_name_USA if price_type_name else price_type_name_UZB
    currency_name = currency_name or data["currency_name"]
    sub_filial_name = sub_filial_name or data["sub_filial_name"]

    # Login
    login_user(driver, test_data, url='anor/mkr/price_type_list')

    # Open Price Type List
    price_type_list = PriceTypeList(driver)
    price_type_list.element_visible()
    price_type_list.click_add_button()

    # Add Price Type
    price_type_add = PriceTypeAdd(driver)
    price_type_add.element_visible()
    price_type_add.input_name(price_type_name)
    price_type_add.input_rooms(room_name)
    price_type_add.input_currency(currency_name)
    if sub_filial:
        price_type_add.input_sub_filial(sub_filial_name)
    price_type_add.click_save_button()

    # Verify in List
    price_type_list.element_visible()
    price_type_list.find_row(price_type_name)
    price_type_list.click_view_button()

    # Verify in View
    price_type_view = PriceTypeIdView(driver)
    price_type_view.element_visible()
    text = price_type_view.get_elements()
    assert text == price_type_name, f'Expected "{price_type_name}", got "{text}"'
    price_type_view.click_close_button()

    if all_price:
        # Attach additional price types
        price_type_list.element_visible()
        price_type_list.click_add_dropdown_button()

        # Attach price types
        price_type_list_attach = PriceTypeListAttach(driver)

        name_a = 'Промо'
        price_type_list_attach.find_rows(name_a)

        price_type_list.element_visible()
        price_type_list.click_add_dropdown_button()
        name_b = 'Акция'
        price_type_list_attach.find_rows(name_b)

        price_type_list.element_visible()
        price_type_list.click_add_dropdown_button()
        name_c = 'Возврат'
        price_type_list_attach.find_rows(name_c)

        price_type_list.element_visible()
        price_type_list.click_add_dropdown_button()
        name_d = 'Передача забаланс'
        price_type_list_attach.find_rows(name_d)

        price_type_list.element_visible()
        price_type_list.click_add_dropdown_button()
        name_e = 'Обмен'
        price_type_list_attach.find_rows(name_e)

        price_type_list.element_visible()
        price_type_list.find_row(price_type_name)


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
    # Login
    login_user(driver, test_data, url='anor/mkr/payment_type_list')

    # Open Payment Type List
    payment_type_list = PaymentTypeList(driver)
    payment_type_list.element_visible()
    payment_type_list.click_attach_button()

    # Attach Payment Types
    payment_type_list_attach = PaymentTypeListAttach(driver)
    payment_type_list_attach.element_visible()
    payment_type_list_attach.click_checkbox_all()
    payment_type_list_attach.click_close_button()


def test_sector_add(driver, test_data):
    """Test adding a sector"""
    # Test data
    data = test_data["data"]
    sector_name = data["sector_name"]
    room_name = data["room_name"]

    # Login
    login_user(driver, test_data, url='anor/mr/sector_list')

    # Open Sector List
    sector_list = SectorList(driver)
    sector_list.element_visible()
    sector_list.click_add_button()

    # Add Sector
    sector_add = SectorAdd(driver)
    sector_add.element_visible()
    sector_add.input_name(sector_name)
    sector_add.input_rooms(room_name)
    sector_add.click_save_button()

    # Verify in List
    sector_list.element_visible()
    sector_list.find_row(sector_name)
    sector_list.click_view_button()

    # Verify in View
    sector_view = SectorView(driver)
    sector_view.element_visible()
    text = sector_view.check_sector_name()
    assert text == sector_name, f'Expected "{sector_name}", got "{text}"'
    sector_view.click_close_button()


def test_check_price_tag(driver, test_data):
    """Test checking a price tag"""
    # Test data
    data = test_data["data"]
    product_name = data["product_name"]
    price_type_name = data["price_type_name_UZB"]

    # Login
    login_user(driver, test_data, url='anor/mkr/price_type_list')

    # Price Type List
    price_type_list = PriceTypeList(driver)
    price_type_list.element_visible()
    price_type_list.find_row(price_type_name)
    price_type_list.click_price_tag_button()

    # Price Tag
    price_tag = PriceTag(driver)
    price_tag.element_visible()
    price_tag.input_product_name(product_name)
    price_tag.click_run_button()
    generate_and_verify_download(driver, file_name='PriceTag', file_type='xlsx')


def test_margin_add(driver, test_data):
    """Test adding a margin"""
    base_page = BasePage(driver)

    # Test data
    data = test_data["data"]
    margin_name = data["margin_name"]
    percent_value = data["percent_value"]

    # Login as Admin
    login_admin(driver, test_data, url='anor/mkr/margin_list')

    # Open Margin List - Admin
    margin_list_attach = MarginListAttach(driver)
    margin_list_attach.element_visible()
    try:
        margin_list_attach.find_row('')
    except ElementNotFoundError:
        base_page.logger.info(f"Element topilmadi, Logout qilinadi")
        logout(driver)
    else:
        margin_list_attach.click_delete_button()
        margin_list_attach.element_visible()
        logout(driver)

    # Login
    login_user(driver, test_data, url='anor/mkr/margin_list')

    # Open Margin List
    margin_list = MarginList(driver)
    margin_list.element_visible()
    margin_list.click_attach_button()

    # Open Margin List Attach
    margin_list_attach = MarginListAttach(driver)
    margin_list_attach.element_visible()
    margin_list_attach.click_add_button()

    # Add Margin
    margin_add = MarginAdd(driver)
    margin_add.element_visible()
    margin_add.click_name_button(margin_name)
    margin_add.click_percent_button(percent_value)
    margin_add.click_percent_type_radio_button(percent_type=1)
    margin_add.click_save_button()

    # Verify in List
    margin_list.element_visible()
    margin_list.click_attach_button()

    # Attach Margin
    margin_list_attach.element_visible()
    margin_list.find_row(margin_name)
    margin_list.click_attach_one_button()

    # Final Verification
    margin_list.element_visible()
    margin_list.find_row(margin_name)

# ----------------------------------------------------------------------------------------------------------------------

def test_room_attachment(driver, test_data):
    """Test attaching different elements to a room."""
    # Test data
    data = test_data["data"]
    warehouse_name = data["warehouse_name"]
    cash_register_name = data["cash_register_name"]
    client_name = data["client_name"]
    room_name = data["room_name"]

    # Login
    login_user(driver, test_data, url='trade/trf/room_list')

    # Room List
    room_list = RoomList(driver)
    room_list.element_visible()
    room_list.find_row(room_name)
    room_list.click_attachment_button()

    # Room Attachment
    room_attachment = RoomAttachment(driver)
    room_attachment.element_visible()

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


def test_init_balance(driver, test_data):
    """Test initializing inventory balance."""
    base_page = BasePage(driver)

    # Test data
    data = test_data["data"]
    product_name = data['product_name']
    product_quantity = data['product_quantity']
    product_price = data['product_price']

    # Login
    login_user(driver, test_data, url='anor/mkw/init_balance/init_inventory_balance_list')

    # Open Init Inventory Balance List
    init_balance_list = InitInventoryBalanceList(driver)
    init_balance_list.element_visible()
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
    init_balance_list.element_visible()
    init_balance_list.click_reload_button()
    init_balance_list.find_row(balance_number)
    init_balance_list.click_post_one_button()

    # Open Balance List
    base_page.switch_window(direction="prepare")
    cut_url = base_page.cut_url()
    base_page.switch_window(direction="new", url=cut_url + 'anor/mkw/balance/balance_list')

    balance_list = BalanceList(driver)
    balance_list.element_visible()
    balance_list.click_reload_button()
    balance_list.find_row(product_name)
    balance_list.click_detail_button()
    balance_list.click_reload_button()

    balance = balance_list.check_balance_quantity()
    assert balance == product_quantity, f"Error: Balance: '{balance}' != product_quantity: '{product_quantity}'"


def test_setting_consignment(driver, test_data):
    """Test enabling consignment settings."""
    system_setting = SystemSetting(driver)

    # Login
    login_user(driver, test_data, url='trade/pref/system_setting')

    # Open System Setting
    system_setting.element_visible()
    system_setting.click_navbar_button(navbar_button=6)

    # Configure Consignment
    system_setting.element_visible_order()
    if not system_setting.check_checkbox_text():
        system_setting.click_checkbox_consignment()
        system_setting.input_consignment_day_limit(day_limit=90)

    # Save Settings
    system_setting.click_save_button()


def test_order_request(driver, test_data):
    """Test creating an order request."""
    # Test data
    data = test_data["data"]
    room_name = data["room_name"]
    robot_name = data["robot_name"]
    client_name = data["client_name"]
    product_name = data["product_name"]
    product_quantity = data["product_quantity"]

    # Login
    login_user(driver, test_data, url='anor/mdeal/order/order_request_list')

    # Open Order Request List
    order_request_list = OrderRequestList(driver)
    order_request_list.element_visible()
    order_request_list.click_add_button()

    # Open Order Request Main
    order_request_add_main = OrderRequestAddMain(driver)
    order_request_add_main.element_visible()
    order_request_add_main.click_rooms_input(room_name)
    order_request_add_main.click_robots_input(robot_name)
    order_request_add_main.click_persons_input(client_name)
    order_request_add_main.click_next_step_button()

    # Open Order Request Product
    order_request_add_product = OrderRequestAddProduct(driver)
    order_request_add_product.element_visible()
    order_request_add_product.input_name(product_name)
    order_request_add_product.input_quantity(product_quantity)
    order_request_add_product.click_next_step_button()

    # Open Order Request Final
    order_request_add_final = OrderRequestAddFinal(driver)
    order_request_add_final.element_visible()
    request_number = random.randint(1, 99999)
    order_request_add_final.input_request_number(request_number)
    order_request_add_final.click_save_button()

    # Verify in Order Request List
    order_request_list.element_visible()
    order_request_list.find_row(client_name)
    order_request_list.click_view_button()

    # Verify in Order Request View
    order_request_view = OrderRequestView(driver)
    order_request_view.element_visible()
    text = order_request_view.check_number()
    assert text == request_number, f"Error: {text} != {request_number}"
    order_request_view.click_close_button()

    # Change status in Order Request List
    order_request_list.element_visible()
    order_request_list.click_status_button()

# ----------------------------------------------------------------------------------------------------------------------

def setting_prepayment(driver, test_data, prepayment=True):
    """Test enabling and configuring prepayment settings."""
    # Test data
    data = test_data["data"]
    status_name = data['Delivered']

    system_setting = SystemSetting(driver)

    # Login
    login_user(driver, test_data, url='trade/pref/system_setting')

    # System setting
    system_setting.element_visible()
    system_setting.click_navbar_button(navbar_button=6)
    system_setting.element_visible_order()
    if prepayment:
        if not system_setting.check_checkbox_prepayment():
            system_setting.click_checkbox_prepayment()
            system_setting.input_prepayment(status_name)
            system_setting.input_prepayment_min_percent(payment_min_percent=50)
    if not prepayment:
        if system_setting.check_checkbox_prepayment():
            system_setting.click_checkbox_prepayment()
    system_setting.click_save_button()
    system_setting.element_visible_order()


def test_setting_prepayment_on(driver, test_data):
    """Prepayment setting on"""

    setting_prepayment(driver, test_data, prepayment=True)


def test_setting_prepayment_off(driver, test_data):
    """Prepayment setting off"""

    setting_prepayment(driver, test_data, prepayment=False)


# ----------------------------------------------------------------------------------------------------------------------

def test_add_user_license(driver, test_data):
    """Test configuring add user license."""

    # Test data
    data = test_data["data"]
    natural_person_name = data['natural_person_name']

    # Login
    login_admin(driver, test_data, url='biruni/kl/license_list')

    # License List
    license_list = LicenseList(driver)
    license_list.element_visible()
    license_list.click_navbar_button()

    license_list.licence_visible()
    license_list.click_tbl_row_button()
    license_list.click_bind_user_button()

    # License User List
    license_user_list = LicenseUserList(driver)
    license_user_list.element_visible()
    license_user_list.click_all_checkbox()

    license_user_list.element_visible()
    license_user_list.click_detach_button()

    license_user_list.attach_button_visible()
    license_user_list.find_row(natural_person_name)
    license_user_list.click_attach_button()
    license_user_list.attach_button_visible()

# ----------------------------------------------------------------------------------------------------------------------

def test_add_van(driver, test_data):
    """Test adding a van"""

    # Test data
    van_name = "Malibu"
    carrying_name = 500
    van_number = "AB123456"

    # Login
    login_user(driver, test_data, url='anor/mrf/van_list')

    # VanList
    van_list = VanList(driver)
    van_list.element_visible()
    van_list.click_add_button()

    van_add = VanAdd(driver)
    van_add.element_visible()
    van_add.input_name(van_name)
    van_add.input_carrying(carrying_name)
    van_add.input_van_number(van_number)
    van_add.click_save_button()
    time.sleep(5)

# ----------------------------------------------------------------------------------------------------------------------