from autotest.core.md.login_page import LoginPage
from utils.driver_setup import driver


def run_test(driver, test_name, email, password, expect_success=False):
    login_xpath = "//div/input[@placeholder='Логин@компания']"
    password_xpath = "//div/input[@placeholder='Пароль']"
    signup_xpath = "//div/button[contains(text(), 'Войти')]"
    error_message_xpath = "//div/span[@id='error']"
    dashboard_header_xpath = "//div/h3[contains(text(), 'Trade')]"

    login_page = LoginPage(driver)
    login_page.login(email, password, login_xpath, password_xpath, signup_xpath)

    if expect_success:
        result = login_page.is_dashboard_visible(dashboard_header_xpath)
        success_message = "Log in Successful!"
        failure_message = "Log in Failed!"
    else:
        result = login_page.is_error_message_displayed(error_message_xpath)
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