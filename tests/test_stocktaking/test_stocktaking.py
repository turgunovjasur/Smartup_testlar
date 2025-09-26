import random
import pytest
from autotest.anor.mkw.stocktaking.stocktaking_add import StocktakingAdd
from flows.auth_flow import login_user
from tests.test_stocktaking.stocktaking_flows import list_flow, add_flow, select_flow, add_product_flow, edit_flow, \
    view_flow, check_transaction_flow, complete_flow


@pytest.mark.regression
@pytest.mark.order(670)
def test_add_stocktaking(driver, test_data, load_data, save_data):
    """Test adding a stocktaking"""

    data = test_data["data"]

    # Login
    login_user(driver, test_data, url='anor/mkw/stocktaking/stocktaking_list')

    list_flow(driver, add=True)
    stocktaking_number = random.randint(100000, 999999)
    result = add_flow(driver,
                 stocktaking_number=stocktaking_number,
                 warehouse_name=data["warehouse_name"],
                 reason_name="Контрольная проверка",
                 note_name="TEST_TEXT",
                 get_data="Дата",
                 get_currency="Валюта")

    add = StocktakingAdd(driver)
    add.click_select_button()
    select_flow(driver, product_name=data["product_name"])
    add_product_flow(driver,
                     product_name=data["product_name_2"],
                     product_item_quant=10,
                     product_item_income_price=data["product_price"])

    list_flow(driver, find_row=stocktaking_number, edit=True)
    edit_flow(driver, stocktaking_number=stocktaking_number, warehouse_name=data["warehouse_name"])

    list_flow(driver, find_row=stocktaking_number, view=True)
    view_flow(driver,
              navbar_name="Основная информация",
              warehouse_name=data["warehouse_name"],
              sum_excess=data["product_price"] * 10,
              sum_minority=data["product_price"] * 5,
              data_creation=result["get_data"])

    list_flow(driver, find_row=stocktaking_number)
    check_transaction_flow(driver)

    list_flow(driver, complete=True)
    complete_flow(driver,
                  stocktaking_number=stocktaking_number,
                  data=result["get_data"],
                  warehouse_name=data["warehouse_name"],
                  sum_excess=data["product_price"] * 10,
                  sum_minority=data["product_price"] * 5)

    list_flow(driver, find_row=stocktaking_number, view=True)
    view_flow(driver, navbar_name="ТМЦ", search_name=data["product_name"], product_name=data["product_name"])

    list_flow(driver)
