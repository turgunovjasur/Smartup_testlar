from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException

from autotest.core.md.base_page import BasePage
from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage

from webdriver_manager.chrome import ChromeDriverManager


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
        "cod": 35,
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
        "sub_filial_name": f"Test_sub_filial-{base_data['cod']}",
        "sector_name": f"Test_sector-{base_data['cod']}",
        "product_name": f"Test_product-{base_data['cod']}",
        "role_name": "Админ",
        "warehouse_name": "Основной склад",
        "cash_register_name": "Основная касса",
        "measurement_name": "Количество",

        "price_type_name_UZB": f"Цена продажи UZB-{base_data['cod']}",
        "price_type_name_USA": f"Цена продажи USA-{base_data['cod']}",

        "margin_name": f"Test_margin-{base_data['cod']}",
        "percent_value": 5,

        "payment_type_name": "Наличные деньги",
        "product_quantity": 1_000,
        "product_price": 12_000,
        "product_price_USA": 12,
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
        "error_massage_2": "H02-ANOR279-006",
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
        driver.get("https://app3.greenwhite.uz/xtrade/login.html")
        # driver.get("http://gw.greenwhite.uz:8081/xtrade/login.html")
        # driver.get("https://smartup.online/login.html")
        return driver

    except Exception as e:
        print(f"Failed to initialize WebDriver: {str(e)}")
        raise


def open_new_window(driver, url: str) -> bool:
    """Yangi oynada URL ochish."""

    base_page = BasePage(driver)

    try:
        base_page._wait_for_all_loaders()

        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(url)

        if base_page._wait_for_all_loaders():
            base_page.logger.info(f"URL muvaffaqiyatli ochildi: {url}")
            return True
        else:
            base_page.logger.error("Sahifa to'liq yuklanmadi")
            return False

    except Exception as e:
        base_page.logger.error(f"Yangi oyna ochishda xato: {str(e)}", exc_info=True)
        base_page.take_screenshot("open_new_window_error")
        raise WebDriverException(f"Yangi oyna ochishda xato: {str(e)}")


def logout(driver):
    # Log
    base_page = BasePage(driver)
    login_page = LoginPage(driver)
    try:
        login_page.click_navbar_button()
        login_page.click_logout_button()
        base_page.logger.info("Logout successfully.")

    except Exception as e:
        base_page.logger.error(f"❌Error: logout_error(): {e}")
        base_page.take_screenshot("logout_error")
        raise


def login(driver, email, password):
    base_page = BasePage(driver)
    login_page = LoginPage(driver)

    if not base_page._wait_for_all_loaders():
        return False

    if not login_page.element_visible():
        base_page.logger.error("Login jarayonida xatolik")
        return False

    if not login_page.fill_form(email, password):
        base_page.logger.error("Email yoki parolni kiritishda xatolik")
        return False

    login_page.click_button()
    return True


def dashboard(driver):
    base_page = BasePage(driver)
    dashboard_page = DashboardPage(driver)

    if not base_page._wait_for_all_loaders():
        return False

    if dashboard_page.element_visible_session() is True:
        dashboard_page.click_button_delete_session()
        base_page.logger.info("Eski sessiya muvaffaqiyatli o'chirildi")

    if dashboard_page.element_visible():
        base_page.logger.info("Tizim muvaffaqiyatli ochildi")
        return True

    base_page.logger.error(f"Tizimga kirishda xatolik yuz berdi")
    return False


def login_system(driver, email, password, filial_name, url):
    base_page = BasePage(driver)
    dashboard_page = DashboardPage(driver)

    if not login(driver, email, password):
        return False

    if not dashboard(driver):
        return False

    if filial_name:
        dashboard_page.find_filial(filial_name)

    if url:
        cut_url = base_page.cut_url()
        open_new_window(driver, cut_url + url)

    return True


def login_admin(driver, filial_name=None, email=None, password=None, url=None):
    """Admin sifatida tizimga kirish."""

    data = test_data()["data"]
    filial_name = filial_name if filial_name is not None else data["Administration_name"]
    email = email if email is not None else data["email"]
    password = password if password is not None else data["password"]
    url = url if url is not None else 'trade/intro/dashboard'

    if not login_system(driver, email, password, filial_name, url):
        return False
    return True


def login_user(driver, filial_name=None, email=None, password=None, url=None):
    """Oddiy foydalanuvchi sifatida tizimga kirish."""

    data = test_data()["data"]
    filial_name = filial_name if filial_name is not None else data["filial_name"]
    email = email if email is not None else data["email_user"]
    password = password if password is not None else data["password_user"]
    url = url if url is not None else 'trade/intro/dashboard'

    if not login_system(driver, email, password, filial_name, url):
        return False
    return True
