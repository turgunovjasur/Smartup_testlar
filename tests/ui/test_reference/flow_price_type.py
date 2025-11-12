from pages.anor.mkr.price_type_add.price_type_add import PriceTypeAdd
from pages.anor.mkr.price_type_list.price_type_list import PriceTypeList
from pages.anor.mkr.price_type_list_attach.price_type_list_attch import PriceTypeListAttach
from pages.anor.mkr.price_type_view.price_type_id import PriceTypeIdView

# ======================================================================================================================

def list_flow(driver, **kwargs):
    price_type_list = PriceTypeList(driver)
    price_type_list.element_visible()

    if kwargs.get("add"):
        price_type_list.click_add_button()

    find_row = kwargs.get("find_row")
    if find_row:
        price_type_list.find_row(find_row)

    if kwargs.get("view"):
        price_type_list.click_view_button()

    if kwargs.get("setting"):
        price_type_list.click_setting_button()

    if kwargs.get("add_dropdown"):
        price_type_list.click_add_dropdown_button()

# ======================================================================================================================

def list_attach(driver, **kwargs):
    price_type_list_attach = PriceTypeListAttach(driver)

    find_row = kwargs.get("find_row")
    if find_row:
        price_type_list_attach.find_rows(find_row)

# ======================================================================================================================

def add_flow(driver, **kwargs):
    price_type_add = PriceTypeAdd(driver)
    price_type_add.element_visible()

    price_type_name = kwargs.get("price_type_name")
    if price_type_name:
        price_type_add.input_name(price_type_name)

    room_name = kwargs.get("room_name")
    if room_name:
        price_type_add.input_rooms(room_name)

    currency_name = kwargs.get("currency_name")
    if currency_name:
        price_type_add.input_currency(currency_name)

    sub_filial_name = kwargs.get("sub_filial_name")
    if sub_filial_name:
        price_type_add.input_sub_filial(sub_filial_name)

    if kwargs.get("save", True):
        price_type_add.click_save_button()

# ======================================================================================================================

def view_flow(driver, **kwargs):
    price_type_view = PriceTypeIdView(driver)
    price_type_view.element_visible()

    price_type_name = kwargs.get("check_price_type")
    if price_type_name:
        text = price_type_view.get_elements()
        assert text == price_type_name, f'Expected "{price_type_name}", got "{text}"'

    if kwargs.get("close", True):
        price_type_view.click_close_button()

# ======================================================================================================================
