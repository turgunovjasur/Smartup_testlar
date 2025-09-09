import time

import pytest
from autotest.anor.mr.product.inventory_add.inventory_new import InventoryNew
from flows.auth_flow import login_user
from tests.test_reference.flow_product import list_flow, add_flow, view_flow, set_price_flow, add_foto_flow


# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order(15)
def test_product_add_as_product_1(driver, test_data):
    """Test adding a product-1"""

    data = test_data["data"]
    product_name = data["product_name"]

    login_user(driver, test_data, url='anor/mr/product/inventory_list')

    list_flow(driver, add=True)

    add_flow(driver,
             product_name=product_name,
             sector_name=data["sector_name"],
             measurement_name=data["measurement_name"],
             goods_checkbox=True,
             weight_netto=data["product_weight_netto"],
             weight_brutto=data["product_weight_brutto"],
             litre=data["product_litre"])

    list_flow(driver, find_row=product_name, view=True)

    view_flow(driver, product_name=product_name)

    list_flow(driver, find_row=product_name, set_price=True)

    set_price_flow(driver,
                   product_name=product_name,
                   product_price=data["product_price"],
                   product_price_USA=data["product_price_USA"],
                   price_type_name_UZB=data["price_type_name_UZB"],
                   price_type_name_USA=data["price_type_name_USA"])

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order(58)
def test_product_add_as_product_2(driver, test_data):
    """Test adding a product-2"""

    data = test_data["data"]
    product_name = data["product_name_2"]

    login_user(driver, test_data, url='anor/mr/product/inventory_list')

    list_flow(driver, add=True)

    add_flow(driver,
             product_name=product_name,
             sector_name=data["sector_name"],
             measurement_name=data["measurement_name"],
             goods_checkbox=True,
             supplier_name=data["supplier_name"],
             weight_netto=data["product_weight_netto_2"],
             weight_brutto=data["product_weight_brutto_2"],
             litre=data["product_litre_2"])

    list_flow(driver, find_row=product_name, view=True)

    view_flow(driver, product_name=product_name)

    list_flow(driver, find_row=product_name, set_price=True)

    set_price_flow(driver,
                   product_name=product_name,
                   product_price=data["product_price"],
                   product_price_USA=data["product_price_USA"],
                   price_type_name_UZB=data["price_type_name_UZB"],
                   price_type_name_USA=data["price_type_name_USA"])

# ======================================================================================================================

def test_product_add_as_product_3(driver, test_data):
    """Test adding a product-3"""

    data = test_data["data"]
    product_name = data["product_name"]

    login_user(driver, test_data, url='anor/mr/product/inventory_list')

    list_flow(driver, add=True)

    add_foto_flow(driver, add_foto=True)

    add_flow(driver,
             product_name=product_name,
             sector_name=data["sector_name"],
             measurement_name=data["measurement_name"],
             goods_checkbox=True,
             weight_netto=data["product_weight_netto"],
             weight_brutto=data["product_weight_brutto"],
             litre=data["product_litre"])

    list_flow(driver, find_row=product_name, view=True)

    view_flow(driver, product_name=product_name)

    list_flow(driver, find_row=product_name, set_price=True)

    set_price_flow(driver,
                   product_name=product_name,
                   product_price=data["product_price"],
                   product_price_USA=data["product_price_USA"],
                   price_type_name_UZB=data["price_type_name_UZB"],
                   price_type_name_USA=data["price_type_name_USA"])


# ======================================================================================================================
