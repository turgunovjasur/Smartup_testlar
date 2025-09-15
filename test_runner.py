import inspect
import time

import allure
import pytest
from tests.test_cashin.test_cashin import test_cashin_add_A
from tests.test_finance.test_contract import (
    test_add_contract_for_client_A_UZB,
    test_add_contract_for_client_B_UZB,
    test_add_contract_for_client_C_USA,
)
from tests.test_finance.test_currency import test_currency_add
from tests.test_input.test_input import test_add_input, test_add_input_with_extra_cost
from tests.test_license.test_license import test_add_user_license, test_add_purchase_license
from tests.test_movement.test_movement import test_add_internal_movement
from tests.test_offset.test_offset import test_offset_add_A, test_offset_add_B
from tests.test_order.test_life_cycle import (
    test_adding_permissions_to_user,
    test_check_price_tag,
    test_filial_create,
    test_init_balance,
    test_margin_add,
    test_payment_type_add,
    test_price_type_add_USA,
    test_price_type_add_UZB,
    test_robot_add,
    test_room_add,
    test_room_attachment,
    test_sector_add,
    test_setting_consignment,
    test_setting_prepayment_off,
    test_setting_prepayment_on,
    test_sub_filial_add,
    test_user_change_password,
    test_user_create,
)
from tests.test_order.test_order import (
    test_add_order_for_action_demo,
    test_add_order_for_price_type_USA_demo,
    test_add_order_for_sub_filial_demo,
    test_add_order_with_consignment_demo,
    test_add_order_with_contract_demo,
)
from tests.test_order.test_order_change_status import (
    test_change_status_draft_and_archive_demo,
    test_change_status_draft_and_delivered_demo,
    test_change_status_new_and_cancelled_demo,
    test_order_change_status_from_draft_to_cancelled_demo,
)
from tests.test_order.test_order_edit import (
    test_edit_order_for_action_demo,
    test_edit_order_for_price_type_USA_demo,
    test_edit_order_with_consignment_demo,
)
from tests.test_order.test_order_list import test_copy_search_filter_in_order_list_demo
from tests.test_order.test_order_report import (
    test_add_template_for_order_invoice_report,
    test_check_invoice_report_for_order_list,
    test_check_report_for_order_history_list,
    test_check_report_for_order_list,
    test_sales_report_constructor_demo,
)
from tests.test_order.test_order_return import test_order_return
from tests.test_purchase.test_extra_cost import test_add_extra_cost
from tests.test_purchase.test_purchase import (
    test_add_purchase,
    test_add_purchase_with_extra_cost_quantity,
    test_add_purchase_with_extra_cost_sum,
    test_add_purchase_with_extra_cost_weight_brutto,
)
from tests.test_reference.test_action import (
    test_add_action_cash_money,
    test_add_action_terminal,
)
from tests.test_reference.test_client import (
    test_client_add_A,
    test_client_add_B,
    test_client_add_C,
)
from tests.test_reference.test_legal_person import (
    test_add_legal_person,
    test_add_legal_person_by_supplier,
)
from tests.test_reference.test_natural_person import (
    test_natural_person_add,
    test_natural_person_client_add_A,
    test_natural_person_client_add_B,
    test_natural_person_client_add_C,
)
from tests.test_reference.test_product import (
    test_product_add_as_product_1,
    test_product_add_as_product_2,
)
from tests.test_rep.integration.cislink.test_cislink import test_check_report_cis_link
from tests.test_rep.integration.integration_three.test_integration_three import (
    test_check_report_integration_three,
)
from tests.test_rep.integration.integration_two.test_integration_two import (
    test_check_report_integration_two,
)
from tests.test_rep.integration.optimum.test_optimum import test_check_report_optimum
from tests.test_rep.integration.saleswork.test_saleswork import (
    test_check_report_sales_work,
)
from tests.test_rep.integration.spot.test_spot import test_check_report_spot_2d
from tests.test_return_supplier.test_return_supplier import (
    test_add_purchase_to_supplier,
    test_return_to_supplier,
)
from tests.test_stocktaking.test_stocktaking import test_add_stocktaking
from tests.test_warehouse.test_supplier import test_add_supplier
from tests.test_warehouse.test_warehouse import test_add_warehouse
from tests.test_writeoff.test_writeoff import (
    test_add_write_off,
    test_check_constructor_report_write_off,
)
from utils.test_state import save_state, can_continue, CONFIG

# All ------------------------------------------------------------------------------------------------------------------

test_cases = [
    {"name": "Add Legal Person",                         "func": test_add_legal_person},
    {"name": "Filial Create",                            "func": test_filial_create},
    {"name": "Room Add",                                 "func": test_room_add},
    {"name": "Robot Add",                                "func": test_robot_add},
    {"name": "Sub filial Add",                           "func": test_sub_filial_add},
    {"name": "Natural Person Add",                       "func": test_natural_person_add},
    {"name": "User Create",                              "func": test_user_create},
    {"name": "Adding Permissions",                       "func": test_adding_permissions_to_user},
    {"name": "Add User License",                         "func": test_add_user_license},
    {"name": "Add Purchase License",                     "func": test_add_purchase_license},
    {"name": "User Change Password",                     "func": test_user_change_password},
    {"name": "Price Type Add (UZB)",                     "func": test_price_type_add_UZB},
    {"name": "Price Type Add (USA)",                     "func": test_price_type_add_USA},
    {"name": "Payment Type Add",                         "func": test_payment_type_add},
    {"name": "Sector Add",                               "func": test_sector_add},
    {"name": "Add Product-1",                            "func": test_product_add_as_product_1},
    {"name": "Check Price Tag",                          "func": test_check_price_tag},
    {"name": "Currency Add",                             "func": test_currency_add},
    {"name": "Margin Add",                               "func": test_margin_add},

    {"name": "Natural Person Client Add-A",              "func": test_natural_person_client_add_A},
    {"name": "Natural Person Client Add-B",              "func": test_natural_person_client_add_B},
    {"name": "Natural Person Client Add-C",              "func": test_natural_person_client_add_C},
    {"name": "Client Add-A",                             "func": test_client_add_A},
    {"name": "Client Add-B",                             "func": test_client_add_B},
    {"name": "Client Add-C",                             "func": test_client_add_C},

    {"name": "Room Attachment",                          "func": test_room_attachment},
    {"name": "Init Balance",                             "func": test_init_balance},

    # (Group-A) Order with Consignment:
    {"name": "(Group-A) Add Contract For Client UZB",           "func": test_add_contract_for_client_A_UZB},
    {"name": "(Group-A) Setting Consignment On",                "func": test_setting_consignment},
    {"name": "(Group-A) Add Order With Consignment",            "func": test_add_order_with_consignment_demo},
    {"name": "(Group-A) Check Report For Order List",           "func": test_check_report_for_order_list},
    {"name": "(Group-A) Edit Order With Consignment",           "func": test_edit_order_with_consignment_demo},
    {"name": "(Group-A) Copy Search Filter In Order List",      "func": test_copy_search_filter_in_order_list_demo},
    {"name": "(Group-A) Sales Report Constructor Demo",         "func": test_sales_report_constructor_demo},
    {"name": "(Group-A) Change Status From Draft To Cancelled", "func": test_order_change_status_from_draft_to_cancelled_demo},
    {"name": "(Group-A) Check Report For Order History List",   "func": test_check_report_for_order_history_list},
    {"name": "(Group-A) Cashin Add",                            "func": test_cashin_add_A},
    {"name": "(Group-A) Offset Add",                            "func": test_offset_add_A},

    # (Group-B) Order with Contract:
    {"name": "(Group-B) Add Contract For Client UZB-B",         "func": test_add_contract_for_client_B_UZB},
    {"name": "(Group-B) Add Order With Contract-B",             "func": test_add_order_with_contract_demo},
    {"name": "(Group-B) Change Status Draft And Archive-B",     "func": test_change_status_draft_and_archive_demo},
    {"name": "(Group-B) Offset Add-B",                          "func": test_offset_add_B},

    # (Group-C) Order with Price Type USA:
    {"name": "(Group-C) Add Contract For Client USA-C",    "func": test_add_contract_for_client_C_USA},
    {"name": "(Group-C) Add Order With Price Type-C",      "func": test_add_order_for_price_type_USA_demo},
    {"name": "(Group-C) Test Setting Prepayment On",       "func": test_setting_prepayment_on},
    {"name": "(Group-C) Edit Order For Price Type USA-C",  "func": test_edit_order_for_price_type_USA_demo},
    {"name": "(Group-C) Test Setting Prepayment Off",      "func": test_setting_prepayment_off},

    # Order with Sub Filial:
    {"name": "Add Template For Order Invoice Report",      "func": test_add_template_for_order_invoice_report},
    {"name": "Order Add For Sub Filial Select-C",          "func": test_add_order_for_sub_filial_demo},
    {"name": "Check Invoice Report For Order List-C",      "func": test_check_invoice_report_for_order_list},
    {"name": "Change Status Draft And Cancelled-C",        "func": test_change_status_new_and_cancelled_demo},

    # Order with Action:
    {"name": "Add Action Cash Money",                      "func": test_add_action_cash_money},
    {"name": "Add Action Terminal",                        "func": test_add_action_terminal},
    {"name": "Add Order For Action-C",                     "func": test_add_order_for_action_demo},
    {"name": "Edit Order For Action-C",                    "func": test_edit_order_for_action_demo},
    {"name": "Change Status Draft And Delivered-C",        "func": test_change_status_draft_and_delivered_demo},
    {"name": "Order Return",                               "func": test_order_return},

    # Purchase and Extra Cost:
    {"name": "Add Legal Person By Supplier",               "func": test_add_legal_person_by_supplier},
    {"name": "Add Supplier",                               "func": test_add_supplier},
    {"name": "Add Product-2",                              "func": test_product_add_as_product_2},
    {"name": "Add Purchase",                               "func": test_add_purchase},
    {"name": "Add Extra Cost",                             "func": test_add_extra_cost},
    {"name": "Add Purchase With Extra Cost Sum",           "func": test_add_purchase_with_extra_cost_sum},
    {"name": "Add Purchase With Extra Cost Quantity",      "func": test_add_purchase_with_extra_cost_quantity},
    {"name": "Add Purchase With Extra Cost Weight Brutto", "func": test_add_purchase_with_extra_cost_weight_brutto},

    # Input with Purchase
    {"name": "Add Input",                                  "func": test_add_input},
    {"name": "Add Input With Extra Cost",                  "func": test_add_input_with_extra_cost},

    # Return Supplier with Purchase
    {"name": "Add Purchase To Supplier",                   "func": test_add_purchase_to_supplier},
    {"name": "Add Return To Supplier",                     "func": test_return_to_supplier},

    # Internal Movement
    {"name": "Add Warehouse",                              "func": test_add_warehouse},
    {"name": "Add Internal Movement",                      "func": test_add_internal_movement},

    # Write Off
    {"name": "Add Write Off",                              "func": test_add_write_off},
    {"name": "Check Constructor Report Write Off",         "func": test_check_constructor_report_write_off},

    # Stocktaking
    {"name": "Add Stocktaking",                            "func": test_add_stocktaking},

    # Report:
    {"name": "Check Report CisLink",                       "func": test_check_report_cis_link},
    {"name": "Check Report Integration Three",             "func": test_check_report_integration_three},
    {"name": "Check Report Integration Two",               "func": test_check_report_integration_two},
    {"name": "Check Report Optimum",                       "func": test_check_report_optimum},
    {"name": "Check Report Sales Work",                    "func": test_check_report_sales_work},
    {"name": "Check Report Spot 2d",                       "func": test_check_report_spot_2d},
]

# ======================================================================================================================
# 3) TEST FUNKSIYASIGA KERAKLI PARAMETRLARNI TAYYORLASH
def _get_fixture_kwargs(func, request):
    """
    Har bir test funksiyasining parametrlarini to'playdi:
      1) Agar parametr fixture bo'lsa -> fixture'dan oladi
      2) Bo'lmasa test_data['data'] ichidan oladi
      3) Agar topilmasa va default qiymat bo'lsa -> uzatmaymiz
      4) Aks holda -> xato
    """
    sig = inspect.signature(func)
    kwargs = {}

    test_data = request.getfixturevalue("test_data")
    test_data_flat = test_data.get("data", {}) if isinstance(test_data, dict) else {}

    for param_name, param in sig.parameters.items():
        # *args / **kwargs bo‘lsa uzatmaymiz
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue

        # 1) Fixture sifatida olishga urinib ko‘ramiz
        try:
            kwargs[param_name] = request.getfixturevalue(param_name)
            continue
        except pytest.FixtureLookupError:
            pass

        # 2) test_data ichidan olish
        if param_name in test_data_flat:
            kwargs[param_name] = test_data_flat[param_name]
            continue

        # 3) Default qiymat bo‘lsa uzatmaymiz
        if param.default is not inspect._empty:
            continue

        # 4) Topilmasa xato
        raise Exception(f"❌ Parametr '{param_name}' topilmadi.")

    return kwargs


# ======================================================================
# 4) PYTEST PARAMETRIZATSIYA
@pytest.fixture
def runner_case(request):
    return request.param

def pytest_generate_tests(metafunc):
    if "runner_case" in metafunc.fixturenames:
        params = [pytest.param(case, id=case["name"]) for case in test_cases]
        metafunc.parametrize("runner_case", params)


# ======================================================================
# 5) ASOSIY RUNNER + RETRY (FACTORY BILAN)
def test_run_with_state(runner_case, request, driver_factory):
    func = runner_case["func"]
    allure.dynamic.title(runner_case["name"])

    if not can_continue():
        save_state(func.__name__, "skipped")
        allure.attach("Skipped because fail limit exceeded",
                      name="Skip Reason",
                      attachment_type=allure.attachment_type.TEXT)
        pytest.skip("❌ Fail limitdan oshdi. Keyingi testlar to‘xtatildi.")

    # Sizdagi helper orqali birinchi urinish uchun kwargs to'planadi (driver shu yerda fixture'dan keladi)
    kwargs = _get_fixture_kwargs(func, request)
    retry_count = CONFIG.get("retry_count", 0)

    for attempt in range(1, retry_count + 2):  # retry_count=1 -> 2 urinish
        try:
            with allure.step(f"Attempt {attempt}"):
                func(**kwargs)
                save_state(func.__name__, "passed", attempt=attempt)
                allure.attach(f"PASSED on attempt {attempt}",
                              name="Result",
                              attachment_type=allure.attachment_type.TEXT)
                return

        except Exception as e:
            # Urinish natijasini JSON + Allure ga yozamiz
            save_state(func.__name__, "failed", attempt=attempt, error=str(e))
            allure.attach(str(e),
                          name=f"Error on attempt {attempt}",
                          attachment_type=allure.attachment_type.TEXT)

            # 🧹 Eski driverni tozalaymiz (va kwargs'dan olib tashlaymiz!)
            old = kwargs.pop("driver", None)
            if old:
                try:
                    old.quit()
                    with allure.step(f"Attempt {attempt} - Driver closed"):
                        allure.attach("Driver quit successfully",
                                      name="Driver Cleanup",
                                      attachment_type=allure.attachment_type.TEXT)
                except Exception as qerr:
                    with allure.step(f"Attempt {attempt} - Driver close failed"):
                        allure.attach(str(qerr),
                                      name="Driver Quit Error",
                                      attachment_type=allure.attachment_type.TEXT)

            if attempt <= retry_count:
                # 🔁 MUHIM: fixture emas, FACTORY orqali YANGI driver ochamiz
                new_driver = driver_factory()
                kwargs["driver"] = new_driver

                with allure.step(f"Attempt {attempt} - New Driver Created"):
                    allure.attach(f"New driver session_id: {getattr(new_driver, 'session_id', 'n/a')}",
                                  name="Driver Re-init",
                                  attachment_type=allure.attachment_type.TEXT)

                # Yangi Chrome protsessi to'liq tayyor bo'lsin
                time.sleep(1)
                continue

            # Retry tugagan — yakuniy fail
            allure.attach(str(e), name="Final Failure",
                          attachment_type=allure.attachment_type.TEXT)
            raise


# def _get_fixture_kwargs(func, request):
#     """
#     Har bir test funksiyasining parametrlarini to'playdi:
#       1) Agar parametr fixture bo'lsa -> fixture'dan oladi
#       2) Bo'lmasa test_data['data'] ichidan nomi bilan oladi
#       3) Agar topilmasa va parametr DEFAULT qiymatga ega bo'lsa -> uzatmaymiz (funksiya o'zi defaultni oladi)
#       4) Agar parametr *args / **kwargs bo'lsa -> uzatmaymiz (Python o'zi boshqaradi)
#       5) Aks holda -> xato
#     """
#     sig = inspect.signature(func)
#     kwargs = {}
#
#     test_data = request.getfixturevalue("test_data")
#     test_data_flat = test_data.get("data", {}) if isinstance(test_data, dict) else {}
#
#     for param_name, param in sig.parameters.items():
#         # *args / **kwargs -> hech narsa uzatmaymiz
#         if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
#             continue
#
#         # 1) Fixture sifatida berishga urinamiz
#         try:
#             kwargs[param_name] = request.getfixturevalue(param_name)
#             continue
#         except pytest.FixtureLookupError:
#             pass
#
#         # 2) test_data['data'] ichidan olishga urinib ko'ramiz
#         if param_name in test_data_flat:
#             kwargs[param_name] = test_data_flat[param_name]
#             continue
#
#         # 3) Default qiymat bo'lsa, uzatmaymiz
#         if param.default is not inspect._empty:
#             continue
#
#         # 5) Topilmasa xato
#         raise Exception(
#             f"❌ Parametr '{param_name}' uchun fixture ham, test_data['data'] ichida ham topilmadi!"
#         )
#
#     return kwargs
#
#
# def _inherit_marks(func):
#     """
#     Original testdagi markerlarni (masalan, regression) olib, parametrga beramiz.
#     'order' markerini olib tashlaymiz — ro‘yxat tartibiga aralashmasin.
#     """
#     fmarks = getattr(func, "pytestmark", [])
#     if not isinstance(fmarks, (list, tuple)):
#         fmarks = [fmarks]
#     return [m for m in fmarks if getattr(m, "name", None) != "order"]
#
#
# def pytest_generate_tests(metafunc):
#     if "test_case" in metafunc.fixturenames:
#         params = []
#         for tc in test_cases:
#             marks = _inherit_marks(tc["func"])
#             params.append(pytest.param(tc, id=tc["name"], marks=marks))
#         metafunc.parametrize("test_case", params)
#
#
# @pytest.fixture(scope="function")
# def test_case():
#     # Parametrizatsiya bu fixture'ga qiymat beradi; bu yerda hech narsa qilmaymiz.
#     pass
#
#
# def test_run_from_runner(request, test_case):
#     """
#     Har bir element = alohida test.
#     Allure uchun sarlavha: ro‘yxatdagi 'name'.
#     """
#     allure.dynamic.title(test_case["name"])
#     func = test_case["func"]
#     kwargs = _get_fixture_kwargs(func, request)
#     func(**kwargs)
