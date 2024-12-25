import time
from tests.test_base.test_base import get_driver
from tests.test_order.test_cashin import test_cashin_add_A, test_offset_add_A, test_offset_add_B

# Import all test functions
from tests.test_order.test_life_cycle import (
    test_legal_person_add,
    test_filial_creat,
    test_room_add,
    test_robot_add,
    test_natural_person_add,
    test_user_creat,
    test_adding_permissions_to_user,
    test_user_change_password,
    test_price_type_add,
    test_payment_type_add,
    test_sector_add,
    test_product_add,
    test_natural_person_client_add_A,
    test_natural_person_client_add_B,
    test_natural_person_client_add_C,
    test_client_add_A,
    test_client_add_B,
    test_client_add_C,
    test_room_attachment,
    test_init_balance,
    test_contract_add_A,
    test_contract_add_B,
    test_contract_add_C, test_setting_consignment,
)

from tests.test_order.test_order import (
    # Add
    test_order_add_A,
    test_order_add_B,
    test_order_add_C,

    # Edit
    test_order_edit_A,

    # Status
    test_order_change_status_A,
    test_order_change_status_B,
    test_order_change_status_C, test_order_copy_C_for_A_B
)
from utils.driver_setup import driver


# All ------------------------------------------------------------------------------------------------------------------

# pytest tests/test_order/test_runner.py::test_all -v --html=report.html --self-contained-html
# pytest tests/test_order/test_runner.py::test_all -v --html=report.html --self-contained-html --alluredir=./allure-results
# allure serve ./allure-results
def test_all():
    """All test runner"""
    tests = [
        # Base setup
        {"name": "Legal Person Add", "func": test_legal_person_add},
        {"name": "Filial Create", "func": test_filial_creat},
        {"name": "Room Add", "func": test_room_add},
        {"name": "Robot Add", "func": test_robot_add},

        # User management
        {"name": "Natural Person Add", "func": test_natural_person_add},
        {"name": "User Create", "func": test_user_creat},
        {"name": "Adding Permissions", "func": test_adding_permissions_to_user},
        {"name": "User Change Password", "func": test_user_change_password},

        # Product setup
        {"name": "Price Type Add", "func": test_price_type_add},
        {"name": "Payment Type Add", "func": test_payment_type_add},
        {"name": "Sector Add", "func": test_sector_add},
        {"name": "Product Add", "func": test_product_add},

        # Client setup
        {"name": "Natural Person Client Add-A", "func": test_natural_person_client_add_A},
        {"name": "Natural Person Client Add-B", "func": test_natural_person_client_add_B},
        {"name": "Natural Person Client Add-C", "func": test_natural_person_client_add_C},
        {"name": "Client Add-A", "func": test_client_add_A},
        {"name": "Client Add-B", "func": test_client_add_B},
        {"name": "Client Add-C", "func": test_client_add_C},

        # Attachment setup
        {"name": "Room Attachment", "func": test_room_attachment},
        {"name": "Init Balance", "func": test_init_balance},
        {"name": "Setting Consignment", "func": test_setting_consignment},

        # Test-A:
        # Contract -> Order(Add, Edit, Status) -> Cashin_Add -> Offset_Add
        {"name": "Contract Add-A", "func": test_contract_add_A},
        {"name": "Order Add-A", "func": test_order_add_A},
        {"name": "Order Edit-A", "func": test_order_edit_A},
        {"name": "Order Change Status-A", "func": test_order_change_status_A},
        {"name": "Cashin Add-A", "func": test_cashin_add_A},
        {"name": "Offset Add-A", "func": test_offset_add_A},

        # Test-B:
        # Contract -> Order(Add, Edit, Status) -> Offset_Add -> Check: Cashin_Add
        {"name": "Contract Add-B", "func": test_contract_add_B},
        {"name": "Order Add-B", "func": test_order_add_B},
        {"name": "Order Change Status-B", "func": test_order_change_status_B},
        {"name": "Offset Add-B", "func": test_offset_add_B},

        # Test-C:
        # {"name": "Contract Add-C", "func": test_contract_add_C},
        {"name": "Order Add-C", "func": test_order_add_C},
        {"name": "Order Copy-C for A,B", "func": test_order_copy_C_for_A_B},

    ]

    passed_tests = []
    failed_tests = []
    total_tests = len(tests)

    print("\n=== Test Execution Summary ===")

    for test in tests:
        try:
            driver = get_driver()
            if driver is None:
                raise Exception("WebDriver initialization failed")

            test['func'](driver)
            passed_tests.append(test['name'])
            print(f"✅ {test['name']}: PASSED")
            print("*" * 70)
            print("*" * 70)
        except Exception as e:
            failed_tests.append({"name": test['name'], "error": str(e)})
            print(f"❌ {test['name']}: FAILED")
            print("*" * 70)
            print("*" * 70)
        finally:
            if driver:
                driver.quit()
            time.sleep(1)

    print("\n=== Final Results ===")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {len(passed_tests)}")
    print(f"Failed: {len(failed_tests)}")

    if failed_tests:
        print("\nFailed Tests Details:")
        for test in failed_tests:
            print(f"❌ {test['name']}")
            print(f"   Error: {test['error']}\n")

    # Agar birorta test muvaffaqiyatsiz bo'lsa, pytest uchun xatolikni ko'rsatamiz
    assert len(failed_tests) == 0, "Some tests failed"
