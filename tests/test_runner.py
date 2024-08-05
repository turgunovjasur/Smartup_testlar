import unittest
from HtmlTestRunner import HTMLTestRunner
from tests import test_registration, test_login_negative, test_purchases

if __name__ == "__main__":
    test_suite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromModule(test_registration),
        unittest.TestLoader().loadTestsFromModule(test_login_negative),
        unittest.TestLoader().loadTestsFromModule(test_purchases)
    ])

    report_path = "../reports/test_report.html"
    with open(report_path, "w", encoding="utf-8") as report_file:
        runner = HTMLTestRunner(
            stream=report_file,
            report_title="Smartup",
            descriptions="Test results for registration, login, and purchases"
        )
        runner.run(test_suite)