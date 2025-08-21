from autotest.biruni.kl.license_list.license_list import LicenseList
from autotest.biruni.kl.license_user_list.license_user_list import LicenseUserList

# ======================================================================================================================

def balance_flow(driver, **kwargs):
    _list = LicenseList(driver)
    _list.element_visible()

    navbar_name = kwargs.get("navbar_name")
    if navbar_name:
        _list.click_navbar_button(navbar_name)

# ======================================================================================================================

def document_flow(driver, **kwargs):
    _list = LicenseList(driver)
    _list.licence_and_document_visible()

    element_name = kwargs.get("element_name")
    data = kwargs.get("data")
    if element_name and data:
        _list.click_tbl_row_button(element_name, data)
        _list.click_attach_users_button(element_name, data)

# ======================================================================================================================

def purchase_flow(driver, **kwargs):
    _list = LicenseList(driver)
    _list.visible_buy_button()

    payer_name = kwargs.get("payer_name")
    if payer_name:
        _list.input_payers(payer_name)

    contract_name = kwargs.get("contract_name")
    if contract_name:
        _list.input_contract(contract_name)

    begin_date = kwargs.get("begin_date")
    if begin_date:
        _list.input_begin_date(begin_date)

    end_date = kwargs.get("end_date")
    if end_date:
        _list.input_end_date(end_date)

# ======================================================================================================================

def attach_user_flow(driver, **kwargs):
    _list = LicenseUserList(driver)
    _list.element_visible()

    find_row = kwargs.get("find_row")
    if _list.get_row_no_data():
        _list.click_detach_button()
        _list.find_row(find_row)
        _list.click_attach_button()
        _list.click_close_button()
        return

    _list.click_all_checkbox()
    _list.click_detach_checked_button()
    _list.click_detach_button()
    _list.find_row(find_row)
    _list.click_attach_button()
    _list.click_close_button()

# ======================================================================================================================