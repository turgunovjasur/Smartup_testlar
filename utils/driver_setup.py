import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tests.conftest import test_data


@pytest.fixture
def driver(request, test_data):
    data = test_data["data"]
    url = data["url"]

    # Chrome WebDriver uchun xizmatni sozlash
    service = ChromeService(ChromeDriverManager().install())

    # Chrome uchun maxsus sozlamalar
    options = Options()
    options.add_argument("--start-maximized")                 # Oynani maksimal o'lchamda ochish
    options.add_argument("--force-device-scale-factor=0.90")  # Masshtabni sozlash
    options.add_argument('--ignore-ssl-errors=yes')           # SSL xatoliklarni e'tiborsiz qoldirish
    options.add_argument('--ignore-certificate-errors')       # Sertifikat xatoliklarini e'tiborsiz qoldirish
    options.add_argument('--disable-gpu')                     # GPU bilan bog'liq xatoliklarni oldini olish
    options.add_argument('--no-sandbox')                      # Xavfsizlik rejimini o'chirish
    options.add_argument('--disable-dev-shm-usage')           # Xotira bilan bog'liq xatoliklarni oldini olish

    # GPU va WebGL bilan bog‘liq muammolarni oldini olish
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Chrome loglarini kamaytirish

    # **Performance logging'ni yoqish**
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    # Selenium WebDriver'ni ishga tushirish
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    yield driver
    driver.quit()
