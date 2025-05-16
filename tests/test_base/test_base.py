from autotest.biruni.md.biruni.grid_setting.grid_setting import GridSetting
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.core.md.base_page import BasePage
from autotest.core.md.login_page import LoginPage
from tests.conftest import driver, test_data


def logout(driver):
    login_page = LoginPage(driver)

    login_page.click_navbar_button()
    if login_page.click_logout_button():
        return True

# ----------------------------------------------------------------------------------------------------------------------

def login(driver, test_data, email, password):
    login_page = LoginPage(driver)

    data = test_data["data"]
    email = email or data["email"]
    password = password or data["password"]

    assert login_page.element_visible(), "LoginPage not open!"
    login_page.fill_form(email, password)
    login_page.click_button()

# ----------------------------------------------------------------------------------------------------------------------

def dashboard(driver, dashboard_check=False, change_password_check=False, filial_name=None, url=None):
    base_page = BasePage(driver)
    dashboard_page = DashboardPage(driver)

    if dashboard_page.element_visible_session():
        dashboard_page.click_button_delete_session()

    if dashboard_check:
        assert dashboard_page.element_visible_dashboard(), "DashboardPage not open!"

    if change_password_check:
        assert dashboard_page.element_visible_change_password(), "ChangePassword Page not open!"

    if filial_name:
        dashboard_page.find_filial(filial_name)

    if url:
        cut_url = base_page.cut_url()
        base_page.switch_window(direction="new", url=cut_url + url)


# ----------------------------------------------------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------------------------------------------------

def test_grid_setting_(driver, test_data, option_name=None):
    """Test configuring grid settings."""
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_grid_setting")

    # List
    grid_setting = GridSetting(driver)
    grid_setting.click_group_button()

    # Grid Setting
    assert grid_setting.element_visible(), 'GridSetting not open!'
    grid_setting.click_options_button(option_name)
    grid_setting.click_save_button()

    base_page.logger.info(f"✅Test end: test_grid_setting")

# ----------------------------------------------------------------------------------------------------------------------
