# import pytest
# import allure
# from allure_commons.types import AttachmentType
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options
# from tests.test_reference.test_prices import test_prices
# from tests.test_reference.test_inventories import test_inventories
# from tests.test_reference.test_services import test_services
#
#
# def pytest_configure(config):
#     allure.environment(hostname="localhost", browser="chrome", environment="test")
#
#
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     rep = outcome.get_result()
#     if rep.when == "call" and rep.failed:
#         try:
#             driver = item.funcargs['driver']
#             allure.attach(
#                 driver.get_screenshot_as_png(),
#                 name="screenshot",
#                 attachment_type=AttachmentType.PNG
#             )
#         except Exception as e:
#             print(f"Skrinshot olishda xatolik yuz berdi: {e}")
#
# def run_tests():
#     pytest.main(["-v", "--alluredir=./allure-results",
#                  "tests/test_reference/test_prices.py",
#                  "tests/test_reference/test_inventories.py",
#                  "tests/test_reference/test_services.py"])
#
# if __name__ == "__main__":
#     run_tests()
#
#     print("Testlar yakunlandi. Allure hisobotini ko'rish uchun quyidagi buyruqni bajaring:")
#     print("allure serve ./allure-results")


import unittest
from HtmlTestRunner import HTMLTestRunner
from tests.test_reference.test_prices import test_prices
from tests.test_reference.test_inventories import test_inventories
from tests.test_reference.test_services import test_services
from utils.driver_setup import driver


if __name__ == "__main__":
    test_suite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromModule(test_prices),
        unittest.TestLoader().loadTestsFromModule(test_inventories),
        # unittest.TestLoader().loadTestsFromModule(test_services)
    ])

    report_path = "../reports/test_report.html"
    with open(report_path, "w", encoding="utf-8") as report_file:
        runner = HTMLTestRunner(
            stream=report_file,
            report_title="Smartup",
            descriptions="Automation test"
        )
        runner.run(test_suite)
