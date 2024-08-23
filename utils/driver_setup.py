import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options


@pytest.fixture(params=["chrome"])
def driver(request):
    if request.param == "chrome":
        service = ChromeService(
            executable_path='C:\\Users\\jasur.turgunov\\Desktop\\ish\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')

        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--force-device-scale-factor=0.90")

        driver = webdriver.Chrome(service=service, options=options)
        driver.get("http://localhost:8080/smartup5x_trade_patch/")
        # driver.get("http://localhost:8080/smartup5x_trade/")
        # driver.get("https://smartup.online/")

        yield driver
        driver.quit()