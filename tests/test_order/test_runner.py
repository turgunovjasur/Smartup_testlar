import allure
import pytest
from tests.test_base.test_base import get_driver
from tests.test_order.test_cashin import test_cashin_add_A, test_offset_add_A, test_offset_add_B
from utils.driver_setup import driver

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
    test_setting_consignment,
    test_sub_filial_add,
    test_price_type_add_UZB,
    test_price_type_add_USA,
    test_currency_add,
    test_margin_add,
    test_contract_add_A_UZB,
    test_contract_add_B_UZB,
    test_contract_add_C_USA,
)

from tests.test_order.test_order import (
    # Add
    test_order_add_with_consignment,
    test_order_add_client_B_check_contract,
    test_order_add_price_type_USA,

    # Edit
    test_order_edit_A,

    # Status
    test_order_change_status_A,
    test_order_change_status_B,
    test_order_change_status_C,
    test_order_copy_C_for_A_B,
    test_order_return
)


# All ------------------------------------------------------------------------------------------------------------------

# pytest tests/test_order/test_runner.py::test_all -v --html=report.html --self-contained-html
# pytest tests/test_order/test_runner.py::test_all -v --html=report.html --self-contained-html --alluredir=./allure-results
# allure serve ./allure-results
def get_tests():
    """All test runner"""
    return [
        {"name": "Legal Person Add", "func": test_legal_person_add},
        {"name": "Filial Create", "func": test_filial_creat},
        {"name": "Room Add", "func": test_room_add},
        {"name": "Robot Add", "func": test_robot_add},
        {"name": "Sub filial Add", "func": test_sub_filial_add},

        {"name": "Natural Person Add", "func": test_natural_person_add},
        {"name": "User Create", "func": test_user_creat},
        {"name": "Adding Permissions", "func": test_adding_permissions_to_user},
        {"name": "User Change Password", "func": test_user_change_password},

        {"name": "Price Type Add", "func": test_price_type_add_UZB},
        {"name": "Price Type Add", "func": test_price_type_add_USA},
        {"name": "Payment Type Add", "func": test_payment_type_add},
        {"name": "Sector Add", "func": test_sector_add},
        {"name": "Product Add", "func": test_product_add},
        {"name": "Currency Add", "func": test_currency_add},
        {"name": "Margin Add", "func": test_margin_add},

        {"name": "Natural Person Client Add-A", "func": test_natural_person_client_add_A},
        {"name": "Natural Person Client Add-B", "func": test_natural_person_client_add_B},
        {"name": "Natural Person Client Add-C", "func": test_natural_person_client_add_C},
        {"name": "Client Add-A", "func": test_client_add_A},
        {"name": "Client Add-B", "func": test_client_add_B},
        {"name": "Client Add-C", "func": test_client_add_C},

        {"name": "Room Attachment", "func": test_room_attachment},
        {"name": "Init Balance", "func": test_init_balance},
        {"name": "Setting Consignment", "func": test_setting_consignment},

        {"name": "Contract Add-A", "func": test_contract_add_A_UZB},
        {"name": "Order Add-A", "func": test_order_add_with_consignment},
        {"name": "Order Edit-A", "func": test_order_edit_A},
        {"name": "Order Change Status-A", "func": test_order_change_status_A},
        {"name": "Cashin Add-A", "func": test_cashin_add_A},
        {"name": "Offset Add-A", "func": test_offset_add_A},

        {"name": "Contract Add-B", "func": test_contract_add_B_UZB},
        {"name": "Order Add-B", "func": test_order_add_client_B_check_contract},
        {"name": "Order Change Status-B", "func": test_order_change_status_B},
        {"name": "Offset Add-B", "func": test_offset_add_B},

        {"name": "Contract Add-C", "func": test_contract_add_C_USA},
        {"name": "Order Add-C", "func": test_order_add_price_type_USA},
        # # {"name": "Order Copy-C for A,B", "func": test_order_copy_C_for_A_B},
        # # {"name": "Order Return", "func": test_order_return},
    ]


@pytest.mark.parametrize("test", get_tests())
def test_all(test):
    with allure.step(test["name"]):
        driver = get_driver()
        try:
            test["func"](driver)
            print(f"✅ {test['name']} passed.")
        except Exception as e:
            allure.attach(
                body=str(e),
                name="Error Log",
                attachment_type=allure.attachment_type.TEXT
            )
            print(f"❌ {test['name']} failed with error: {e}")
            pytest.fail(f"Test failed: {test['name']}. Stopping execution.")
        finally:
            driver.quit()
