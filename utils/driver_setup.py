import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver(request):
    # Chrome driver sozlamalari
    service = ChromeService(ChromeDriverManager().install())
    options = Options()

    # Browser sozlamalari
    options.add_argument("--start-maximized")  # Oynani maksimal o'lchamda ochish
    options.add_argument("--force-device-scale-factor=0.90")  # Masshtabni sozlash
    options.add_argument('--ignore-ssl-errors=yes')  # SSL xatoliklarni e'tiborsiz qoldirish
    options.add_argument('--ignore-certificate-errors')  # Sertifikat xatoliklarini e'tiborsiz qoldirish
    options.add_argument('--disable-gpu')  # GPU bilan bog'liq xatoliklarni oldini olish
    options.add_argument('--no-sandbox')  # Xavfsizlik rejimini o'chirish
    options.add_argument('--disable-dev-shm-usage')  # Xotira bilan bog'liq xatoliklarni oldini olish

    # Driver yaratish
    driver = webdriver.Chrome(service=service, options=options)

    # Test URL ga o'tish
    driver.get("http://gw.greenwhite.uz:8081/xtrade/login.html")

    # Alternativ URLlar:
    # driver.get("http://localhost:8080/smartup5x_trade_patch/")
    # driver.get("https://smartup.online/login.html")

    yield driver

    driver.quit()
