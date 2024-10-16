import unittest
from HtmlTestRunner import HTMLTestRunner

from tests.test_sales.test_login_negative import test_login

from tests.test_reference.test_inventories import test_inventories
from tests.test_reference.test_prices import test_prices
from tests.test_reference.test_services import test_services

from tests.test_reference.test_action import test_actions
from tests.test_reference.test_overload import test_overload

from tests.tests_warehouse.test_internal_movements import test_internal_movements
from tests.tests_warehouse.test_inventory_receipts import test_inventory_receipts
from tests.tests_warehouse.test_purchases import test_purchase

from tests.test_sales.test_order import test_order
from tests.test_sales.test_order_history import test_order_history

from utils.driver_setup import driver


if __name__ == "__main__":
    test_suite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromModule(test_login),

        unittest.TestLoader().loadTestsFromModule(test_prices),
        unittest.TestLoader().loadTestsFromModule(test_inventories),
        unittest.TestLoader().loadTestsFromModule(test_services),
        unittest.TestLoader().loadTestsFromModule(test_actions),
        unittest.TestLoader().loadTestsFromModule(test_overload),

        unittest.TestLoader().loadTestsFromModule(test_inventory_receipts),
        unittest.TestLoader().loadTestsFromModule(test_internal_movements),
        unittest.TestLoader().loadTestsFromModule(test_purchase),

        unittest.TestLoader().loadTestsFromModule(test_order),
        unittest.TestLoader().loadTestsFromModule(test_order_history)

    ])

    report_path = "../reports/test_report.html"
    with open(report_path, "w", encoding="utf-8") as report_file:
        runner = HTMLTestRunner(
            stream=report_file,
            report_title="Smartup",
            descriptions="Automation test"
        )
        runner.run(test_suite)
