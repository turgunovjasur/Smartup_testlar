import pytest
from apis.filial_api import FilialAPI

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(3)
def test_filial_save(load_data, save_data):
    api = FilialAPI(load_data, auth_profile="admin")

    legal_person_id = load_data("api/legal_person_id")

    code = load_data("api/code")
    filial_name = f"api_filial-{code}"

    body = {
        "filial_id": legal_person_id,
        "name": filial_name,
        "state": "A",
        "vat_enabled": "N",
        "base_currency_id": "12434",
        "excise_enabled": "N"
    }

    resp, t_network, t_total = api.import_filial(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_name = data["name"]
    assert filial_name == get_name, f"{filial_name} != {get_name}"

    get_filial_id = data["filial_id"]
    save_data("api/filial_id", get_filial_id)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(4)
def test_filial_model(load_data):
    api = FilialAPI(load_data, auth_profile="admin", filial_id=None)

    filial_id = load_data("api/filial_id")

    body = {
        "filial_id": filial_id
    }

    resp, t_network, t_total = api.export_filial(body)

    api.handle_response(resp, t_network, t_total, body=body)

# ----------------------------------------------------------------------------------------------------------------------
