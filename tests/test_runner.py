import unittest
from HtmlTestRunner import HTMLTestRunner
from tests import test_registration

if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(test_registration)

    report_path = "../reports/test_report.html"
    with open(report_path, "w", encoding="utf-8") as report_file:
        runner = HTMLTestRunner(
            stream=report_file,
            title="Smartup",
            description="Test results for the registration process and product warehouse"
        )
        runner.run(test_suite)
