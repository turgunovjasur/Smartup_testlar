import pytest
from apis.inventory_api import InventoryAPI

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(33)
def test_inventory_save(save_data, load_data):
    api = InventoryAPI(load_data, auth_profile="user")

    code = load_data("api/code")
    name = f"api_product-{code}"
    product_code = f"api_product_code-{code}"
    sector_id = load_data("api/sector_id")

    body = {
      "name": name,
      "short_name": name,
      "measure_id": "19619",
      "box_type_id": "16354",
      "box_quant": "10",
      "barcodes": [],
      "breakage_id": [],
      "code": product_code,
      "comment_id": [],
      "files": [],
      "group_type_id": {},
      "gtins": [],
      "inventory_kinds": ["G"],
      "litr": "10",
      "marking_measures": [],
      "photos": [],
      "sector_id": [sector_id],
      "state": "A",
      "supplier_id": [],
      "weight_brutto": "100",
      "weight_netto": "80"
    }

    resp, t_network, t_total = api.save_inventory(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_name = data["name"]
    assert get_name == name, f"{get_name} != {name}"

    get_product_id = data["product_id"]
    save_data("api/product_id", get_product_id)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(34)
def test_inventory_model(save_data, load_data):
    api = InventoryAPI(load_data, auth_profile="user")

    product_id = load_data("api/product_id")

    body = {
        "product_id": product_id
    }

    resp, t_network, t_total = api.model_inventory(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    get_product_id = data[2]["product_id"]
    assert get_product_id == product_id, f"get_product_id: {get_product_id} != product_id: {product_id}"

# ----------------------------------------------------------------------------------------------------------------------
