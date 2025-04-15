import time

import pytest
from autotest.anor.mr.product.inventory_add.inventory_new import InventoryNew
from autotest.anor.mr.product.inventory_list.inventory_list import InventoryList
from autotest.anor.mr.product.product_set_price.product_set_price import ProductSetPrice
from autotest.anor.mr.product.inventory_view.product_id import ProductId as ProductView
from autotest.core.md.base_page import BasePage
from tests.test_base.test_base import login_user
from utils.driver_setup import driver
from tests.conftest import test_data


def product_add(driver, test_data, product_name, supplier=False, weight_netto=None, weight_brutto=None, litre=None):
    """Test adding a product"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_product_add")

    # Test data
    data = test_data["data"]
    measurement_name = data["measurement_name"]
    sector_name = data["sector_name"]
    product_price = data["product_price"]
    product_price_USA = data["product_price_USA"]
    price_type_name_UZB = data["price_type_name_UZB"]
    price_type_name_USA = data["price_type_name_USA"]
    supplier_name = data["supplier_name"]

    try:
        # Login
        login_user(driver, test_data, url='anor/mr/product/inventory_list')

        # Open Inventory List
        inventory_list = InventoryList(driver)
        assert inventory_list.element_visible(), "InventoryList not open!"
        inventory_list.click_add_button()

        # Add Product (Inventory)
        inventory_add = InventoryNew(driver)
        assert inventory_add.element_visible(), "InventoryNew not open!"
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
        assert product_view.element_visible(), "ProductView not open!"
        text = product_view.get_elements()
        assert text == product_name, f'Expected "{product_name}", got "{text}"'
        product_view.click_close_button()

        # Set Price
        assert inventory_list.element_visible(), "InventoryList not open!"
        inventory_list.find_and_click_checkbox(product_name)
        inventory_list.click_set_price_button()

        # Open Set Price Page
        product_set_price = ProductSetPrice(driver)
        assert product_set_price.element_visible(), "ProductSetPrice not open!"
        text = product_set_price.check_product()
        assert text == product_name, f'Expected "{product_name}", got "{text}"'
        product_set_price.input_prices(product_price, price_type_name_UZB)
        product_set_price.input_prices(product_price_USA, price_type_name_USA)
        product_set_price.click_save_button()

        base_page.logger.info(f"✅ Test end: test_product_add")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_product_add_as_product_1(driver, test_data):
    """Test adding a product-1"""

    # Test data
    data = test_data["data"]
    product_name = data["product_name"]
    product_add(driver, test_data, product_name, weight_netto=1000, weight_brutto=1100, litre=100)


def test_product_add_as_product_2(driver, test_data):
    """Test adding a product-2"""

    # Test data
    data = test_data["data"]
    product_name = data["product_name_2"]
    product_add(driver, test_data, product_name, supplier=True, weight_netto=2000, weight_brutto=2100, litre=200)