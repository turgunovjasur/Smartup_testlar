import pytest
from apis.room_api import RoomAPI

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(5)
def test_room_save(test_data, load_data, save_data):
    api = RoomAPI(load_data, auth_profile="admin")

    code = load_data("api/code")
    room_name = f"api_room-{code}"

    body = {
      "code": code,
      "name": room_name,
      "room_kind": "D",
      "state": "A"
    }

    resp, t_network, t_total = api.import_room(body)

    data = api.handle_response(resp, t_network, t_total)

    get_name = data["name"]
    assert room_name == get_name, f"room_name: {room_name} != get_name: {get_name}"

    room_id = data["room_id"]
    save_data("api/room_id", room_id)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(6)
def test_room_model(test_data, load_data):
    api = RoomAPI(load_data, auth_profile="admin")

    room_id = load_data("api/room_id")

    body = {
        "room_id": room_id
    }

    resp, t_network, t_total = api.export_room(body)

    data = api.handle_response(resp, t_network, t_total)

    get_room_id = data[2]["room_id"]
    assert room_id == get_room_id, f"room_id: {room_id} != get_room_id: {get_room_id}"

# ----------------------------------------------------------------------------------------------------------------------
