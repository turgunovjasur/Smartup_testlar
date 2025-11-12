import os
import json
import time
import shutil
import pytest
import tempfile
from datetime import datetime
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from pages.core.md.base_page import BasePage
from tests.ui.test_rep.integration.rep_main_funksiya import DOWNLOAD_DIR
from utils.assertions import SoftAssertions
from utils.env_reader import get_env
from utils.logger import configure_logging
from utils.email import send_email_report, format_test_results

# ======================================================================================================================

test_results = {
    'passed': [],
    'failed': [],
    'skipped': [],
    'errors': [],
    'start_time': None,
    'end_time': None
}

# ======================================================================================================================
# pytest hooks - test natijalarini yig'ish
# ======================================================================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Har bir test uchun natijani qayd qilish"""
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call':
        test_info = {
            'name': item.nodeid,
            'duration': report.duration,
        }

        if report.passed:
            test_results['passed'].append(test_info)
        elif report.failed:
            test_info['error'] = str(report.longrepr)
            test_results['failed'].append(test_info)
        elif report.skipped:
            test_info['reason'] = str(report.longrepr) if hasattr(report, 'longrepr') else 'Unknown'
            test_results['skipped'].append(test_info)

    # Setup yoki teardown xatolari
    elif report.failed and report.when in ['setup', 'teardown']:
        test_info = {
            'name': f"{item.nodeid} ({report.when})",
            'duration': report.duration,
            'error': str(report.longrepr)
        }
        test_results['errors'].append(test_info)

# ======================================================================================================================
# Yangi: Driver yaratish va tozalash funksiyalari (test_retry uchun)
# ======================================================================================================================

def create_driver(test_name, test_data):
    """Yangi driver yaratish (eski fixture logikasiga o'xshash, lekin request o'rniga test_name)."""
    logger = configure_logging(test_name)

    logger.info("=" * 80)
    logger.info(f"DRIVER YARATISH BOSHLANDI: {test_name}")
    logger.info("=" * 80)

    start_time = time.time()
    drv = None
    user_data_dir = None

    try:
        # Test ma'lumotlarini olish
        data = test_data["data"]
        url = data["url"]
        logger.info(f"Test URL: {url}")

        # ChromeDriver o'rnatish
        driver_path = ChromeDriverManager().install()
        service = ChromeService(driver_path)
        logger.debug(f"ChromeDriver o'rnatildi: {driver_path}")

        # Headless rejim - faqat environment variable orqali
        headless = os.getenv("GITHUB_ACTIONS") == "true"
        if headless:
            logger.info("Headless rejim yoqildi")
        else:
            logger.info("Normal rejim (GUI)")

        # Chrome options sozlash
        options = Options()

        if headless:
            options.add_argument("--headless=new")

        # Vaqtinchalik profil yaratish
        user_data_dir = tempfile.mkdtemp()
        logger.debug(f"Vaqtinchalik profil yaratildi: {user_data_dir}")
        options.add_argument(f"--user-data-dir={user_data_dir}")

        # Barcha argumentlarni qo'shish
        options.add_argument("--start-maximized")
        options.add_argument("--force-device-scale-factor=0.90")
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--incognito")
        options.add_argument("--disable-features=AutofillServerCommunication,PasswordManagerEnabled,PasswordCheck")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # Preferences sozlash
        all_prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "download.default_directory": DOWNLOAD_DIR,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", all_prefs)
        logger.debug(f"Yuklab olish katalogi: {DOWNLOAD_DIR}")

        # Chrome driver yaratish
        drv = webdriver.Chrome(service=service, options=options)
        logger.info(f"Browser ishga tushdi. Session ID: {drv.session_id}")

        # CDP orqali fayl yuklash sozlamalari
        try:
            drv.execute_cdp_cmd(
                "Page.setDownloadBehavior",
                {"behavior": "allow", "downloadPath": DOWNLOAD_DIR}
            )
        except Exception as e:
            logger.warning(f"CDP sozlashda xatolik: {e}")

        # Timeout sozlash
        drv.set_page_load_timeout(120)

        # URL ochish
        logger.info(f"URL ochilmoqda: {url}")
        drv.get(url)

        setup_time = time.time() - start_time
        logger.info("=" * 80)
        logger.info(f"DRIVER TAYYOR! Setup vaqti: {setup_time:.2f} sekund")
        logger.info("=" * 80)

        return drv, user_data_dir, start_time

    except WebDriverException as e:
        logger.error("=" * 80)
        logger.error(f"WEBDRIVER XATOLIK: {e}")
        logger.error("=" * 80)
        raise
    except Exception as e:
        logger.error("=" * 80)
        logger.error(f"KUTILMAGAN XATOLIK: {e}")
        logger.error("=" * 80)
        raise

# ======================================================================================================================

def cleanup_driver(drv, user_data_dir, logger, start_time, test_name):
    """Driver ni tozalash."""
    if drv:
        try:
            drv.quit()
            logger.info("Browser yopildi")
        except Exception as e:
            logger.warning(f"Browser yopishda xatolik: {e}")
    else:
        logger.warning("Driver yaratilmagan edi")

    if user_data_dir:
        try:
            shutil.rmtree(user_data_dir)
            logger.info("Vaqtinchalik profil o'chirildi")
        except Exception as e:
            logger.warning(f"Profil o'chirishda xatolik: {user_data_dir} - {e}")

    total_time = time.time() - start_time
    logger.info("=" * 80)
    logger.info(f"DRIVER SESSION TUGADI. Umumiy vaqt: {total_time:.2f} sekund")
    logger.info("=" * 80)

# ======================================================================================================================
# driver
# ======================================================================================================================

@pytest.fixture(scope="function")
def driver(request, test_data):
    """Driver yaratish, sozlash va tozalashning yagona joyi."""
    # Logger sozlash
    test_name = request.node.name
    logger = configure_logging(test_name)

    logger.info("=" * 80)
    logger.info(f"DRIVER YARATISH BOSHLANDI: {test_name}")
    logger.info("=" * 80)

    start_time = time.time()
    drv = None
    user_data_dir = None

    try:
        # Test ma'lumotlarini olish
        data = test_data["data"]
        url = data["url"]

        # ChromeDriver o'rnatish
        driver_path = ChromeDriverManager().install()
        service = ChromeService(driver_path)
        logger.debug(f"ChromeDriver o'rnatildi: {driver_path}")

        # Headless rejimni tekshirish
        headless = request.config.getoption("--headless", default=False)
        if headless or os.getenv("GITHUB_ACTIONS") == "true":
            logger.info("Headless rejim yoqildi")

        # Chrome options sozlash
        options = Options()

        if headless or os.getenv("GITHUB_ACTIONS") == "true":
            options.add_argument("--headless=new")

        # Vaqtinchalik profil yaratish
        user_data_dir = tempfile.mkdtemp()
        logger.debug(f"Vaqtinchalik profil yaratildi: {user_data_dir}")
        options.add_argument(f"--user-data-dir={user_data_dir}")

        # Barcha argumentlarni qo'shish
        options.add_argument("--start-maximized")
        options.add_argument("--force-device-scale-factor=0.90")
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--incognito")
        options.add_argument("--disable-features=AutofillServerCommunication,PasswordManagerEnabled,PasswordCheck")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # Preferences sozlash
        all_prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "download.default_directory": DOWNLOAD_DIR,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", all_prefs)
        logger.debug(f"Yuklab olish katalogi: {DOWNLOAD_DIR}")

        # Chrome driver yaratish
        drv = webdriver.Chrome(service=service, options=options)
        logger.info(f"Browser ishga tushdi. Session ID: {drv.session_id}")

        # CDP orqali fayl yuklash sozlamalari
        try:
            drv.execute_cdp_cmd(
                "Page.setDownloadBehavior",
                {"behavior": "allow", "downloadPath": DOWNLOAD_DIR}
            )
        except Exception as e:
            logger.warning(f"CDP sozlashda xatolik: {e}")

        # Timeout sozlash
        drv.set_page_load_timeout(120)

        # URL ochish
        logger.info(f"URL ochilmoqda: {url}")
        drv.get(url)

        setup_time = time.time() - start_time
        logger.info("=" * 80)
        logger.info(f"DRIVER TAYYOR! Setup vaqti: {setup_time:.2f} sekund")
        logger.info("=" * 80)

        yield drv

    except WebDriverException as e:
        logger.error("=" * 80)
        logger.error(f"WEBDRIVER XATOLIK: {e}")
        logger.error("=" * 80)
        raise
    except Exception as e:
        logger.error("=" * 80)
        logger.error(f"KUTILMAGAN XATOLIK: {e}")
        logger.error("=" * 80)
        raise
    finally:
        # Driver yopish
        if drv:
            try:
                drv.quit()
                logger.info("Browser yopildi")
            except Exception as e:
                logger.warning(f"Browser yopishda xatolik: {e}")
        else:
            logger.warning("Driver yaratilmagan edi")

        # Vaqtinchalik profil o'chirish
        if user_data_dir:
            try:
                shutil.rmtree(user_data_dir)
                logger.info("Vaqtinchalik profil o'chirildi")
            except Exception as e:
                logger.warning(f"Profil o'chirishda xatolik: {user_data_dir} - {e}")

        total_time = time.time() - start_time
        logger.info("=" * 80)
        logger.info(f"DRIVER SESSION TUGADI. Umumiy vaqt: {total_time:.2f} sekund")
        logger.info("=" * 80)

# ======================================================================================================================
# test_data
# ======================================================================================================================

@pytest.fixture(scope="session")
def cod_generator():
    """Test sessiyasi uchun yagona cod qiymati"""
    return datetime.today().strftime("%d_%m_%H_%M")

@pytest.fixture(scope="function")
def test_data(save_data, cod_generator):
    """Dinamik test ma'lumotlari"""

    cod = cod_generator
    # cod = "xtest"
    # cod = "xtest-1"
    save_data("cod", cod)

    base_data = {
        "email_company": get_env("EMAIL_COMPANY"),
        "password_company": get_env("PASSWORD_COMPANY"),
        "name_company": "red test",
        "plan_account": "UZ COA",
        "bank_name": "UZ BANK",
        "base_currency_cod": 860,
        "code_input": get_env("CODE_INPUT"),
        "cod": cod,
        "url": get_env("URL"),
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
        "password_user": get_env("PASSWORD_USER"),
    }
    product_data = {
        "legal_person_name": f"legal_person-{base_data['cod']}",
        "natural_person_name": f"natural_person-{base_data['cod']}",
        "client_name": f"client-{base_data['cod']}",
        "supplier_name": f"supplier-{base_data['cod']}",
        "contract_name": f"contract-{base_data['cod']}",
        "room_name": f"Test_room-{base_data['cod']}",
        "robot_name": f"Test_robot-{base_data['cod']}",
        "sub_filial_name": f"Test_sub_filial-{base_data['cod']}",
        "sector_name": f"Test_sector-{base_data['cod']}",
        "product_name": f"Test_product-{base_data['cod']}",
        "product_name_2": f"Test_product-{base_data['cod']}-2",
        "template_name": f"Test_invoice_report-{base_data['cod']}",
        "expense_article_name": f"Test_expense_article-{base_data['cod']}",
        "role_name": "Админ",
        "warehouse_name": "Основной склад",
        "minor_warehouse_name": "Minor warehouse",
        "cash_register_name": "Основная касса",
        "measurement_name": "Количество",
        "payment_type_name": "Наличные деньги",
        "price_tag_name": "Ценник",

        "price_type_name_UZB": f"Цена продажи UZB-{base_data['cod']}",
        "price_type_name_USA": f"Цена продажи USA-{base_data['cod']}",
        "margin_name": f"Test_margin-{base_data['cod']}",
        "percent_value": 5,
        "product_quantity": 1_000,

        "product_price": 12_000,
        "product_price_USA": 12,

        "product_weight_brutto": 1_100,
        "product_weight_brutto_2": 2_100,

        "product_weight_netto": 1_000,
        "product_weight_netto_2": 2_000,

        "product_litre": 100,
        "product_litre_2": 200,
    }
    order_status = {
        "Draft": "Черновик",
        "New": "Новый",
        "Processing": "В обработке",
        "Pending": "В ожидании",
        "Shipped": "Отгружен",
        "Delivered": "Доставлен",
        "Archive": "Архив",
        "Cancelled": "Отменен",
    }
    error_massage = {
        "error_massage_1": "H02-ANOR279-015",  # error -> contract
        "error_massage_2": "H02-ANOR279-006",  # error -> consignment
        "error_massage_3": "A02-16-120",
        "error_massage_4": "H02-ANOR66-003",   # error -> sector
        "error_massage_5": "A02-02-039",       # error -> data
        "error_massage_6": "H02-ANOR279-010",       # error -> data
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

# ======================================================================================================================
# save_data/load_data
# ======================================================================================================================

DATA_STORE_FILE = os.path.join(os.path.dirname(__file__), "data_store.json")

def get_data_file_path(request, file_name=None):
    base_dir = os.path.dirname(request.fspath)

    if file_name:
        return os.path.join(base_dir, file_name)

    return DATA_STORE_FILE

# ======================================================================================================================

@pytest.fixture
def save_data(request):
    logger = configure_logging(request.node.name)

    def _save(key, value, file_name=None):
        file_path = get_data_file_path(request, file_name=f"{file_name}.json" if file_name else None)
        data = {}

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}

        data[key] = value

        logger.info(f"[SAVE_DATA] {key} = {value}")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    return _save

# ======================================================================================================================

@pytest.fixture
def load_data(request):
    def _load(key, file_name=None):
        file_path = get_data_file_path(request, file_name=f"{file_name}.json" if file_name else None)

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    return data.get(key)
                except json.JSONDecodeError:
                    return None
        return None

    return _load

# ======================================================================================================================
# assertions
# ======================================================================================================================

@pytest.fixture
def base_page(driver):
    return BasePage(driver)

@pytest.fixture
def assertions(base_page):
    return base_page.assertions

@pytest.fixture
def soft_assertions(base_page):
    return SoftAssertions(page=base_page)

# ======================================================================================================================

from utils.test_retry import TestStateManager, get_test_summary, print_test_states

def pytest_sessionstart(session):
    """Test sessiyasi boshlanishida - mavjud kodni yangilang"""
    test_results['start_time'] = time.time()
    print("\n" + "=" * 70)
    print("🚀 TEST SESSIYASI BOSHLANDI")
    print("=" * 70)

    # ✨ YANGI: Test state faylini tozalash (ixtiyoriy)
    # Agar har safar yangi boshdan boshlashni istasangiz:
    # state_manager = TestStateManager()
    # state_manager.reset_all_states()
    # print("🔄 Test holatlari qayta tiklandi\n")

# ======================================================================================================================

def pytest_sessionfinish(session, exitstatus):
    """Test sessiyasi tugaganda - mavjud kodni yangilang"""
    test_results['end_time'] = time.time()
    total_duration = test_results['end_time'] - test_results['start_time']

    print("\n" + "=" * 70)
    print("🏁 TEST SESSIYASI TUGADI")
    print("=" * 70)

    # Natijalarni hisoblash
    passed_count = len(test_results['passed'])
    failed_count = len(test_results['failed'])
    skipped_count = len(test_results['skipped'])
    errors_count = len(test_results['errors'])

    print_test_states()
    get_test_summary()

    # Email uchun sarlavha
    status = "✅ PASSED" if failed_count == 0 and errors_count == 0 else "❌ FAILED"
    subject = f"{status} - Automation Test Natijalari ({datetime.now().strftime('%Y-%m-%d %H:%M')})"

    # Email uchun body
    body = format_test_results(
        passed=passed_count,
        failed=failed_count,
        skipped=skipped_count,
        errors=errors_count,
        total_duration=total_duration,
        test_details=test_results
    )

    # Emailni yuborish
    print("\n📧 Email yuborilmoqda...")
    send_email_report(subject, body)
    print("✅ Email yuborish jarayoni tugadi\n")

# ======================================================================================================================

@pytest.fixture(scope="session")
def test_state_manager():
    """Test state manager fixture - barcha testlar uchun umumiy"""
    return TestStateManager()

# ======================================================================================================================
