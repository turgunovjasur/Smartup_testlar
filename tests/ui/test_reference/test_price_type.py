import pytest
from flows.auth_flow import login_user
from pages.anor.mkr.price_editable.price_editable import PriceEditable
from tests.ui.test_reference.flow_price_type import list_flow, list_attach, add_flow, view_flow

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.regression
@pytest.mark.order(110)
def test_price_type_add_UZB(driver, test_data):
    """Test adding a UZB price type"""

    data = test_data["data"]
    price_type_name = data["price_type_name_UZB"]

    login_user(driver, test_data, url='anor/mkr/price_type_list')

    list_flow(driver, add=True)

    add_flow(driver,
             price_type_name=price_type_name,
             room_name=data["room_name"],
             currency_name="Узбекский сум")

    list_flow(driver, find_row=price_type_name, view=True)

    view_flow(driver, check_price_type=price_type_name)

    # Attach additional price types
    list_flow(driver, add_dropdown=True)

    # Attach price types
    list_attach(driver, find_row='Промо')
    list_flow(driver, add_dropdown=True)

    list_attach(driver, find_row='Акция')
    list_flow(driver, add_dropdown=True)

    list_attach(driver, find_row='Возврат')
    list_flow(driver, add_dropdown=True)

    list_attach(driver, find_row='Передача забаланс')
    list_flow(driver, add_dropdown=True)

    list_attach(driver, find_row='Обмен')
    list_flow(driver, find_row=price_type_name)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.regression
@pytest.mark.order(120)
def test_price_type_add_USA(driver, test_data):
    """Test adding a USA price type"""

    data = test_data["data"]
    price_type_name = data["price_type_name_USA"]

    login_user(driver, test_data, url='anor/mkr/price_type_list')

    list_flow(driver, add=True)

    add_flow(driver,
             price_type_name=price_type_name,
             room_name=data["room_name"],
             currency_name="Доллар США",
             sub_filial_name=data["sub_filial_name"])

    list_flow(driver, find_row=price_type_name, view=True)

    view_flow(driver, check_price_type=price_type_name)

    list_flow(driver)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.regression
@pytest.mark.order_group_C
@pytest.mark.order(435)
def test_price_type_setting(driver, test_data):
    """Test try a UZB price type limit"""

    data = test_data["data"]
    price_type_name = data["price_type_name_UZB"]

    login_user(driver, test_data, url='anor/mkr/price_type_list')

    list_flow(driver, find_row=price_type_name, setting=True)

    price_editable = PriceEditable(driver)
    price_editable.element_visible()
    price_editable.input_min_amount(amount=100_000)
    price_editable.click_save_button()

    list_flow(driver)

# ----------------------------------------------------------------------------------------------------------------------
