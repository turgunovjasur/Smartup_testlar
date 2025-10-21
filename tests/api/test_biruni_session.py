import pytest
from apis.biruni_session_api import BiruniSessionAPI

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(17)
def test_biruni_session(load_data, save_data):
    api = BiruniSessionAPI(load_data, auth_profile="admin")

    body = {}

    resp, t_network, t_total = api.biruni_session(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_project = data["projects"][0]
    get_administration_id = get_project["filials"][0][0]
    get_administration_name = get_project["filials"][0][1]

    api.logger.info(f"Administration ID: {get_administration_id}")
    api.logger.info(f"Administration NAME: {get_administration_name}")

    assert get_administration_name == "Администрирование", f"{get_administration_name} != 'Администрирование'"

    save_data("api/administration_id", get_administration_id)

# ----------------------------------------------------------------------------------------------------------------------
