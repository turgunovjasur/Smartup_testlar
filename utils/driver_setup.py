import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService


@pytest.fixture(params=["chrome"])
def driver(request):
    if request.param == "chrome":
        service = ChromeService(
            executable_path='C:\\Users\\jasur.turgunov\\Downloads\\chromedriver-win64 (1)\\chromedriver-win64\\chromedriver.exe')
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.get("https://smartup.online/")
    yield driver
    driver.quit()