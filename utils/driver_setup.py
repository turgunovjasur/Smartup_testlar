import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService


@pytest.fixture(params=["chrome"]) # , "firefox"
def driver(request):
    if request.param == "chrome":
        service = ChromeService(
            executable_path='C:\\Users\\jasur.turgunov\\Downloads\\chromedriver-win64 (1)\\chromedriver-win64\\chromedriver.exe')
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
    # elif request.param == "firefox":
    #     service = FirefoxService(
    #         executable_path='C:\\Users\\jasur.turgunov\\Downloads\\geckodriver-v0.34.0-win64\\geckodriver.exe')
    #     options = webdriver.FirefoxOptions()
    #     driver = webdriver.Firefox(service=service, options=options)

    driver.maximize_window()
    driver.get("https://smartup.online/")
    yield driver
    driver.quit()
