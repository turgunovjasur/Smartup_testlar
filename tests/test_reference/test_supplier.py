from autotest.anor.mkw.supplier_add.supplier_add import SupplierAdd
from autotest.anor.mkw.supplier_list.supplier_list import SupplierList
from autotest.anor.mkw.supplier_product_list.supplier_product_list import SupplierProductList
from autotest.anor.mkw.supplier_view.supplier_view import SupplierView
from autotest.core.md.base_page import BasePage
from tests.test_base.test_base import login_user
from tests.conftest import driver, test_data


def test_add_supplier(driver, test_data):
    """Test adding supplier"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_add_supplier")

    # Test data
    data = test_data["data"]
    supplier_name = data['supplier_name']
    product_name = data['product_name']

    # Login
    login_user(driver, test_data, url='anor/mkw/supplier_list')

    # SupplierList
    supplier_list = SupplierList(driver)
    assert supplier_list.element_visible(), "SupplierList not open!"
    supplier_list.click_add_button()

    # SupplierAdd
    supplier_add = SupplierAdd(driver)
    assert supplier_add.element_visible(), "SupplierAdd not open!"
    supplier_add.input_persons(supplier_name)
    supplier_add.click_add_button()

    # SupplierList
    assert supplier_list.element_visible(), "SupplierList not open after save!"
    supplier_list.find_row(supplier_name)
    supplier_list.click_view_button()

    # SupplierView
    supplier_view = SupplierView(driver)
    assert supplier_view.element_visible(), "SupplierView not open!"
    get_supplier_name = supplier_view.check_supplier_name()
    assert get_supplier_name == supplier_name, f"{get_supplier_name} != {supplier_name}"
    supplier_view.click_close_button()

    # SupplierList
    assert supplier_list.element_visible(), "SupplierList not open after view!"
    supplier_list.find_row(supplier_name)
    supplier_list.click_bind_product_button()

    # SupplierProductList
    supplier_product_list = SupplierProductList(driver)
    assert supplier_product_list.element_visible(), "SupplierProductList not open!"
    supplier_product_list.click_detach_button()
    supplier_product_list.find_row(product_name)
    supplier_product_list.click_attach_one_button()

    supplier_product_list.click_attach_button()
    assert supplier_product_list.element_visible(), "SupplierProductList not open after bind product!"
    supplier_product_list.find_row(product_name)
    supplier_product_list.click_close_button()

    # SupplierList
    assert supplier_list.element_visible(), "SupplierList not open after bind product!"
    supplier_list.find_row(supplier_name)

    base_page.logger.info(f"✅Test end: test_add_supplier successfully!")