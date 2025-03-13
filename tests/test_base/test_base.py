from autotest.core.md.base_page import BasePage
from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from utils.exception import LoaderTimeoutError, ElementInteractionError, ElementVisibilityError, ElementNotFoundError, \
    ElementNotClickableError
from tests.conftest import test_data


def logout(driver):
    login_page = LoginPage(driver)

    try:
        login_page.click_navbar_button()
        if login_page.click_logout_button():
            return True

    except (ElementNotClickableError, ElementInteractionError):
        raise

    except Exception:
        raise ElementInteractionError


def login(driver, email, password):
    login_page = LoginPage(driver)

    try:
        login_page.element_visible()
        login_page.fill_form(email, password)
        login_page.click_button()
        return True

    except (ElementNotClickableError, ElementInteractionError):
        raise

    except Exception:
        raise


def dashboard(driver):
    dashboard_page = DashboardPage(driver)

    try:
        if dashboard_page.element_visible_session():
            dashboard_page.click_button_delete_session()

        if not dashboard_page.element_visible():
            raise ElementVisibilityError
        return True

    except ElementInteractionError:
        raise

    except Exception:
        raise


def login_system(driver, email, password, filial_name, url):
    base_page = BasePage(driver)
    dashboard_page = DashboardPage(driver)

    try:
        if not login(driver, email, password):
            raise ElementInteractionError

        if not dashboard(driver):
            raise ElementInteractionError

        if filial_name:
            dashboard_page.find_filial(filial_name)

        if url:
            cut_url = base_page.cut_url()
            base_page.open_new_window(cut_url + url)

        return True

    except ElementInteractionError:
        raise

    except Exception:
        raise


def login_admin(driver, test_data, filial_name=None, email=None, password=None, url=None):
    """Admin sifatida tizimga kirish."""

    base_page = BasePage(driver)
    try:
        data = test_data["data"]
        filial_name = filial_name or data["Administration_name"]
        email = email or data["email"]
        password = password or data["password"]
        url = url or 'trade/intro/dashboard'

        if not login_system(driver, email, password, filial_name, url):
            base_page.logger.error("login_admin: Admin login failed")
            raise ElementInteractionError
        return True

    except ElementInteractionError:
        raise

    except Exception:
        raise


def login_user(driver, test_data, filial_name=None, email=None, password=None, url=None):
    """User sifatida tizimga kirish."""

    base_page = BasePage(driver)
    try:
        data = test_data["data"]
        filial_name = filial_name or data["filial_name"]
        email = email or data["email_user"]
        password = password or data["password_user"]
        url = url or 'trade/intro/dashboard'

        if not login_system(driver, email, password, filial_name, url):
            base_page.logger.error("login_user: User login failed")
            raise ElementInteractionError
        return True

    except ElementInteractionError:
        raise

    except Exception:
        raise
