from autotest.core.md.login_page import LoginPage
from utils.driver_setup import driver


def run_test(driver, test_name, email, password, expect_success=False):

    # XPath'lar
    login_xpath = "//div/input[@placeholder='Логин@компания']"
    password_xpath = "//div/input[@placeholder='Пароль']"
    signup_xpath = "//div/button[contains(text(), 'Войти')]"
    error_message_xpath = "//div/span[@id='error']"
    dashboard_header_xpath = "//div/h3[contains(text(), 'Trade')]"
    # XPath'lar

    login_page = LoginPage(driver)
    login_page.login(email, password, login_xpath, password_xpath, signup_xpath)

    if expect_success:
        result = login_page.is_dashboard_visible(dashboard_header_xpath)
        success_message = "Tizimga kirish omadli!"
        failure_message = "Tizimga kirish omadsiz!"
    else:
        result = login_page.is_error_message_displayed(error_message_xpath)
        success_message = "Xato xabari ko'rsatildi"
        failure_message = "Xato xabari ko'rsatilmadi"

        if not result:
            login_page.take_error_screenshot()

    print(f"\n{test_name}: {'MUVAFFAQIYATLI' if result else 'MUVAFFAQIYATSIZ'}")
    assert result, f"{test_name}: {failure_message}"
    print(f"{success_message}")


def test_login_with_invalid_credentials(driver):
    run_test(driver, "Noto'g'ri login va parol testi", "invalid@test.com", "wrongpassword")


def test_login_with_empty_fields(driver):
    run_test(driver, "Bo'sh maydonlar testi", "", "")


def test_login_with_invalid_email_format(driver):
    run_test(driver, "Noto'g'ri email formati testi", "invalidemail", "password123")


def test_login_with_short_password(driver):
    run_test(driver, "Qisqa parol testi", "invalid@test.com", "123")


def test_login_with_valid_credentials(driver):
    run_test(driver, "To'g'ri login va parol testi", "admin@test", "greenwhite", expect_success=True)
