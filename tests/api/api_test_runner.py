import allure

from tests.api.test_biruni_session import test_biruni_session
from tests.api.test_filial_save_model import test_filial_save, test_filial_model
from tests.api.test_legal_person_import_export import test_legal_person_import, test_legal_person_export
from tests.api.test_natural_person_import_export import test_natural_person_import, test_natural_person_export
from tests.api.test_robot_save_model import test_robot_save, test_robot_model
from tests.api.test_role_save_model import test_role_edit, test_role_view, test_role_access_generate_all
from tests.api.test_room_save_model import test_room_save, test_room_model
from tests.api.test_user_save_model import test_user_add, test_user_view, test_user_form_attach
from tests.api.test_user_license_attach import (
    test_get_purchase_info, test_purchase_license, test_user_license_list, test_user_license_attach)

# All ------------------------------------------------------------------------------------------------------------------

test_cases = [
    {"name": "Legal Person [IMPORT]", "func": test_legal_person_import},
    {"name": "Legal Person [EXPORT]", "func": test_legal_person_export},

    {"name": "Filial [SAVE]", "func": test_filial_save},
    {"name": "Filial [MODEL]", "func": test_filial_model},

    {"name": "Room [SAVE]", "func": test_room_save},
    {"name": "Room [MODEL]", "func": test_room_model},

    {"name": "Robot [SAVE]", "func": test_robot_save},
    {"name": "Robot [MODEL]", "func": test_robot_model},

    {"name": "Natural Person [IMPORT]", "func": test_natural_person_import},
    {"name": "Natural Person [EXPORT]", "func": test_natural_person_export},

    {"name": "User [SAVE]", "func": test_user_add},
    {"name": "User [MODEL]", "func": test_user_view},
    {"name": "User [ATTACH FORM]", "func": test_user_form_attach},

    {"name": "Role [SAVE]", "func": test_role_edit},
    {"name": "Role [MODEL]", "func": test_role_view},
    {"name": "Role [ATTACH FORM]", "func": test_role_access_generate_all},

    {"name": "Biruni Session [INFO]", "func": test_biruni_session},

    {"name": "License [INFO]", "func": test_get_purchase_info},
    {"name": "License [SAVE]", "func": test_purchase_license},
    {"name": "License [INFO]", "func": test_user_license_list},
    {"name": "License [ATTACH USER]", "func": test_user_license_attach},
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
