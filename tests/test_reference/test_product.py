import time

import pytest

from autotest.anor.mr.product.inventory_add.inventory_new import InventoryNew
from autotest.anor.mr.product.inventory_list.inventory_list import InventoryList
from autotest.anor.mr.product.product_set_price.product_set_price import ProductSetPrice
from autotest.anor.mr.product.inventory_view.product_id import ProductId as ProductView
from autotest.core.md.base_page import BasePage
from flows.auth_flow import login_user


def product_add(driver, test_data, product_name, supplier=False, weight_netto=None, weight_brutto=None, litre=None):
    """Test adding a product"""
    base_page = BasePage(driver)

    # Test data
    data = test_data["data"]
    measurement_name = data["measurement_name"]
    sector_name = data["sector_name"]
    product_price = data["product_price"]
    product_price_USA = data["product_price_USA"]
    price_type_name_UZB = data["price_type_name_UZB"]
    price_type_name_USA = data["price_type_name_USA"]
    supplier_name = data["supplier_name"]

    # Login
    login_user(driver, test_data, url='anor/mr/product/inventory_list')

    # Open Inventory List
    inventory_list = InventoryList(driver)
    inventory_list.element_visible()
    inventory_list.click_add_button()

    # Add Product (Inventory)
    inventory_add = InventoryNew(driver)
    inventory_add.element_visible()
    inventory_add.input_name(product_name)
    inventory_add.input_sectors(sector_name)
    inventory_add.input_measurement(measurement_name)
    inventory_add.click_goods_checkbox()
    if supplier:
        inventory_add.input_suppliers(supplier_name)
    if weight_netto is not None:
        inventory_add.input_weight_netto(weight_netto)
    if weight_brutto is not None:
        inventory_add.input_weight_brutto(weight_brutto)
    if litre is not None:
        inventory_add.input_litre(litre)
    time.sleep(1)
    inventory_add.click_save_button()

    # Checking error message
    error_code = inventory_add.error_massage()
    if error_code:
        base_page.logger.warning(f"⚠️ Xatolik aniqlandi!")
        assert error_code == data["error_massage_4"], f'Nomalum xatolik! -> "{error_code}"'
        base_page.refresh_page()
    else:
        base_page.logger.info("✅ Xatolik yoq! -> Product saqlandi.")

    # Verify in List
    assert inventory_list.element_visible(), "InventoryList not open after save!"
    inventory_list.find_and_click_checkbox(product_name)
    inventory_list.click_view_button()

    # Verify in View
    product_view = ProductView(driver)
    product_view.element_visible()
    text = product_view.get_elements()
    assert text == product_name, f'Expected "{product_name}", got "{text}"'
    product_view.click_close_button()

    # Set Price
    inventory_list.element_visible()
    inventory_list.find_and_click_checkbox(product_name)
    inventory_list.click_set_price_button()

    # Open Set Price Page
    product_set_price = ProductSetPrice(driver)
    product_set_price.element_visible()
    text = product_set_price.check_product()
    assert text == product_name, f'Expected "{product_name}", got "{text}"'
    product_set_price.input_prices(product_price, price_type_name_UZB)
    product_set_price.input_prices(product_price_USA, price_type_name_USA)
    product_set_price.click_save_button()


@pytest.mark.regression
@pytest.mark.order(15)
def test_product_add_as_product_1(driver, test_data):
    """Test adding a product-1"""

    # Test data
    data = test_data["data"]
    product_name = data["product_name"]
    brutto = data["product_weight_brutto"]
    netto = data["product_weight_netto"]
    litre = data["product_litre"]
    product_add(driver, test_data, product_name, weight_netto=netto, weight_brutto=brutto, litre=litre)

@pytest.mark.regression
@pytest.mark.order(58)
def test_product_add_as_product_2(driver, test_data):
    """Test adding a product-2"""

    # Test data
    data = test_data["data"]
    product_name = data["product_name_2"]
    brutto = data["product_weight_brutto_2"]
    netto = data["product_weight_netto_2"]
    litre = data["product_litre_2"]
    product_add(driver, test_data, product_name, supplier=True, weight_netto=netto, weight_brutto=brutto, litre=litre)