import random
import time
from autotest.anor.mdeal.order.order_add.create_order_page import CreateOrderPage
from autotest.anor.mdeal.order.order_add.final_page import FinalPage
from autotest.anor.mdeal.order.order_add.goods_page import GoodsPage
from autotest.anor.mdeal.order.order_view.order_view import OrderView
from autotest.anor.mdeal.return_.return_add.return_add import ReturnAdd
from autotest.anor.mdeal.return_.return_list.return_list import ReturnList
from autotest.anor.mdeal.return_.return_view.return_view import ReturnView
from autotest.anor.mkw.balance.balance_list.balance_list import BalanceList
from autotest.core.md.base_page import BasePage
from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.sales_navbar import SalesNavbar
from autotest.trade.tdeal.order.order_cancelled_list.order_cancelled_list import OrderCancelledList
from autotest.trade.tdeal.order.order_history_list.order_history_list import OrdersHistoryList
from autotest.trade.tdeal.order.order_list.orders_page import OrdersPage
from utils.driver_setup import driver


def open_new_window(driver, url):
    time.sleep(2)
    driver.execute_script("window.open('');")
    all_windows = driver.window_handles
    driver.switch_to.window(all_windows[-1])
    driver.get(url)
    time.sleep(2)


def test_order_return(driver):
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
        dashboard_page.element_visible_session(timeout=2)
        dashboard_page.click_button_delete_session()
    except:
        pass
    dashboard_page.element_visible()
    dashboard_page.click_hover_show_button()
    # ------------------------------------------------------------------------------------------------------------------
    # add_order
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
    count_orders = orders_page.check_order()
    orders_page.click_add_button()
    # ------------------------------------------------------------------------------------------------------------------
    order_request_number = random.randint(1, 9999)
    print(f"Order request number: {order_request_number}")
    create_order_page = CreateOrderPage(driver)
    time.sleep(2)
    create_order_page.element_visible()
    create_order_page.fill_form(order_request_number)
    create_order_page.click_button()
    # ------------------------------------------------------------------------------------------------------------------
    quantity_order = random.randint(1, 10)
    print(f"Quantity order: {quantity_order}")
    goods_page = GoodsPage(driver)
    time.sleep(2)
    goods_page.element_visible()
    goods_page.fill_form(quantity_order)
    goods_page.click_button()
    # ------------------------------------------------------------------------------------------------------------------
    final_page = FinalPage(driver)
    time.sleep(2)
    final_page.fill_form()
    final_page.click_save_button()
    # ------------------------------------------------------------------------------------------------------------------
    orders_page = OrdersPage(driver)
    time.sleep(2)
    if orders_page.element_visible():
        driver.refresh()
    orders_page.element_visible()
    new_count_orders = orders_page.check_order()
    time.sleep(0.5)

    try:
        assert new_count_orders == count_orders + 1, f"Error: expected number {count_orders + 1}, but the expected number {new_count_orders}"
        print("Order successfully created:")
    except AssertionError as e:
        print(f"{str(e)}")
        raise
    # ------------------------------------------------------------------------------------------------------------------
    # order view
    # ------------------------------------------------------------------------------------------------------------------
    orders_page.click_first_elem_button()
    orders_page.click_view_button()
    order_view = OrderView(driver)
    order_view.element_visible()
    order_id = order_view.get_elements()
    print(f"Order id: {order_id}")
    order_view.click_close_button()
    # ------------------------------------------------------------------------------------------------------------------
    # order status history
    # ------------------------------------------------------------------------------------------------------------------
    # orders_page.click_first_elem_button()
    orders_page.click_change_status_one_button()
    after_history_count_orders = orders_page.check_order()

    try:
        assert new_count_orders == after_history_count_orders, f"Error: expected number {after_history_count_orders}, but the expected number {new_count_orders}"
        print("Order status moved history:")
    except AssertionError as e:
        print(f"{str(e)}")
        raise
    # ------------------------------------------------------------------------------------------------------------------
    # history -> return
    # ------------------------------------------------------------------------------------------------------------------
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    open_new_window(driver, cut_url + 'trade/tdeal/order/order_history_list')
    # ------------------------------------------------------------------------------------------------------------------
    history_list = OrdersHistoryList(driver)
    history_list.click_first_elem_button()
    history_list.click_view_button()
    # ------------------------------------------------------------------------------------------------------------------
    history_view = OrderView(driver)
    history_view.element_visible()
    history_id = history_view.get_elements()
    print(f'History id: {history_id}')
    time.sleep(1)
    history_view.click_close_button()
    # ------------------------------------------------------------------------------------------------------------------
    # check balance
    # ------------------------------------------------------------------------------------------------------------------
    open_new_window(driver, cut_url + 'anor/mkw/balance/balance_list')
    balance_list = BalanceList(driver)
    balance_list.element_visible()
    balance_before_return = balance_list.check_balance()
    # ------------------------------------------------------------------------------------------------------------------
    # order history -> return
    # ------------------------------------------------------------------------------------------------------------------
    open_new_window(driver, cut_url + 'trade/tdeal/order/order_history_list')
    history_list.click_first_elem_button()
    history_list.click_return_button()
    # ------------------------------------------------------------------------------------------------------------------
    # create return
    # ------------------------------------------------------------------------------------------------------------------
    return_add = ReturnAdd(driver)
    return_add.element_visible()
    return_add.input_warehouse()
    quantity_return = return_add.next_step_and_get_quantity()
    print(f"Quantity return: {quantity_return}")
    return_add.click_finish_button()
    time.sleep(1)
    # ------------------------------------------------------------------------------------------------------------------
    # check balance
    # ------------------------------------------------------------------------------------------------------------------
    open_new_window(driver, cut_url + 'anor/mkw/balance/balance_list')
    balance_list.element_visible()
    balance_after_return = balance_list.check_balance()
    try:
        assert balance_after_return == balance_before_return + quantity_return, \
            f"Error: expected number {balance_after_return}, " \
            f"but the expected number {balance_before_return + quantity_return}"
        print(f"Warehouse balance after Return: {balance_before_return}, "
              f"Warehouse balance before Return: {balance_after_return}")
        print("Return testing successful!")
    except AssertionError as e:
        print(f"{str(e)}")
        raise
    # ------------------------------------------------------------------------------------------------------------------
    # view return list
    # ------------------------------------------------------------------------------------------------------------------
    open_new_window(driver, cut_url + 'anor/mdeal/return/return_list')
    return_add = ReturnList(driver)
    return_add.element_visible()
    return_add.click_first_elem_button()
    return_add.click_view_button()
    # ------------------------------------------------------------------------------------------------------------------
    return_view = ReturnView(driver)
    return_view.element_visible()
    order_id, return_id = return_view.get_elements()
    print(f'Order id: {order_id}')
    print(f'Return id: {return_id}')
    return_view.click_close_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Delete return list
    # ------------------------------------------------------------------------------------------------------------------
    return_add.click_first_elem_button()
    return_add.click_draft_one_button()
    return_add.click_first_elem_button()
    return_add.click_delete_one_button()
    print(f'Delete return list')
    # ------------------------------------------------------------------------------------------------------------------
    # Delete history list
    # ------------------------------------------------------------------------------------------------------------------
    open_new_window(driver, cut_url + 'trade/tdeal/order/order_history_list')
    history_list.element_visible()
    history_list.click_first_elem_button()
    history_list.click_change_status_one_button()
    print(f'Delete history list')
    # ------------------------------------------------------------------------------------------------------------------
    # Delete order list
    # ------------------------------------------------------------------------------------------------------------------
    open_new_window(driver, cut_url + 'trade/tdeal/order/order_list')
    orders_page.element_visible()
    orders_page.click_first_elem_button()
    orders_page.click_change_status_one_button(index=7)
    print(f'Delete order list')
    # ------------------------------------------------------------------------------------------------------------------
    # Delete cancelled list
    # ------------------------------------------------------------------------------------------------------------------
    open_new_window(driver, cut_url + 'trade/tdeal/order/order_cancelled_list')
    cancelled_list = OrderCancelledList(driver)
    cancelled_list.element_visible()
    cancelled_list.click_first_elem_button()
    cancelled_list.click_delete_one_button()
    print(f'Delete cancelled list')
    # ------------------------------------------------------------------------------------------------------------------



