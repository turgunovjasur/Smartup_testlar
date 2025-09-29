import time
from pages.anor.mr.product.inventory_add.inventory_new import InventoryNew
from pages.anor.mr.product.inventory_list.inventory_list import InventoryList
from pages.anor.mr.product.inventory_view.product_id import ProductId as ProductView
from pages.anor.mr.product.product_set_price.product_set_price import ProductSetPrice

# ======================================================================================================================

def add_foto_flow(driver, **kwargs):
    inventory_add = InventoryNew(driver)
    inventory_add.element_visible()

    if kwargs.get("add_foto"):
        inventory_add.input_upload_photo()

    if kwargs.get("close_modal"):
        inventory_add.click_close_modal_button()

# ======================================================================================================================

def list_flow(driver, **kwargs):
    inventory_list = InventoryList(driver)
    inventory_list.element_visible()

    if kwargs.get("add"):
        inventory_list.click_add_button()

    find_row = kwargs.get("find_row")
    if find_row:
        inventory_list.find_row(find_row)

    if kwargs.get("view"):
        inventory_list.click_view_button()

    if kwargs.get("set_price"):
        inventory_list.click_set_price_button()

# ======================================================================================================================

def add_flow(driver, **kwargs):
    inventory_add = InventoryNew(driver)
    inventory_add.element_visible()

    product_name = kwargs.get("product_name")
    if product_name:
        inventory_add.input_name(product_name)

    sector_name = kwargs.get("sector_name")
    if sector_name:
        inventory_add.input_sectors(sector_name)

    measurement_name = kwargs.get("measurement_name")
    if measurement_name:
        inventory_add.input_measurement(measurement_name)

    if kwargs.get("goods_checkbox"):
        inventory_add.click_goods_checkbox()

    supplier_name = kwargs.get("supplier_name")
    if supplier_name:
        inventory_add.input_suppliers(supplier_name)

    weight_netto = kwargs.get("weight_netto")
    if weight_netto:
        inventory_add.input_weight_netto(weight_netto)

    weight_brutto = kwargs.get("weight_brutto")
    if weight_brutto:
        inventory_add.input_weight_brutto(weight_brutto)

    litre = kwargs.get("litre")
    if litre:
        inventory_add.input_litre(litre)

    if kwargs.get("save", True):
        time.sleep(0.5)
        inventory_add.click_save_button()

# ======================================================================================================================

def view_flow(driver, **kwargs):
    product_view = ProductView(driver)
    product_view.element_visible()

    product_name = kwargs.get("product_name")
    if product_name:
        text = product_view.get_elements()
        assert text == product_name, f'Expected "{product_name}", got "{text}"'

    if kwargs.get("close", True):
        product_view.click_close_button()

# ======================================================================================================================

def set_price_flow(driver, **kwargs):
    product_set_price = ProductSetPrice(driver)
    product_set_price.element_visible()

    product_name = kwargs.get("product_name")
    product_price = kwargs.get("product_price")
    product_price_USA = kwargs.get("product_price_USA")
    price_type_name_UZB = kwargs.get("price_type_name_UZB")
    price_type_name_USA = kwargs.get("price_type_name_USA")

    if product_name:
        text = product_set_price.check_product()
        assert text == product_name, f'Expected "{product_name}", got "{text}"'
        product_set_price.input_prices(product_price, price_type_name_UZB)
        product_set_price.input_prices(product_price_USA, price_type_name_USA)

    if kwargs.get("save", True):
        product_set_price.click_save_button()

# ======================================================================================================================
