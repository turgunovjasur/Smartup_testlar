import random
import time
from autotest.anor.mdeal.order.order_view.order_view import OrderView
from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.sales_navbar import SalesNavbar
from autotest.trade.tdeal.order.order_list.orders_page import OrdersPage
from autotest.anor.mdeal.order.order_add.create_order_page import CreateOrderPage
from autotest.anor.mdeal.order.order_add.goods_page import GoodsPage
from autotest.anor.mdeal.order.order_add.final_page import FinalPage
from autotest.trade.tdeal.order.order_history_list.order_history_list import OrdersHistoryList
from utils.driver_setup import driver


def test_order_history(driver):
    # ------------------------------------------------------------------------------------------------------------------
    # Login_page
    # ------------------------------------------------------------------------------------------------------------------
    email, password = 'jasur@auto_test', '01062001'
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
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    dashboard_page.click_sales_button()
    # Sales_modal
    sales_navbar = SalesNavbar(driver)
    time.sleep(2)
    sales_navbar.element_visible()
    sales_navbar.click_orders_button()
    # Order_page
    orders_page = OrdersPage(driver)
    time.sleep(2)
    orders_page.element_visible()
    old_count_orders = orders_page.check_order()
    # print(f'old_count_orders: {old_count_orders}')
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    dashboard_page.click_sales_button()
    # Sales_modal
    sales_navbar = SalesNavbar(driver)
    time.sleep(2)
    sales_navbar.element_visible()
    sales_navbar.click_orders_archive_button()
    # ------------------------------------------------------------------------------------------------------------------
    # list
    # ------------------------------------------------------------------------------------------------------------------
    history_list = OrdersHistoryList(driver)
    time.sleep(2)
    history_list.element_visible()
    element = history_list.check_history()
    if element:
        print('There are no orders in the history list: we will create an order:')
        # ------------------------------------------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------------------------------------------
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
        number = random.randint(1, 10)
        # ------------------------------------------------------------------------------------------------------------------
        goods_page = GoodsPage(driver)
        time.sleep(2)
        goods_page.element_visible()
        goods_page.fill_form(number)
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
        # print(f"First count: {count_orders}")
        # print(f"New count: {new_count_orders}")

        try:
            assert new_count_orders == count_orders + 1, f"Error: expected number {count_orders + 1}, but the expected number {new_count_orders}"
            print("Order added:")
        except AssertionError as e:
            print(f"{str(e)}")
            raise

        orders_page.click_first_elem_button()
        orders_page.click_change_status_one_button()
        after_history_count_orders = orders_page.check_order()

        try:
            assert new_count_orders == after_history_count_orders, f"Error: expected number {after_history_count_orders}, but the expected number {new_count_orders}"
            print("Order status has been moved to archive:")
        except AssertionError as e:
            print(f"{str(e)}")
            raise

        dashboard_page.click_sales_button()
        # Sales_modal
        sales_navbar = SalesNavbar(driver)
        time.sleep(2)
        sales_navbar.element_visible()
        sales_navbar.click_orders_archive_button()

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    else:
        print('Yes found')

    history_list.click_first_elem_button()
    history_list.click_view_button()
    # ------------------------------------------------------------------------------------------------------------------
    # view
    # ------------------------------------------------------------------------------------------------------------------
    history_view = OrderView(driver)
    history_view.element_visible()
    order_id = history_view.get_elements()
    print(f'order_id: {order_id}')
    history_view.click_close_button()
    # ------------------------------------------------------------------------------------------------------------------
    # change_payment_type
    # ------------------------------------------------------------------------------------------------------------------
    history_list.click_first_elem_button()
    history_list.click_change_payment_type_button()
    # ------------------------------------------------------------------------------------------------------------------
    # change_subfilial
    # ------------------------------------------------------------------------------------------------------------------
    history_list.click_first_elem_button()
    history_list.click_change_subfilial_button()
    # ------------------------------------------------------------------------------------------------------------------
    # change_status_one
    # ------------------------------------------------------------------------------------------------------------------
    history_list.click_first_elem_button()
    old_count = history_list.check_order_history()
    # print(f'old_history_count: {old_count}')
    history_list.click_change_status_one_button()
    driver.refresh()

    new_count = history_list.check_order_history()
    # print(f'new_history_count: {new_count}')
    driver.refresh()

    try:
        assert old_count - 1 == new_count or None == element, f"Error: expected number {old_count - 1}, but got {old_count - 1 or element}"
        print(f"Quantity of orders in the archive: {old_count} ta\n After: {old_count - 1}")
    except AssertionError as e:
        print(f"{str(e)}")
        raise
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    dashboard_page.click_sales_button()
    # Sales_modal
    sales_navbar = SalesNavbar(driver)
    time.sleep(2)
    sales_navbar.element_visible()
    sales_navbar.click_orders_button()
    # Order_page
    orders_page = OrdersPage(driver)
    time.sleep(2)
    orders_page.element_visible()
    new_count_orders = orders_page.check_order()
    # print(f'new_count_orders: {new_count_orders}')

    try:
        assert old_count_orders == new_count_orders - 1, f"Error: expected number {old_count_orders}, but got {new_count_orders - 1}"
        print(f"Quantity orders: {old_count_orders} ta\n After: {new_count_orders}")
    except AssertionError as e:
        print(f"{str(e)}")
        raise
