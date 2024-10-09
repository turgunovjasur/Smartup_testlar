import random
import time
import pytest
from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.sales_navbar import SalesNavbar
from autotest.trade.tdeal.order.order_list.orders_page import OrdersPage
from autotest.anor.mdeal.order.order_add.create_order_page import CreateOrderPage
from autotest.anor.mdeal.order.order_add.goods_page import GoodsPage
from autotest.anor.mdeal.order.order_add.final_page import FinalPage
from utils.driver_setup import driver


def run_test(driver, number_range):
    # ------------------------------------------------------------------------------------------------------------------
    # Login_page
    # ------------------------------------------------------------------------------------------------------------------
    email, password = 'admin@auto_test', 'greenwhite'
    # ------------------------------------------------------------------------------------------------------------------
    login_page = LoginPage(driver)
    login_page.fill_form(email, password)
    login_page.click_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Dashboard_page
    # ------------------------------------------------------------------------------------------------------------------
    dashboard_page = DashboardPage(driver)
    try:
        dashboard_page.element_visible_session()
        dashboard_page.click_button_delete_session()
    except:
        pass
    dashboard_page.element_visible()
    dashboard_page.click_hover_show_button()
    dashboard_page.click_sales_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Sales_modal
    # ------------------------------------------------------------------------------------------------------------------
    sales_navbar = SalesNavbar(driver)
    time.sleep(2)
    sales_navbar.element_visible()
    sales_navbar.click_orders_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Order_page
    # ------------------------------------------------------------------------------------------------------------------
    orders_page = OrdersPage(driver)
    time.sleep(2)
    orders_page.element_visible()
    count_orders = orders_page.check_order()
    orders_page.click_add_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Create_order_page
    # ------------------------------------------------------------------------------------------------------------------
    create_order_page = CreateOrderPage(driver)
    time.sleep(2)
    create_order_page.element_visible()
    create_order_page.fill_form()
    create_order_page.click_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Goods_page / Action / Overload
    # ------------------------------------------------------------------------------------------------------------------
    number = random.randint(*number_range)
    # ------------------------------------------------------------------------------------------------------------------
    goods_page = GoodsPage(driver)
    time.sleep(2)
    goods_page.element_visible()
    goods_page.fill_form(number)
    # ------------------------------------------------------------------------------------------------------------------
    # Overload
    # ------------------------------------------------------------------------------------------------------------------
    if number >= 10:
        goods_page.click_overload_button()
        goods_page.overload_is_visible()
    # ------------------------------------------------------------------------------------------------------------------
    # Action
    # ------------------------------------------------------------------------------------------------------------------
    if number >= 10:
        goods_page.click_action_button()
        goods_page.action_is_visible()
    # ------------------------------------------------------------------------------------------------------------------
    goods_page.click_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Final page
    # ------------------------------------------------------------------------------------------------------------------
    final_page = FinalPage(driver)
    time.sleep(2)
    final_page.fill_form()
    final_page.click_save_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Check count
    # ------------------------------------------------------------------------------------------------------------------
    orders_page = OrdersPage(driver)
    time.sleep(2)
    if orders_page.element_visible():
        driver.refresh()
    orders_page.element_visible()
    new_count_orders = orders_page.check_order()
    time.sleep(0.5)
    print(f"First count: {count_orders}")
    print(f"New count: {new_count_orders}")

    try:
        assert new_count_orders == count_orders + 1, f"Error: expected number {count_orders + 1}, but the expected number {new_count_orders}"
        print("Product successfully added")
    except AssertionError as e:
        print(f"{str(e)}")
        raise
# ------------------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("number_range", [(1, 9), (10, 20)])
def test_order(driver, number_range):
    print(f"Testing with numbers from {number_range[0]} to {number_range[1]}")
    run_test(driver, number_range)
# ------------------------------------------------------------------------------------------------------------------
