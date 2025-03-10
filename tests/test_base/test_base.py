from autotest.core.md.base_page import BasePage
from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from utils.exception import LoaderTimeoutError, ElementInteractionError, ElementVisibilityError, ElementNotFoundError
from tests.conftest import test_data


def logout(driver):
    # Log
    base_page = BasePage(driver)
    login_page = LoginPage(driver)
    try:
        login_page.click_navbar_button()
        if login_page.click_logout_button():
            base_page.logger.info("Tizimdan chiqish muvaffaqiyatli amalga oshirildi")
            return True
    except Exception:
        base_page.logger.error(f"Tizimdan chiqishda xatolik yuz berdi")
        return False


def login(driver, email, password):
    base_page = BasePage(driver)
    login_page = LoginPage(driver)

    try:
        base_page._wait_for_all_loaders(log_text='Login Page')
        login_page.element_visible()
        login_page.fill_form(email, password)
        login_page.click_button()
        return True

    except (LoaderTimeoutError, ElementVisibilityError, ElementInteractionError) as e:
        base_page.logger.error(e.message)
        raise

    except Exception as e:
        base_page.logger.error(f"Login Page: -> Unexpected error {str(e)}")
        raise


def dashboard(driver):
    base_page = BasePage(driver)
    dashboard_page = DashboardPage(driver)

    try:
        base_page._wait_for_all_loaders(log_text='Dashboard Page')

        if dashboard_page.element_visible_session():
            dashboard_page.click_button_delete_session()

        if not dashboard_page.element_visible():
            base_page.logger.error("Dashboard Page: Verification failed - elements not found")
            raise ElementInteractionError("Dashboard Page: Failed to open")

        return True

    except (LoaderTimeoutError, ElementVisibilityError, ElementInteractionError) as e:
        base_page.logger.error(e.message)
        raise

    except Exception as e:
        base_page.logger.error(f"Dashboard Page: -> Unexpected error {str(e)}")
        raise


def login_system(driver, email, password, filial_name, url):
    base_page = BasePage(driver)
    dashboard_page = DashboardPage(driver)

    try:
        login(driver, email, password)
        dashboard(driver)

        if filial_name:
            dashboard_page.find_filial(filial_name)

        if url:
            cut_url = base_page.cut_url()
            base_page.open_new_window(cut_url + url)

        return True

    except (ElementNotFoundError, ElementInteractionError) as e:
        base_page.logger.error(e.message)
        raise

    except Exception as e:
        base_page.logger.error(f"login_system: -> Unexpected error {str(e)}")
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
            raise

        return True

    except Exception as e:
        base_page.logger.error(f"login_admin: -> Unexpected error: {str(e)}")
        return False


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
            raise

        return True

    except Exception as e:
        base_page.logger.error(f"login_user: -> Unexpected error: {str(e)}")
        return False
