import pytest
from apis.sector_api import SectorAPI

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(31)
def test_sector_save(save_data, load_data):
    api = SectorAPI(load_data, auth_profile="user")

    code = load_data("api/code")
    sector_code = f"sector_code-{code}"
    sector_name = f"sector_name-{code}"
    room_id = load_data("api/room_id")

    body = {
        "code": sector_code,
        "name": sector_name,
        "room_ids": [room_id],
        "state": "A"
    }

    resp, t_network, t_total = api.save_sector(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_name = data["name"]
    assert get_name == sector_name, f"{get_name} != {sector_name}"

    get_sector_id = data["sector_id"]
    save_data("api/sector_id", get_sector_id)
    save_data("api/sector_code", sector_code)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(32)
def test_sector_model(load_data):
    api = SectorAPI(load_data, auth_profile="user")

    sector_id = load_data("api/sector_id")
    sector_code = load_data("api/sector_code")

    body = {
        "sector_id": sector_id
    }

    resp, t_network, t_total = api.model_sector(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_code = data[2]["code"]
    assert get_code == sector_code, f"{get_code} != {sector_code}"

# ----------------------------------------------------------------------------------------------------------------------
