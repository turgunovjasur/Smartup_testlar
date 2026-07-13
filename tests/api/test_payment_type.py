import pytest
from apis.payment_type_api import PaymentTypeAPI

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(29)
def test_payment_type_attach(load_data, save_data):
    api = PaymentTypeAPI(load_data, auth_profile="user")
    payment_type_ids = _get_payment_type_ids(api)

    body = {
      "payment_type_id": payment_type_ids
    }

    resp, t_network, t_total = api.attach_payment_type(body)

    api.handle_response(resp, t_network, t_total, body=body, expect_status=200, allow_empty_response=True)
    save_data("api/payment_type_ids", payment_type_ids)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(30)
def test_payment_type_attach_to_room(load_data):
    api = PaymentTypeAPI(load_data, auth_profile="user")

    room_id = load_data("api/room_id")
    payment_type_ids = load_data("api/payment_type_ids")

    body = {
      "payment_type_id": payment_type_ids,
      "room_id": room_id
    }

    resp, t_network, t_total = api.attach_payment_type_to_room(body)

    api.handle_response(resp, t_network, t_total, body=body, expect_status=200, allow_empty_response=True)

# ----------------------------------------------------------------------------------------------------------------------

def _get_payment_type_ids(api):
    body = {
        "p": {
            "column": ["payment_type_id", "name"],
            "limit": 100,
            "offset": 0,
            "sort": []
        }
    }

    resp, t_network, t_total = api.list_attach_payment_types(body)
    data = api.handle_response(resp, t_network, t_total, body=body)
    rows = data.get("data") or []

    if not rows:
        raise AssertionError("Biriktirish uchun payment type topilmadi")

    return [row[0] for row in rows]

# ----------------------------------------------------------------------------------------------------------------------
