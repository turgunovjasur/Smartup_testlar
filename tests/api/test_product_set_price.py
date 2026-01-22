import pytest
from apis.product_set_price_api import ProductSetPriceAPI

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(35)
def test_product_set_price_save(load_data):
    api = ProductSetPriceAPI(load_data, auth_profile="user")

    product_id = load_data("api/product_id")
    price_type_uzb_id = load_data("api/price_type_uzb_id")
    price_type_use_id = load_data("api/price_type_use_id")

    body = {
        "product_id": product_id,
        "prices": [
            {
                "price_type_id": price_type_uzb_id,
                "card_id": "-1",
                "price": "12000"
            },
            {
                "price_type_id": price_type_use_id,
                "card_id": "-1",
                "price": "12"
            }
        ]
    }

    resp, t_network, t_total = api.save_product_set_price(body)

    api.handle_response(resp, t_network, t_total, body=body, expect_status=200, allow_empty_response=True)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(36)
def test_product_set_price_model(save_data, load_data):
    api = ProductSetPriceAPI(load_data, auth_profile="user")

    product_id = load_data("api/product_id")
    price_type_uzb_id = load_data("api/price_type_uzb_id")
    price_type_use_id = load_data("api/price_type_use_id")

    body = {
        "product_id": product_id
    }

    resp, t_network, t_total = api.model_product_set_price(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_product_id = data[2]["product_id"]
    assert get_product_id == product_id, f"get_product_id: {get_product_id} != product_id: {product_id}"

    prices = data[2]["prices"]

    # Kutilayotgan narxlar map'i
    expected_prices = {
        price_type_uzb_id: "12000",  # UZS narxi
        price_type_use_id: "12"      # USD narxi
    }
    # Har bir price type uchun tekshirish
    for price_item in prices:
        price_id = price_item[0]  # price ID
        price_value = price_item[5]  # price value

        if price_id in expected_prices:
            expected_value = expected_prices[price_id]
            assert price_value == expected_value, \
                f"Price ID {price_id} uchun narx noto'g'ri: kutilgan {expected_value}, lekin {price_value} keldi"


        if price_id in expected_prices:
            assert price_value == expected_prices[price_id], \
                f"Price ID {price_id} uchun narx noto'g'ri: kutilgan {expected_prices[price_id]}, lekin {price_value} keldi"

# ----------------------------------------------------------------------------------------------------------------------
