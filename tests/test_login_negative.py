import time
from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage


def run_test(driver, test_name, email, password, expect_success=False):

    login_page = LoginPage(driver)
    time.sleep(2)
    login_page.login(email, password, LoginPage.email_xpath, LoginPage.password_xpath, LoginPage.signup_xpath)

    if expect_success:
        result = login_page.is_dashboard_visible(DashboardPage.dashboard_header_xpath)
        success_message = "Log in Successful!"
        failure_message = "Log in Failed!"
    else:
        result = login_page.is_error_message_displayed(LoginPage.error_message_xpath)
        success_message = "Error message displayed"
        failure_message = "Failed to display error message"

        if not result:
            login_page.take_error_screenshot()

    print(f"\n{test_name}: {'Successful' if result else 'Failed'}")
    assert result, f"{test_name}: {failure_message}"
    print(f"{success_message}")


def test_login_with_invalid_credentials(driver):
    run_test(driver, "Incorrect login and password test", "invalid@test.com", "wrongpassword")


def test_login_with_empty_fields(driver):
    run_test(driver, "Empty fields test", "", "")


def test_login_with_invalid_email_format(driver):
    run_test(driver, "Incorrect email format Test", "invalidemail", "password123")


def test_login_with_short_password(driver):
    run_test(driver, "Short password test", "invalid@test.com", "123")


def test_login_with_valid_credentials(driver):
    run_test(driver, "Correct login and password test", "admin@test", "greenwhite", expect_success=True)