import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from utils.driver_setup import driver


def run_test(driver, test_name, email, password, expect_success=False):
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    time.sleep(2)

    # Login
    login_page.fill_form(email, password, LoginPage.email_xpath, LoginPage.password_xpath)
    login_page.click_button(LoginPage.signup_xpath)

    if expect_success:
        result = is_dashboard_visible(driver, DashboardPage.dashboard_header)
        success_message = "Tizimga kirish muvaffaqiyatli!"
        failure_message = "Tizimga kirish muvaffaqiyatsiz tugadi!"
    else:
        result = is_error_message_displayed(driver)
        success_message = "Xato xabari ko'rsatildi"
        failure_message = "Xato xabarini ko'rsatishda xatolik yuz berdi"

    if not result:
        take_error_screenshot(driver, test_name)

    print(f"\n{test_name}: {'Muvaffaqiyatli' if result else 'Muvaffaqiyatsiz'}")
    assert result, f"{test_name}: {failure_message}"
    print(f"{success_message}")


def is_dashboard_visible(driver, dashboard_header, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, dashboard_header))
        )
        return True
    except:
        return False


def is_error_message_displayed(driver, timeout=5):
    error_message_xpath = "id('error')"
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, error_message_xpath))
        )
        return True
    except:
        return False


def take_error_screenshot(driver, test_name):
    from datetime import datetime
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_name = f"error_{test_name}_{current_time}.png"
    driver.save_screenshot(screenshot_name)
    print(f"Screenshot saved as {screenshot_name}")


def test_login_with_invalid_credentials(driver):
    run_test(driver, "Noto'g'ri login va parol testi", "invalid@test.com", "wrongpassword")


def test_login_with_empty_fields(driver):
    run_test(driver, "Bo'sh maydonlar testi", "", "")


def test_login_with_invalid_email_format(driver):
    run_test(driver, "Noto'g'ri email formati testi", "invalidemail", "password123")


def test_login_with_short_password(driver):
    run_test(driver, "Qisqa parol testi", "valid@test.com", "123")


def test_login_with_valid_credentials(driver):
    run_test(driver, "To'g'ri login va parol testi", "admin@gws", "correctpassword", expect_success=True)


def run_all_tests(driver):
    tests = [
        test_login_with_invalid_credentials,
        test_login_with_empty_fields,
        test_login_with_invalid_email_format,
        test_login_with_short_password,
        test_login_with_valid_credentials
    ]


if __name__ == "__main__":
    try:
        run_all_tests(driver)
    finally:
        driver.quit()
















# import time
# from autotest.core.md.login_page import LoginPage
# from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
# from utils.driver_setup import driver
#
#
# def run_test(driver, test_name, email, password, expect_success=False):
#     email = 'admin@auto_test'
#     password = ''
#     login_page = LoginPage(driver)
#     time.sleep(2)
#     login_page.login(email, password, LoginPage.email_xpath, LoginPage.password_xpath, LoginPage.signup_xpath)
#
#     if expect_success:
#         result = login_page.is_dashboard_visible(DashboardPage.dashboard_header)
#         success_message = "Log in Successful!"
#         failure_message = "Log in Failed!"
#     else:
#         result = login_page.is_error_message_displayed(LoginPage.error_message_xpath)
#         success_message = "Error message displayed"
#         failure_message = "Failed to display error message"
#
#         if not result:
#             login_page.take_error_screenshot()
#
#     print(f"\n{test_name}: {'Successful' if result else 'Failed'}")
#     assert result, f"{test_name}: {failure_message}"
#     print(f"{success_message}")
#
#
# def test_login_with_invalid_credentials(driver):
#     run_test(driver, "Incorrect login and password test", "invalid@test.com", "wrongpassword")
#
#
# def test_login_with_empty_fields(driver):
#     run_test(driver, "Empty fields test", "", "")
#
#
# def test_login_with_invalid_email_format(driver):
#     run_test(driver, "Incorrect email format Test", "invalidemail", "password123")
#
#
# def test_login_with_short_password(driver):
#     run_test(driver, "Short password test", "invalid@test.com", "123")
#
#
# def test_login_with_valid_credentials(driver):
#     run_test(driver, "Correct login and password test", "admin@gws", "", expect_success=True)
