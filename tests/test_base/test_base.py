import time
import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from autotest.core.md.base_page import BasePage
from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage


def test_data():
    """Test data"""
    base_data = {
        "email_company": "admin@head",
        "password_company": "greenwhite",
        "code_input": "red_test",
        # "code_input": "autotest",
        "name_company": "red test",
        "plan_account": "UZ COA",
        "bank_name": "UZ BANK",
        "base_currency_cod": 860,
        "cod": 25,
    }
    filial_data = {
        "email": f"admin@{base_data['code_input']}",
        "password": f"{base_data['password_company']}",
        "Administration_name": "Администрирование",
        "filial_name": f"Test_filial-{base_data['cod']}",
        "login_user": f"test-{base_data['cod']}",
    }
    user_data = {
        "email_user": f'{filial_data["login_user"]}@{base_data["code_input"]}',
        "password_user": 123456789,
    }
    product_data = {
        "legal_person_name": f"legal_person-{base_data['cod']}",
        "natural_person_name": f"natural_person-{base_data['cod']}",
        "client_name": f"client-{base_data['cod']}",
        "contract_name": f"contract-{base_data['cod']}",
        "room_name": f"Test_room-{base_data['cod']}",
        "robot_name": f"Test_robot-{base_data['cod']}",
        "sector_name": f"Test_sector-{base_data['cod']}",
        "product_name": f"Test_product-{base_data['cod']}",
        "role_name": "Админ",
        "warehouse_name": "Основной склад",
        "cash_register_name": "Основная касса",
        "measurement_name": "Количество",
        "price_type_name": f"Цена продажи-{base_data['cod']}",
        "payment_type_name": "Наличные деньги",
        # "test_quantity": 10,
        "product_quantity": 1_000,
        "product_price": 12_000,
    }
    order_status = {
        "Draft": "Черновик",
        "New": "Новый",
        "Processing": "В обработке",
        "Pending": "В ожидании",
        "Shipped": "Отгружен",
        "Delivered": "Доставлен",
        "Archive": "Архив"
    }
    error_massage = {
        "error_massage_1": "H02-ANOR279-015",
    }
    return {
        "data": {
            **base_data,
            **filial_data,
            **user_data,
            **product_data,
            **order_status,
            **error_massage
        }
    }


def get_driver():
    """Enhanced driver setup with additional error handling"""
    try:
        service = ChromeService(ChromeDriverManager().install())
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--force-device-scale-factor=0.90")
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        options.add_argument("--disable-software-rasterizer")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--log-level=3")

        driver = webdriver.Chrome(service=service, options=options)
        driver.get("http://gw.greenwhite.uz:8081/xtrade/login.html")
        # driver.get("https://smartup.online/login.html")
        return driver

    except Exception as e:
        print(f"Failed to initialize WebDriver: {str(e)}")
        raise


def open_new_window(driver, url):
    base_page = BasePage(driver)

    try:
        if not base_page._wait_for_page_load(timeout=60):
            base_page.logger.error(f"❌Page did not load(): timeout = 60s!")
            return False

        base_page.logger.info("Opening a new browser window.")
        driver.execute_script("window.open('');")
        all_windows = driver.window_handles
        driver.switch_to.window(all_windows[-1])
        driver.get(url)
        base_page.logger.info(f"Navigated to URL: {url}")
        time.sleep(2)

        return True

    except Exception as e:
        base_page.logger.error(f"❌Error message(): {e}")
        base_page.take_screenshot("open_new_window_error")
        raise


def login(driver, email, password):
    # Log
    base_page = BasePage(driver)
    login_page = LoginPage(driver)

    try:
        if not base_page._wait_for_page_load(timeout=60):
            base_page.logger.error("❌Login_page did not load(): timeout = 60s!")
            return False

        base_page.logger.info("Login_page loaded successfully.")
        login_page.fill_form(email, password)
        base_page.logger.info(f"Form filled with email: {email}")
        login_page.click_button()
        base_page.logger.info("Login button clicked.")
        return True

    except Exception as e:
        base_page.logger.error(f"❌Error message(): {e}")
        base_page.take_screenshot("login_error")
        raise


def dashboard(driver):
    # Log
    base_page = BasePage(driver)
    dashboard_page = DashboardPage(driver)

    try:
        if not base_page._wait_for_page_load(timeout=60):
            base_page.logger.error("❌Dashboard did not load()")
            return False

        base_page.logger.info("Dashboard loaded successfully.")
        dashboard_page.element_visible_session()
        return True

    except Exception as e:
        base_page.logger.error(f"❌Error message(): {e}")
        base_page.take_screenshot("dashboard_error")
        raise


def login_system(driver, email, password, filial_name, url):
    # Login
    login(driver, email, password)

    # Dashboard
    dashboard(driver)
    dashboard_page = DashboardPage(driver)

    if not filial_name is False:
        dashboard_page.find_filial(filial_name)

    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    if not url is False:
        open_new_window(driver, cut_url + url)


def login_admin(driver, filial_name=None, email=None, password=None, url=None):
    # Test data
    data = test_data()["data"]
    filial_name = filial_name if filial_name is not None else data["Administration_name"]
    email = email if email is not None else data["email"]
    password = password if password is not None else data["password"]
    url = url if url is not None else 'trade/intro/dashboard'

    # Authorization
    login_system(driver, email, password, filial_name, url)


def login_user(driver, filial_name=None, email=None, password=None, url=None):
    # Test data
    data = test_data()["data"]
    filial_name = filial_name if filial_name is not None else data["filial_name"]
    email = email if email is not None else data["email_user"]
    password = password if password is not None else data["password_user"]
    url = url if url is not None else 'trade/intro/dashboard'

    # Authorization
    login_system(driver, email, password, filial_name, url)
