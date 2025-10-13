import pytest
from apis.natural_person_api import NaturalPersonAPI

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(9)
def test_natural_person_import(load_data):
    api = NaturalPersonAPI(load_data, auth_profile="admin")

    code = load_data("api/code")
    first_name = f"api_natural_person_first_name-{code}"

    body = {
      "natural_person": [
        {
          "first_name": first_name,
          "code": code,
          "is_budgetarian": "N",
          "state": "A",
          "groups": [
            {
              "group_code": "PRSGR:4",
              "type_code": ""
            }
          ]
        }
      ]
    }

    resp, t_network, t_total = api.import_natural_person(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_code = data["successes"][0]["code"]
    assert code == get_code, f"code: {code} != get_code: {get_code}"

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(10)
def test_natural_person_export(save_data, load_data):
    api = NaturalPersonAPI(load_data, auth_profile="admin")

    code = load_data("api/code")

    body = {
      "rooms": [
            {
              "room_code": ""
            }
          ],
      "code": code,
      "begin_created_on": "",
      "end_created_on": "",
      "begin_modified_on": "",
      "end_modified_on": ""
    }

    resp, t_network, t_total = api.export_natural_person(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_person_id = data["natural_person"][0]["person_id"]
    save_data("api/natural_person_id", get_person_id)

# ----------------------------------------------------------------------------------------------------------------------
