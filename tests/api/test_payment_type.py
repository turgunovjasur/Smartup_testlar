import pytest
from apis.payment_type_api import PaymentTypeAPI

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(29)
def test_payment_type_attach(load_data):
    api = PaymentTypeAPI(load_data, auth_profile="user")

    body = {
      "payment_type_id": ["10645", "10647", "10646", "10648"]
    }

    resp, t_network, t_total = api.attach_payment_type(body)

    api.handle_response(resp, t_network, t_total, body=body, expect_status=200, allow_empty_response=True)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(30)
def test_payment_type_attach_to_room(load_data):
    api = PaymentTypeAPI(load_data, auth_profile="user")

    room_id = load_data("api/room_id")

    body = {
      "payment_type_id": ["10645", "10647", "10646", "10648"],
      "room_id": room_id
    }

    resp, t_network, t_total = api.attach_payment_type_to_room(body)

    api.handle_response(resp, t_network, t_total, body=body, expect_status=200, allow_empty_response=True)

# ----------------------------------------------------------------------------------------------------------------------
