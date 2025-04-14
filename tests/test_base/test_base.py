import pytest
from autotest.biruni.md.biruni.grid_setting.grid_setting import GridSetting
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.core.md.base_page import BasePage
from autotest.core.md.login_page import LoginPage
from tests.conftest import test_data

from utils.exception import (
    ElementInteractionError,
    ElementVisibilityError,
    log_exception_chain
)


def logout(driver):
    try:
        base_page = BasePage(driver)
        login_page = LoginPage(driver)

        login_page.click_navbar_button()
        if login_page.click_logout_button():
            return True

    except Exception as e:
        base_page.logger.debug(f"Dashboard Page: Error: {str(e)}")
        raise

# ----------------------------------------------------------------------------------------------------------------------

def login(driver, email, password):
    try:
        base_page = BasePage(driver)
        login_page = LoginPage(driver)

        login_page.element_visible()
        login_page.fill_form(email, password)
        login_page.click_button()
        return True

    except Exception as e:
        base_page.logger.debug(f"Dashboard Page: Error: {str(e)}")
        raise

# ----------------------------------------------------------------------------------------------------------------------

def dashboard(driver):
    try:
        base_page = BasePage(driver)
        dashboard_page = DashboardPage(driver)

        if dashboard_page.element_visible_session():
            dashboard_page.click_button_delete_session()

        if not dashboard_page.element_visible():
            raise ElementVisibilityError
        return True

    except Exception as e:
        base_page.logger.debug(f"Dashboard Page: Error: {str(e)}")
        raise

# ----------------------------------------------------------------------------------------------------------------------

def login_system(driver, email, password, filial_name, url):
    try:
        base_page = BasePage(driver)
        dashboard_page = DashboardPage(driver)

        if not login(driver, email, password):
            raise ElementInteractionError

        if not dashboard(driver):
            raise ElementInteractionError

        dashboard_page.find_filial(filial_name)
        cut_url = base_page.cut_url()
        base_page.open_new_window(cut_url + url)
        return True

    except Exception as e:
        base_page.logger.debug(f"Dashboard Page: Error: {str(e)}")
        raise

# ----------------------------------------------------------------------------------------------------------------------

def login_admin(driver, test_data, filial_name=None, email=None, password=None, url=None):
    """Admin sifatida tizimga kirish."""
    try:
        base_page = BasePage(driver)

        data = test_data["data"]
        filial_name = filial_name or data["Administration_name"]
        email = email or data["email"]
        password = password or data["password"]
        url = url or 'trade/intro/dashboard'

        if not login_system(driver, email, password, filial_name, url):
            base_page.logger.error("login_admin: Admin login failed")
            raise ElementInteractionError
        return True

    except Exception as e:
        base_page.logger.debug(f"Dashboard Page: Error: {str(e)}")
        raise

# ----------------------------------------------------------------------------------------------------------------------

def login_user(driver, test_data, filial_name=None, email=None, password=None, url=None):
    """User sifatida tizimga kirish."""
    try:
        base_page = BasePage(driver)

        data = test_data["data"]
        filial_name = filial_name or data["filial_name"]
        email = email or data["email_user"]
        password = password or data["password_user"]
        url = url or 'trade/intro/dashboard'

        if not login_system(driver, email, password, filial_name, url):
            base_page.logger.error("login_user: User login failed")
            raise ElementInteractionError
        return True

    except Exception as e:
        base_page.logger.debug(f"Dashboard Page: Error: {str(e)}")
        raise

# ----------------------------------------------------------------------------------------------------------------------

def test_grid_setting_(driver, test_data, option_name=None):
    """Test configuring grid settings."""
    try:
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

    except AssertionError as ae:
        log_exception_chain(base_page.logger, ae)
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        log_exception_chain(base_page.logger, e)
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))

# ----------------------------------------------------------------------------------------------------------------------
