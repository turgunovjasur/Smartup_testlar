import random
import time
from autotest.anor.mdeal.order.order_view.order_view import OrderView
from autotest.core.md.base_page import BasePage
from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.sales_navbar import SalesNavbar
from autotest.trade.tdeal.order.order_cancelled_list.order_cancelled_list import OrderCancelledList
from autotest.trade.tdeal.order.order_list.orders_page import OrdersPage
from autotest.anor.mdeal.order.order_add.create_order_page import CreateOrderPage
from autotest.anor.mdeal.order.order_add.goods_page import GoodsPage
from autotest.anor.mdeal.order.order_add.final_page import FinalPage
from autotest.trade.tdeal.order.order_history_list.order_history_list import OrdersHistoryList
from utils.driver_setup import driver


def open_new_window(driver, url):
    time.sleep(2)
    driver.execute_script("window.open('');")
    all_windows = driver.window_handles
    driver.switch_to.window(all_windows[-1])
    driver.get(url)
    time.sleep(2)


def test_order_history(driver):
    # ------------------------------------------------------------------------------------------------------------------
    # Login_page
    # ------------------------------------------------------------------------------------------------------------------
    login_page = LoginPage(driver)
    login_page.fill_form('jasur@auto_test', '01062001')
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
    dashboard_page.click_sales_button()
    sales_navbar = SalesNavbar(driver)
    sales_navbar.element_visible()
    sales_navbar.click_orders_button()
    orders_page = OrdersPage(driver)
    orders_page.element_visible()
    after_count_orders = orders_page.check_order()
    # ------------------------------------------------------------------------------------------------------------------
    dashboard_page.click_sales_button()
    sales_navbar = SalesNavbar(driver)
    sales_navbar.element_visible()
    sales_navbar.click_orders_archive_button()
    # ------------------------------------------------------------------------------------------------------------------
    history_list = OrdersHistoryList(driver)
    history_list.element_visible()
    element = history_list.check_history()
    if element:
        print('There are no orders in the history list: we will create an order:')
        # ------------------------------------------------------------------------------------------------------------------
        dashboard_page.click_sales_button()
        # ------------------------------------------------------------------------------------------------------------------
        sales_navbar = SalesNavbar(driver)
        time.sleep(2)
        sales_navbar.element_visible()
        sales_navbar.click_orders_button()
        # ------------------------------------------------------------------------------------------------------------------
        orders_page = OrdersPage(driver)
        time.sleep(2)
        orders_page.element_visible()
        after_orders_count = orders_page.check_order()
        orders_page.click_add_button()
        # ------------------------------------------------------------------------------------------------------------------
        create_order_page = CreateOrderPage(driver)
        time.sleep(2)
        create_order_page.element_visible()
        order_request_number = random.randint(1, 9999)
        create_order_page.fill_form(order_request_number)
        create_order_page.click_button()
        # ------------------------------------------------------------------------------------------------------------------
        number = random.randint(1, 10)
        # ------------------------------------------------------------------------------------------------------------------
        goods_page = GoodsPage(driver)
        time.sleep(2)
        goods_page.element_visible()
        goods_page.fill_form(number)
        goods_page.click_button()
        # ------------------------------------------------------------------------------------------------------------------
        final_page = FinalPage(driver)
        time.sleep(2)
        final_page.fill_form()
        final_page.click_save_button()
        time.sleep(2)
        # ------------------------------------------------------------------------------------------------------------------
        driver.refresh()
        orders_page.element_visible()
        before_orders_count = orders_page.check_order()
        time.sleep(2)
        print(f"After orders count: {after_orders_count}")
        print(f"Before orders count: {before_orders_count}")

        try:
            assert before_orders_count == after_orders_count + 1, f"Error: expected number {after_orders_count + 1}, " \
                                                                  f"but the expected number {before_orders_count}"
            print("Order successfully added:")
        except AssertionError as e:
            print(f"{str(e)}")
            raise
        # ------------------------------------------------------------------------------------------------------------------
        orders_page.click_first_elem_button()
        orders_page.click_change_status_one_button()
        after_history_count_orders = orders_page.check_order()

        try:
            assert before_orders_count == after_history_count_orders, f"Error: expected number {after_history_count_orders}, " \
                                                                     f"but the expected number {after_orders_count}"
            print("Order status has been moved to archive:")
        except AssertionError as e:
            print(f"{str(e)}")
            raise

        dashboard_page.click_sales_button()
        sales_navbar = SalesNavbar(driver)
        time.sleep(2)
        sales_navbar.element_visible()
        sales_navbar.click_orders_archive_button()
    # ------------------------------------------------------------------------------------------------------------------
    else:
        print('There are orders in the history list')
    history_list.click_first_elem_button()
    history_list.click_view_button()
    # ------------------------------------------------------------------------------------------------------------------
    # view
    # ------------------------------------------------------------------------------------------------------------------
    history_view = OrderView(driver)
    history_view.element_visible()
    order_id = history_view.get_elements()
    print(f'Order id: {order_id}')
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
    after_count = history_list.check_order_history()
    history_list.click_change_status_one_button()
    driver.refresh()
    before_count = history_list.check_order_history()
    driver.refresh()

    try:
        assert after_count - 1 == before_count or None == element, f"Error: expected number {after_count - 1}, " \
                                                                   f"but got {before_count - 1 or element}"
        print(f"After quantity of orders in the archive: {after_count}"
              f"\nAfter: {after_count - 1}")
    except AssertionError as e:
        print(f"{str(e)}")
        raise
    # ------------------------------------------------------------------------------------------------------------------
    dashboard_page.click_sales_button()
    sales_navbar = SalesNavbar(driver)
    time.sleep(2)
    sales_navbar.element_visible()
    sales_navbar.click_orders_button()
    orders_page = OrdersPage(driver)
    time.sleep(2)
    orders_page.element_visible()
    before_count_orders = orders_page.check_order()

    try:
        assert after_count_orders == before_count_orders - 1, f"Error: expected number {after_count_orders}, " \
                                                              f"but got {before_count_orders - 1}"
        print(f"Quantity orders: {after_count_orders} ta \nAfter: {before_count_orders}")
    except AssertionError as e:
        print(f"{str(e)}")
        raise
    # ------------------------------------------------------------------------------------------------------------------
    orders_page.click_first_elem_button()
    orders_page.click_change_status_one_button(index=7)
    print(f'Delete order')
    # ------------------------------------------------------------------------------------------------------------------
    # Delete cancelled
    # ------------------------------------------------------------------------------------------------------------------
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'trade/tdeal/order/order_cancelled_list')
    cancelled_list = OrderCancelledList(driver)
    cancelled_list.element_visible()
    cancelled_list.click_first_elem_button()
    cancelled_list.click_delete_one_button()
    print(f'Delete cancelled')
    # ------------------------------------------------------------------------------------------------------------------

