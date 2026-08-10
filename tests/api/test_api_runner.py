import json
import os

import allure
import pytest
from conftest import get_data_file_path
from tests.api.test_biruni_session import test_biruni_session as _test_biruni_session
from tests.api.test_filial_save_model import test_filial_save as _test_filial_save, test_filial_model as _test_filial_model
from tests.api.test_inventory import test_inventory_save as _test_inventory_save, test_inventory_model as _test_inventory_model
from tests.api.test_legal_person_import_export import (
    test_legal_person_import as _test_legal_person_import,
    test_legal_person_export as _test_legal_person_export,
)
from tests.api.test_natural_person_import_export import (
    test_natural_person_import as _test_natural_person_import,
    test_natural_person_export as _test_natural_person_export,
)
from tests.api.test_payment_type import (
    test_payment_type_attach as _test_payment_type_attach,
    test_payment_type_attach_to_room as _test_payment_type_attach_to_room,
)
from tests.api.test_price_tag_excel import test_price_tag_excel_download as _test_price_tag_excel_download
from tests.api.test_product_set_price import (
    test_product_set_price_save as _test_product_set_price_save,
    test_product_set_price_model as _test_product_set_price_model,
)
from tests.api.test_robot_save_model import test_robot_save as _test_robot_save, test_robot_model as _test_robot_model
from tests.api.test_role_save_model import (
    test_role_edit as _test_role_edit,
    test_role_view as _test_role_view,
    test_role_access_generate_all as _test_role_access_generate_all,
)
from tests.api.test_room_save_model import test_room_save as _test_room_save, test_room_model as _test_room_model
from tests.api.test_sector import test_sector_save as _test_sector_save, test_sector_model as _test_sector_model
from tests.api.test_user_save_model import (
    test_user_add as _test_user_add,
    test_user_view as _test_user_view,
    test_user_form_attach as _test_user_form_attach,
    test_user_change_password as _test_user_change_password,
)
from tests.api.test_user_license_attach import (
    test_get_purchase_info as _test_get_purchase_info,
    test_purchase_license as _test_purchase_license,
    test_user_license_list as _test_user_license_list,
    test_user_license_attach as _test_user_license_attach,
)
from tests.api.test_price_type import (
    test_price_type_uzb_import as _test_price_type_uzb_import,
    test_price_type_uzb_export as _test_price_type_uzb_export,
    test_price_type_list as _test_price_type_list,
    test_price_type_uzb_edit as _test_price_type_uzb_edit,
    test_price_type_use_save as _test_price_type_use_save,
    test_price_type_use_model as _test_price_type_use_model,
)


@pytest.fixture(scope="module", autouse=True)
def clear_api_state(request):
    """Runner yangi API flow boshlashi uchun oldingi run'dan qolgan api/* state'ni tozalaydi."""
    data_store_file = get_data_file_path(request)

    if not os.path.exists(data_store_file):
        return

    with open(data_store_file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    cleaned_data = {key: value for key, value in data.items() if not key.startswith("api/")}

    if cleaned_data != data:
        with open(data_store_file, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, indent=4, ensure_ascii=False)

# All ------------------------------------------------------------------------------------------------------------------

test_cases = [
    {"name": "Legal Person [IMPORT]", "func": _test_legal_person_import},
    {"name": "Legal Person [EXPORT]", "func": _test_legal_person_export},

    {"name": "Filial [SAVE]", "func": _test_filial_save},
    {"name": "Filial [MODEL]", "func": _test_filial_model},

    {"name": "Room [SAVE]", "func": _test_room_save},
    {"name": "Room [MODEL]", "func": _test_room_model},

    {"name": "Robot [SAVE]", "func": _test_robot_save},
    {"name": "Robot [MODEL]", "func": _test_robot_model},

    {"name": "Natural Person [IMPORT]", "func": _test_natural_person_import},
    {"name": "Natural Person [EXPORT]", "func": _test_natural_person_export},

    {"name": "User [SAVE]", "func": _test_user_add},
    {"name": "User [MODEL]", "func": _test_user_view},
    {"name": "User [ATTACH FORM]", "func": _test_user_form_attach},

    {"name": "Role [EDIT]", "func": _test_role_edit},
    {"name": "Role [MODEL]", "func": _test_role_view},
    {"name": "Role [ATTACH FORM]", "func": _test_role_access_generate_all},

    {"name": "Biruni Session [INFO]", "func": _test_biruni_session},

    {"name": "License Purchase [INFO]", "func": _test_get_purchase_info},
    {"name": "License [SAVE]", "func": _test_purchase_license},
    {"name": "License User [LIST]", "func": _test_user_license_list},
    {"name": "License [ATTACH USER]", "func": _test_user_license_attach},

    {"name": "User Change Password", "func": _test_user_change_password},

    {"name": "Price Type UZB [IMPORT]", "func": _test_price_type_uzb_import},
    {"name": "Price Type UZB [EXPORT]", "func": _test_price_type_uzb_export},
    {"name": "Price Type UZB [INFO]", "func": _test_price_type_list},
    {"name": "Price Type UZB [EDIT]", "func": _test_price_type_uzb_edit},
    {"name": "Price Type USE [SAVE]", "func": _test_price_type_use_save},
    {"name": "Price Type USE [MODEL]", "func": _test_price_type_use_model},

    {"name": "Price Type USE [ATTACH]", "func": _test_payment_type_attach},
    {"name": "Price Type USE [ATTACH]", "func": _test_payment_type_attach_to_room},

    {"name": "Sector [SAVE]", "func": _test_sector_save},
    {"name": "Sector [MODEL]", "func": _test_sector_model},

    {"name": "Inventory [SAVE]", "func": _test_inventory_save},
    {"name": "Inventory [MODEL]", "func": _test_inventory_model},

    {"name": "Product Set Price [SAVE]", "func": _test_product_set_price_save},
    {"name": "Product Set Price [MODEL]", "func": _test_product_set_price_model},

    {"name": "Price Tag Excel Download [LOAD]", "func": _test_price_tag_excel_download},
]

# ======================================================================================================================
# Pytest Configuration
# ======================================================================================================================

def pytest_generate_tests(metafunc):
    """Har bir test case uchun alohida parametrize qiladi"""
    if "runner_case" in metafunc.fixturenames:
        metafunc.parametrize(
            "runner_case",
            test_cases,
            ids=[case["name"] for case in test_cases]
        )

# ======================================================================================================================
# Main Test Runner
# ======================================================================================================================

def test_run_with_state(runner_case, request, save_data, load_data):
    """
    Har bir test case ni ishga tushiradi va kerakli fixturelarni avtomatik inject qiladi
    """
    func = runner_case["func"]
    allure.dynamic.title(runner_case["name"])

    kwargs = _get_fixture_kwargs(func, request, save_data, load_data)

    func(**kwargs)

# ======================================================================================================================
# Helper Functions
# ======================================================================================================================

def _get_fixture_kwargs(func, request, save_data, load_data):
    """Test funksiyasi uchun kerakli fixture larni to'playdi"""
    kwargs = {}
    param_names = func.__code__.co_varnames[:func.__code__.co_argcount]

    for name in param_names:
        if name == "save_data":
            kwargs[name] = save_data
        elif name == "load_data":
            kwargs[name] = load_data
        elif name in request.fixturenames:
            try:
                kwargs[name] = request.getfixturevalue(name)
            except Exception as e:
                print(f"Warning: Fixture '{name}' topilmadi: {e}")

    return kwargs

# ======================================================================================================================
