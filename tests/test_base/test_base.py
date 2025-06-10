import time
from autotest.biruni.md.biruni.grid_setting.grid_setting import GridSetting
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.core.md.base_page import BasePage
from autotest.core.md.login_page import LoginPage
from tests.conftest import driver, test_data

# ======================================================================================================================

def logout(driver):
    login_page = LoginPage(driver)

    login_page.click_navbar_button()
    if login_page.click_logout_button():
        return True

# ======================================================================================================================

def login(driver, test_data, email, password):
    login_page = LoginPage(driver)

    data = test_data["data"]
    email = email or data["email"]
    password = password or data["password"]

    login_page.element_visible()
    login_page.fill_form(email, password)
    login_page.click_button()
    login_page.check_error_message_absence()

# ======================================================================================================================

def dashboard(driver, dashboard_check=False, change_password_check=False, filial_name=None, url=None):
    base_page = BasePage(driver)
    dashboard_page = DashboardPage(driver)

    if dashboard_page.element_visible_session():
        dashboard_page.click_button_delete_session()

    if dashboard_check:
        dashboard_page.element_visible_dashboard()

    if change_password_check:
        dashboard_page.element_visible_change_password()

    if filial_name:
        dashboard_page.find_filial(filial_name)

    if url:
        base_page.switch_window(direction="prepare")
        cut_url = base_page.cut_url()
        base_page.switch_window(direction="new", url=cut_url + url)

# ======================================================================================================================

def login_admin(driver, test_data,
                email=None, password=None,
                dashboard_check=None, change_password_check=None, filial_name=None, url=None):

    data = test_data["data"]
    email = email or data["email"]
    password = password or data["password"]

    login(driver, test_data, email, password)

    dashboard_check = True if (dashboard_check is None) else dashboard_check
    change_password_check = False if (change_password_check is None) else change_password_check
    if filial_name is None:
        filial_name = data["Administration_name"]
    if url is None:
        url = 'trade/intro/dashboard'

    dashboard(driver,
              dashboard_check=dashboard_check,
              change_password_check=change_password_check,
              filial_name=filial_name,
              url=url)

# ======================================================================================================================

def login_user(driver, test_data,
               email=None, password=None, dashboard_check=None,
               change_password_check=None, filial_name=None, url=None):

    data = test_data["data"]
    email = email or data["email_user"]
    password = password or data["password_user"]

    login(driver, test_data, email, password)

    dashboard_check = True if (dashboard_check is None) else dashboard_check
    change_password_check = False if (change_password_check is None) else change_password_check
    if filial_name is None:
        filial_name = data["filial_name"]
    if url is None:
        url = 'trade/intro/dashboard'

    dashboard(driver,
              dashboard_check=dashboard_check,
              change_password_check=change_password_check,
              filial_name=filial_name,
              url=url)

# ======================================================================================================================

def grid_setting(driver, test_data, option_name=None, search_type=None, save_as_default=False):
    """Test configuring grid settings."""

    # Grid Setting
    grid_setting = GridSetting(driver)
    grid_setting.click_group_button()
    grid_setting.element_visible()

    if option_name:
        grid_setting.click_options_button(option_name)
        time.sleep(0.5)

    if search_type:
        grid_setting.click_search_type_switch(search_type)
        time.sleep(0.5)

    if save_as_default:
        grid_setting.click_save_default_button()
        return

    grid_setting.click_save_button()
    time.sleep(0.5)

# ======================================================================================================================
