import random
import pytest
from apis.legal_person_api import LegalPersonAPI
from conftest import save_data, load_data

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(1)
def test_legal_person_import(test_data, save_data, load_data):
    api = LegalPersonAPI(load_data, auth_profile="admin")

    code_int = random.randint(100000, 999999)
    code = str(code_int)

    body = {
        "legal_person": [{
            "person_id": "",
            "name": f"api_legal_person-{code}",
            "short_name": f"api_legal_person_short_name-{code}",
            "code": code,
            "state": "A",
            "is_budgetarian": "N",
            "is_client": "N",
            "is_supplier": "N"
        }]
    }

    resp, t_network, t_total = api.import_legal_person(body)
    save_data("api/code", code)

    data = api.handle_response(resp, t_network, t_total)

    get_code = data["successes"][0]["code"]
    assert code == get_code, f"code: {code} != get_code: {get_code}"

    save_data("api/legal_person_code", code)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(2)
def test_legal_person_export(test_data, save_data, load_data):
    api = LegalPersonAPI(load_data, auth_profile="admin")

    legal_person_code = load_data("api/legal_person_code")

    body = {
        "rooms": [
            {
              "room_code": ""
            }
          ],
        "filial_code": "",
        "code": legal_person_code,
        "state": "",
        "begin_created_on": "",
        "end_created_on": "",
        "begin_modified_on": "",
        "end_modified_on": ""
    }

    resp, t_network, t_total = api.export_legal_person(body)

    data = api.handle_response(resp, t_network, t_total)

    get_legal_person_code = data["legal_person"][0]["code"]
    assert legal_person_code == get_legal_person_code, \
        f"{legal_person_code} != {get_legal_person_code}"

    person_id = data["legal_person"][0]["person_id"]
    save_data("api/legal_person_id", person_id)

# ----------------------------------------------------------------------------------------------------------------------
