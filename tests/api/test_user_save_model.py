import pytest
from apis.user_api import UserAPI
from utils.env_reader import get_env

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(11)
def test_user_add(save_data, load_data):
    api = UserAPI(load_data, auth_profile="admin")

    natural_person_id = load_data("api/natural_person_id")

    code = load_data("api/code")
    user_name = f"api_natural_person_user-{code}"
    login = f"api_test-{code}"
    password = get_env("PASSWORD_USER")

    robot_id = load_data("api/robot_id")

    body = {
      "user_id": natural_person_id,
      "name": user_name,
      "login": login,
      "code": code,
      "email": "",
      "gender": "",
      "password": password,
      "photo_sha": "",
      "robot_id": [robot_id],
      "role_id": [],
      "state": "A"
    }

    resp, t_network, t_total = api.user_add(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_name = data["name"]
    assert user_name == get_name, f"user_name: {user_name} != get_name: {get_name}"

    get_user_id = data["user_id"]
    save_data("api/user_id", get_user_id)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(12)
def test_user_view(load_data):
    api = UserAPI(load_data, auth_profile="admin")

    user_id = load_data("api/user_id")

    body = {
      "user_id": user_id
    }

    resp, t_network, t_total = api.user_view(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_person_id = data[2]["user_id"]
    assert user_id == get_person_id, f"user_id: {user_id} != get_person_id: {get_person_id}"

# ----------------------------------------------------------------------------------------------------------------------

def get_user_form_list(load_data, position=None):
    api = UserAPI(load_data, auth_profile="admin")

    user_id = load_data("api/user_id")

    body = {
      "d": {
        "user_id": user_id,
        "attached": "N",
        "position": position #  R, D, W, E
      },
      "p": {
        "column": [
          "form"
        ],
        "limit": 1000
      }
    }

    resp, t_network, t_total = api.user_form_list(body)

    return api.handle_response(resp, t_network, t_total, body=body)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(13)
def test_user_form_attach(load_data):
    api = UserAPI(load_data, auth_profile="admin")
    user_id = load_data("api/user_id")

    positions = [None, "R", "D", "W", "E"]

    for position in positions:

        api.logger.info(f"Processing position: {position}")

        data = get_user_form_list(load_data, position=position)
        form_list = [form[0] for form in data["data"]]

        body = {
            "form": form_list,
            "user_id": user_id
        }

        resp, t_network, t_total = api.user_form_attach(body)
        api.handle_response(resp, t_network, t_total, expect_status=200, body=body, allow_empty_response=True)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(22)
def test_user_change_password(load_data):
    api = UserAPI(load_data, auth_profile="user")

    password = get_env("PASSWORD_USER")

    body = {
        "current_password": password,
        "new_password": password,
        "rewritten_password": password
    }

    resp, t_network, t_total = api.user_change_password(body)
    api.handle_response(resp, t_network, t_total, expect_status=200, body=body, allow_empty_response=True)

# ----------------------------------------------------------------------------------------------------------------------
