import pytest
from apis.price_type_api import PriceTypeAPI

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(22)
def test_price_type_uzb_import(save_data, load_data):
    api = PriceTypeAPI(load_data, auth_profile="user")

    code = load_data("api/code")
    name = f"price_type_uzb-{code}"
    p_t_u_c = f"price_type_uzb_code-{code}"
    short_name = f"price_type_uzb_short_name-{code}"
    room_id = load_data("api/room_id")

    body = {
      "price_type": [
        {
          "name": name,
          "code": p_t_u_c,
          "with_card": "N",
          "short_name": short_name,
          "price_type_kind": "S",
          "room_ids": [room_id],
          "currency_code": "860",
          "state": "A"
        }
      ]
    }

    resp, t_network, t_total = api.import_price_type(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_code = data["successes"][0]["code"]
    assert p_t_u_c == get_code, f"price_type_uzb_code: {p_t_u_c} != get_code: {get_code}"

    save_data("api/price_type_uzb_code", get_code)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(23)
def test_price_type_uzb_export(save_data, load_data):
    api = PriceTypeAPI(load_data, auth_profile="user")

    price_type_uzb_code = load_data("api/price_type_uzb_code")

    body = {
        "column_list":["code", "name", "short_name", "with_card", "state", "price_type_kind", "currency_code"],
        "limit": "",
        "offset": ""
    }

    resp, t_network, t_total = api.export_price_type(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_price_type_code = data["data"][0]["code"]

    assert price_type_uzb_code == get_price_type_code, f"{price_type_uzb_code} != {get_price_type_code}"

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(24)
def test_price_type_list(save_data, load_data):
    api = PriceTypeAPI(load_data, auth_profile="user")

    body = {
      "p": {
        "column": [
          "code",
          "price_type_id"
        ],
        "filter": [
          "state",
          "=",
          "A"
        ],
        "limit": 50,
        "offset": 0,
        "sort": []
      }
    }

    resp, t_network, t_total = api.price_type_list(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_code = data["data"][0][0]
    price_type_uzb_code = load_data("api/price_type_uzb_code")
    assert price_type_uzb_code == price_type_uzb_code, f"{get_code} != {get_code}"

    get_price_type_id = data["data"][0][1]
    save_data("api/price_type_uzb_id", get_price_type_id)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(25)
def test_price_type_uzb_edit(save_data, load_data):
    api = PriceTypeAPI(load_data, auth_profile="user")

    code = load_data("api/code")
    name = f"price_type_uzb-{code}"
    price_type_uzb_code = load_data("api/price_type_uzb_code")
    short_name = f"price_type_uzb_short_name-{code}"
    price_type_uzb_id = load_data("api/price_type_uzb_id")
    room_id = load_data("api/room_id")

    body = {
          "name": name,
          "code": price_type_uzb_code,
          "with_card": "N",
          "short_name": short_name,
          "price_type_id": price_type_uzb_id,
          "price_type_kind": "S",
          "room_ids": [room_id],
          "currency_id": "12434",
          "state": "A"
        }

    resp, t_network, t_total = api.edit_price_type(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_price_type_id = data["price_type_id"]

    save_data("api/price_type_use_id", get_price_type_id)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(26)
def test_price_type_use_save(save_data, load_data):
    api = PriceTypeAPI(load_data, auth_profile="user")

    code = load_data("api/code")
    name = f"price_type_use-{code}"
    price_type_use_code = f"api/price_type_use_code-{code}"
    short_name = f"price_type_use_short_name-{code}"
    room_id = load_data("api/room_id")

    body = {
          "name": name,
          "code": price_type_use_code,
          "with_card": "N",
          "short_name": short_name,
          "price_type_kind": "S",
          "room_ids": [room_id],
          "currency_id": "12435",
          "state": "A"
        }

    resp, t_network, t_total = api.save_price_type(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_price_type_id = data["price_type_id"]

    save_data("api/price_type_use_id", get_price_type_id)

# ----------------------------------------------------------------------------------------------------------------------
