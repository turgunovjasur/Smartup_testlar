import json
import os
import shutil
import pytest
import tempfile
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from pages.core.md.base_page import BasePage
from tests.ui.test_rep.integration.rep_main_funksiya import DOWNLOAD_DIR
from utils.assertions import SoftAssertions
from utils.env_reader import get_env

# ----------------------------------------------------------------------------------------------------------------------
# driver
# ----------------------------------------------------------------------------------------------------------------------

def _build_driver(request, test_data):
    """
    driver yaratishning yagona joyi.
    driver fixture ham, driver_factory ham shu funksiyani chaqiradi.
    """
    data = test_data["data"]
    url = data["url"]

    driver_path = ChromeDriverManager().install()
    service = ChromeService(driver_path)

    headless = request.config.getoption("--headless", default=False)
    options = Options()

    if headless or os.getenv("GITHUB_ACTIONS") == "true":
        options.add_argument("--headless=new")

    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")

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

    all_prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", all_prefs)

    drv = webdriver.Chrome(service=service, options=options)

    # 📌 Fayl yuklashga ruxsat (CDP)
    try:
        drv.execute_cdp_cmd(
            "Page.setDownloadBehavior",
            {"behavior": "allow", "downloadPath": DOWNLOAD_DIR}
        )
    except Exception:
        pass

    drv.set_page_load_timeout(120)
    print(f"[driver] session_id={drv.session_id}")
    drv.get(url)

    def _finalize(d=drv, profile=user_data_dir):
        try:
            d.quit()
        except Exception:
            pass
        try:
            shutil.rmtree(profile)
        except Exception as e:
            print(f"[Warning] Profilni o‘chirishda xatolik: {profile} ({e})")

    request.addfinalizer(_finalize)
    return drv

@pytest.fixture(scope="function")
def driver_factory(request, test_data):
    """
    Retry uchun yangi driver beradigan "factory".
    """
    def _create():
        return _build_driver(request, test_data)
    return _create

@pytest.fixture(scope="function")
def driver(driver_factory):
    """
    1-urinish uchun odatdagi driver fixture.
    Kodni takrorlamaymiz — ichida _build_driver chaqiriladi.
    """
    drv = driver_factory()
    # Teardown’ni alohida yozish shart emas — finalizer ichida tozalanadi.
    yield drv

# ----------------------------------------------------------------------------------------------------------------------
# test_data
# ----------------------------------------------------------------------------------------------------------------------

@pytest.fixture(scope="session")
def cod_generator():
    """Test sessiyasi uchun yagona cod qiymati"""
    return datetime.today().strftime("%d_%m_%H_%M")

@pytest.fixture(scope="function")
def test_data(save_data, cod_generator):
    """Dinamik test ma'lumotlari"""

    cod = cod_generator
    # cod = "8"
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

# ----------------------------------------------------------------------------------------------------------------------
# save_data/load_data
# ----------------------------------------------------------------------------------------------------------------------

DATA_STORE_FILE = os.path.join(os.path.dirname(__file__), "data_store.json")

# Fayl manzilini aniqlovchi funksiya
def get_data_file_path(request, file_name=None):
    base_dir = os.path.dirname(request.fspath)

    if file_name:  # alohida nom berilgan bo‘lsa, test fayli yonida saqlanadi
        return os.path.join(base_dir, file_name)

    # default: umumiy data_store.json
    return DATA_STORE_FILE

# JSON ga ma'lumot yozuvchi fixture
@pytest.fixture
def save_data(request):
    def _save(key, value, file_name=None):
        file_path = get_data_file_path(request, file_name=file_name)
        data = {}

        # Fayl mavjud bo‘lsa, mavjud ma’lumotlarni o‘qib olamiz
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}

        # Yangi qiymatni yozamiz
        data[key] = value

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    return _save

# JSON dan ma'lumot o‘quvchi fixture
@pytest.fixture
def load_data(request):
    def _load(key, file_name=None):
        file_path = get_data_file_path(request, file_name=file_name)

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    return data.get(key)
                except json.JSONDecodeError:
                    return None
        return None

    return _load

# ----------------------------------------------------------------------------------------------------------------------
# assertions
# ----------------------------------------------------------------------------------------------------------------------

@pytest.fixture
def base_page(driver):
    return BasePage(driver)

@pytest.fixture
def assertions(base_page):
    """Assertion klassi uchun fixture"""
    return base_page.assertions

@pytest.fixture
def soft_assertions(base_page):
    """Soft assertion klassi uchun fixture"""
    return SoftAssertions(page=base_page)

# ----------------------------------------------------------------------------------------------------------------------
