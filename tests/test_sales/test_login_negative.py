import pytest
from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from selenium.common.exceptions import NoSuchElementException
from utils.driver_setup import driver


@pytest.mark.parametrize("email, password, test_name, expect_success", [
    ("admin@auto_test", "greenwhite", "valid_login_test", True),
    ("wrong_email@example.com", "wrongpassword", "invalid_login_test", False),
    # ("admin@auto_test", "wrongpassword", "valid_email_invalid_password", False),
    # ("", "greenwhite", "empty_email_test", False),
    # ("admin@auto_test", "", "empty_password_test", False),
])
# ------------------------------------------------------------------------------------------------------------------
def test_login(driver, email, password, test_name, expect_success):
    driver.implicitly_wait(2)

    login_page = LoginPage(driver)
    login_page.fill_form(email, password)
    login_page.click_button()

    dashboard_page = DashboardPage(driver)

    # ------------------------------------------------------------------------------------------------------------------

    try:
        if dashboard_page.element_visible_session(timeout=2) or dashboard_page.element_visible(timeout=2):
            if expect_success:
                print("Successfully logged in with correct information")
            else:
                print("Logged in with incorrect information")
                dashboard_page.take_screenshot(test_name)
        else:
            error_element = dashboard_page.wait_for_element_error(timeout=2)
            if error_element:
                print("Attempted to log in with incorrect information")
            else:
                print("Unknown error")
                dashboard_page.take_screenshot(test_name)
    except NoSuchElementException:
        print("Unable to log in")
        dashboard_page.take_screenshot(test_name)

    # driver.implicitly_wait(20)
    # ------------------------------------------------------------------------------------------------------------------
