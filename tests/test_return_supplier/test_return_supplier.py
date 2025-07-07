from autotest.anor.mkw.return_supplier.return_list.return_list import ReturnList
from flows.auth_flow import login_user


def test_return_to_supplier(driver, test_data):
    # Log
    data = test_data["data"]
    room_name = data["room_name"]

    login_user(driver, test_data, url='anor/mkw/return/return_list')

    # List
    return_list = ReturnList(driver)
    return_list.element_visible()
    return_list.click_add_button()
