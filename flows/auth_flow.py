from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.core.md.base_page import BasePage
from autotest.core.md.login_page import LoginPage

# ======================================================================================================================

def logout(driver):
    login_page = LoginPage(driver)
    login_page.click_navbar_button()
    login_page.click_logout_button()

# ======================================================================================================================

def login(driver, email, password):
    login_page = LoginPage(driver)
    login_page.element_visible()
    login_page.fill_form(email, password)
    login_page.click_button()
    login_page.check_error_message_absence()

# ======================================================================================================================

def dashboard(driver, dashboard_check, change_password_check, filial_name, url):
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

def login_admin(driver, test_data, **kwargs):

    data = test_data["data"]
    email = kwargs.get("email", data["email"])
    password = kwargs.get("password", data["password"])

    login(driver, email, password)

    dashboard_check = kwargs.get("dashboard_check", True)
    change_password_check = kwargs.get("change_password_check", False)
    filial_name = kwargs.get("filial_name", data["Administration_name"])
    url = kwargs.get("url", 'trade/intro/dashboard')

    dashboard(driver, dashboard_check, change_password_check, filial_name, url)

# ======================================================================================================================

def login_user(driver, test_data, **kwargs):

    data = test_data["data"]
    email = kwargs.get("email", data["email_user"])
    password = kwargs.get("password", data["password_user"])

    login(driver, email, password)

    dashboard_check = kwargs.get("dashboard_check", True)
    change_password_check = kwargs.get("change_password_check", False)
    filial_name = kwargs.get("filial_name", data["filial_name"])
    url = kwargs.get("url", 'trade/intro/dashboard')

    dashboard(driver, dashboard_check, change_password_check, filial_name, url)

# ======================================================================================================================