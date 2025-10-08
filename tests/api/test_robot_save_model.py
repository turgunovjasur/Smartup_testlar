import pytest
from apis.robot_api import RobotAPI
from conftest import save_data, load_data

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(7)
def test_robot_save(test_data, save_data, load_data):
    api = RobotAPI(load_data, auth_profile="admin")

    code = load_data("api/code")
    robot_code = f"api_robot_cod-{code}"
    robot_name = f"api_robot-{code}"
    room_id = load_data("api/room_id")

    body = {
      "code": robot_code,
      "name": robot_name,
      "state": "A",
      "tracking_enabled": "N",
      "role_ids": ["39650"],
      "room_ids": [room_id]
    }

    resp, t_network, t_total = api.import_robot(body)

    data = api.handle_response(resp, t_network, t_total)

    get_name = data["name"]
    assert robot_name == get_name, f"robot_name: {robot_name} != get_name: {get_name}"

    get_robot_id = data["robot_id"]
    save_data("api/robot_id", get_robot_id)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(8)
def test_robot_model(test_data, load_data):
    api = RobotAPI(load_data, auth_profile="admin")

    robot_id = load_data("api/robot_id")

    body = {
        "robot_id": robot_id
    }

    resp, t_network, t_total = api.export_robot(body)

    api.handle_response(resp, t_network, t_total)

# ----------------------------------------------------------------------------------------------------------------------
