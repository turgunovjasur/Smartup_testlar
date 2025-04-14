import allure
import pytest
from tests.conftest import test_data
from utils.driver_setup import driver

from tests.test_reference.test_action import test_add_action
from tests.test_finance.test_currency import test_currency_add
from tests.test_reference.test_supplier import test_add_supplier
from tests.test_order.test_order_return import test_order_return
from tests.test_reference.test_product import test_product_add_as_product_1


from tests.test_finance.test_contract import (
    test_add_contract_for_client_A_UZB,
    test_add_contract_for_client_B_UZB,
    test_add_contract_for_client_C_USA
)
from tests.test_purchase.test_purchase import (
    test_add_purchase,
    test_add_extra_cost,
    test_add_purchase_with_extra_cost_sum
)
from tests.test_reference.test_client import (
    test_client_add_A,
    test_client_add_B,
    test_client_add_C
)
from tests.test_reference.test_legal_person import (
    test_add_legal_person_by_supplier,
    test_add_legal_person
)
from tests.test_reference.test_natural_person import (
    test_natural_person_add,
    test_natural_person_client_add_A,
    test_natural_person_client_add_B,
    test_natural_person_client_add_C
)
from tests.test_order.test_cashin import (
    test_cashin_add_A,
    test_offset_add_A,
    test_offset_add_B
)
from tests.test_order.test_order_for_action import (
    test_add_order_for_action,
    test_edit_order_for_action
)
from tests.test_order.test_order_edit import (
    test_edit_order_with_consignment,
    test_edit_order_for_price_type_USA
)
from tests.test_order.test_order_change_status import (
    test_change_status_from_draft_to_archive,
    test_change_status_draft_and_archive,
    test_change_status_draft_and_cancelled,
    test_change_status_draft_and_delivered
)
from tests.test_order.test_order_report import (
    test_check_report_for_order_list,
    test_check_report_for_order_history_list,
    test_add_template_for_order_invoice_report,
    test_check_invoice_report_for_order_list
)
from tests.test_order.test_life_cycle import (
    test_filial_create,
    test_room_add,
    test_robot_add,
    test_user_create,
    test_adding_permissions_to_user,
    test_user_change_password,
    test_payment_type_add,
    test_sector_add,
    test_room_attachment,
    test_init_balance,
    test_setting_consignment,
    test_sub_filial_add,
    test_price_type_add_UZB,
    test_price_type_add_USA,
    test_margin_add,
    test_setting_prepayment_on,
    test_setting_prepayment_off,
    test_check_price_tag,
    test_add_user_license
)
from tests.test_order.test_order import (
    test_order_add_for_sub_filial_select,
    test_add_order_with_consignment,
    test_add_order_with_contract,
    test_add_order_with_price_type_USA
)

# All ------------------------------------------------------------------------------------------------------------------

# pytest tests/test_runner.py::test_all -v --html=report.html --self-contained-html --alluredir=./allure-results
# allure serve ./allure-results
test_cases = [
        # {"name": "Add Legal Person", "func": test_add_legal_person},
        # {"name": "Filial Create",    "func": test_filial_create},
        # {"name": "Room Add",         "func": test_room_add},
        # {"name": "Robot Add",        "func": test_robot_add},
        # {"name": "Sub filial Add",   "func": test_sub_filial_add},

        # {"name": "Natural Person Add",   "func": test_natural_person_add},
        # {"name": "User Create",          "func": test_user_create},
        # {"name": "Adding Permissions",   "func": test_adding_permissions_to_user},
        # {"name": "Add User License",     "func": test_add_user_license},
        # {"name": "User Change Password", "func": test_user_change_password},
        #
        # {"name": "Price Type Add (UZB)", "func": test_price_type_add_UZB},
        # {"name": "Price Type Add (USA)", "func": test_price_type_add_USA},
        # {"name": "Payment Type Add",     "func": test_payment_type_add},
        # {"name": "Sector Add",           "func": test_sector_add},
        {"name": "Add Product-1",        "func": test_product_add_as_product_1},
        #
        # {"name": "Check Price Tag", "func": test_check_price_tag},
        # {"name": "Currency Add",    "func": test_currency_add},
        # {"name": "Margin Add",      "func": test_margin_add},
        #
        # {"name": "Natural Person Client Add-A", "func": test_natural_person_client_add_A},
        # {"name": "Natural Person Client Add-B", "func": test_natural_person_client_add_B},
        # {"name": "Natural Person Client Add-C", "func": test_natural_person_client_add_C},
        #
        # {"name": "Client Add-A", "func": test_client_add_A},
        # {"name": "Client Add-B", "func": test_client_add_B},
        # {"name": "Client Add-C", "func": test_client_add_C},
        #
        # {"name": "Room Attachment",     "func": test_room_attachment},
        # {"name": "Init Balance",        "func": test_init_balance},
        # {"name": "Setting Consignment", "func": test_setting_consignment},
        #
        # {"name": "Add Contract For Client UZB-A", "func": test_add_contract_for_client_A_UZB},
        # {"name": "Add Order With Consignment-A",  "func": test_add_order_with_consignment},
        # {"name": "Check Report For Order List-A", "func": test_check_report_for_order_list},
        # {"name": "Edit Order With Consignment-A", "func": test_edit_order_with_consignment},
        # {"name": "Change Status From Draft To Archive-A", "func": test_change_status_from_draft_to_archive},
        # {"name": "Check Report For Order History List-A", "func": test_check_report_for_order_history_list},
        # {"name": "Cashin Add-A", "func": test_cashin_add_A},
        # {"name": "Offset Add-A", "func": test_offset_add_A},
        #
        # {"name": "Add Contract For Client UZB-B",     "func": test_add_contract_for_client_B_UZB},
        # {"name": "Add Order With Contract-B",         "func": test_add_order_with_contract},
        # {"name": "Change Status Draft And Archive-B", "func": test_change_status_draft_and_archive},
        # {"name": "Offset Add-B",                      "func": test_offset_add_B},
        #
        # {"name": "Add Contract For Client USA-C",   "func": test_add_contract_for_client_C_USA},
        # {"name": "Add Order With Price Type-C",     "func": test_add_order_with_price_type_USA},
        # {"name": "Test Setting Prepayment On",      "func": test_setting_prepayment_on},
        # {"name": "Edit Order For Price Type USA-C", "func": test_edit_order_for_price_type_USA},
        # {"name": "Test Setting Prepayment Off",     "func": test_setting_prepayment_off},
        #
        {"name": "Add Template For Order Invoice Report", "func": test_add_template_for_order_invoice_report},
        # {"name": "Order Add For Sub Filial Select-C",     "func": test_order_add_for_sub_filial_select},
        # {"name": "Check Invoice Report For Order List-C", "func": test_check_invoice_report_for_order_list},
        # {"name": "Change Status Draft And Cancelled-C",   "func": test_change_status_draft_and_cancelled},
        #
        # {"name": "Add Action",                          "func": test_add_action},
        # {"name": "Add Order For Action-C",              "func": test_add_order_for_action},
        # {"name": "Edit Order For Action-C",             "func": test_edit_order_for_action},
        # {"name": "Change Status Draft And Delivered-C", "func": test_change_status_draft_and_delivered},
        # {"name": "Order Return",                        "func": test_order_return},
        #
        # # Purchase:
        {"name": "Add Legal Person By Supplier",     "func": test_add_legal_person_by_supplier},
        {"name": "Add Supplier",                     "func": test_add_supplier},
        {"name": "Add Purchase",                     "func": test_add_purchase},
        {"name": "Add Extra Cost",                   "func": test_add_extra_cost},
        {"name": "Add Purchase With Extra Cost Sum", "func": test_add_purchase_with_extra_cost_sum},
    ]

@pytest.mark.parametrize("test_case", test_cases)
def test_all(driver, test_data, save_data, load_data, test_case):
    with allure.step(test_case["name"]):
        try:
            func_name = test_case["func"].__name__

            if func_name == "test_add_purchase":
                test_case["func"](driver, test_data, save_data)
            elif func_name in ["test_add_extra_cost", "test_add_purchase_with_extra_cost"]:
                test_case["func"](driver, test_data, save_data, load_data)
            else:
                test_case["func"](driver, test_data)

            print(f"✅ {test_case['name']} passed.")

        except AssertionError as ae:
            allure.attach(
                body=str(ae),
                name=f"Assertion Error - {test_case['name']}",
                attachment_type=allure.attachment_type.TEXT
            )
            print(f"❌ {test_case['name']} failed with assertion error: {ae}")
            pytest.fail(f"Assertion failed: {test_case['name']}")

        except Exception as e:
            allure.attach(
                body=str(e),
                name=f"Error Log - {test_case['name']}",
                attachment_type=allure.attachment_type.TEXT
            )
            print(f"❌ {test_case['name']} failed with error: {e}")
            pytest.fail(f"Test failed: {test_case['name']}. Stopping execution.")

