from autotest.anor.mkw.supplier_add.supplier_add import SupplierAdd
from autotest.anor.mkw.supplier_list.supplier_list import SupplierList
from autotest.anor.mkw.supplier_product_list.supplier_product_list import SupplierProductList
from autotest.anor.mkw.supplier_view.supplier_view import SupplierView
from flows.auth_flow import login_user


def test_add_supplier(driver, test_data):
    """Test adding supplier"""

    # Test data
    data = test_data["data"]
    supplier_name = data['supplier_name']
    product_name = data['product_name']

    # Login
    login_user(driver, test_data, url='anor/mkw/supplier_list')

    # SupplierList
    supplier_list = SupplierList(driver)
    supplier_list.element_visible()
    supplier_list.click_add_button()

    # SupplierAdd
    supplier_add = SupplierAdd(driver)
    supplier_add.element_visible()
    supplier_add.input_persons(supplier_name)
    supplier_add.click_add_button()

    # SupplierList
    supplier_list.element_visible()
    supplier_list.find_row(supplier_name)
    supplier_list.click_view_button()

    # SupplierView
    supplier_view = SupplierView(driver)
    supplier_view.element_visible()
    get_supplier_name = supplier_view.check_supplier_name()
    assert get_supplier_name == supplier_name, f"{get_supplier_name} != {supplier_name}"
    supplier_view.click_close_button()

    # SupplierList
    supplier_list.element_visible()
    supplier_list.find_row(supplier_name)
    supplier_list.click_bind_product_button()

    # SupplierProductList
    supplier_product_list = SupplierProductList(driver)
    supplier_product_list.element_visible()
    supplier_product_list.click_detach_button()
    supplier_product_list.find_row(product_name)
    supplier_product_list.click_attach_one_button()

    supplier_product_list.click_attach_button()
    supplier_product_list.element_visible()
    supplier_product_list.find_row(product_name)
    supplier_product_list.click_close_button()

    # SupplierList
    supplier_list.element_visible()
    supplier_list.find_row(supplier_name)