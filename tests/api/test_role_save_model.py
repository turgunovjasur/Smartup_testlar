import pytest
from apis.role_api import RoleAPI

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(14)
def test_role_edit(load_data):
    api = RoleAPI(load_data, auth_profile="admin")

    admin_id = load_data("api/admin_id")

    body = {
        "role_id": admin_id,
        "name": "Админ",
        "order_no": "",
        "state": "A",
        "pcode": "TRADE:12",
        "function_ids": [
            "1", "2", "3", "4", "5", "7", "8", "9", "10",
            "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
            "21", "22", "23", "24", "25", "26", "28", "101", "102"
        ]
    }

    resp, t_network, t_total = api.role_edit(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_role_id = data["role_id"]
    assert admin_id == get_role_id, f"admin_id: {admin_id} != get_role_id: {get_role_id}"

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(15)
def test_role_view(load_data):
    api = RoleAPI(load_data, auth_profile="admin")

    admin_id = load_data("api/admin_id")

    body = {
      "role_id": admin_id
    }

    resp, t_network, t_total = api.role_view(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_role_id = data[2]["role_id"]
    assert admin_id == get_role_id, f"admin_id: {admin_id} != get_role_id: {get_role_id}"

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(16)
def test_role_access_generate_all(load_data):
    api = RoleAPI(load_data, auth_profile="admin")

    admin_id = load_data("api/admin_id")

    body = {
      "generate": "Y",
      "role_id": admin_id
    }

    resp, t_network, t_total = api.access_generate_all(body)

    api.handle_response(resp, t_network, t_total, expect_status=200, body=body, allow_empty_response=True)

# ----------------------------------------------------------------------------------------------------------------------
