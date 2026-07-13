from apis.currency_api import CurrencyAPI


def get_currency_id(load_data, currency_code):
    api = CurrencyAPI(load_data, auth_profile="admin")
    body = {
        "p": {
            "column": ["currency_id", "code", "name"],
            "filter": ["code", "=", str(currency_code)],
            "limit": 1,
            "offset": 0,
            "sort": []
        }
    }

    resp, t_network, t_total = api.list_currencies(body)
    data = api.handle_response(resp, t_network, t_total, body=body)
    rows = data.get("data") or []

    if not rows:
        raise AssertionError(f"Currency code topilmadi: {currency_code}")

    return rows[0][0]
