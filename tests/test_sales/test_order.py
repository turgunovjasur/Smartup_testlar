import random
import time

from autotest.anor.mcg.action_add.action_add import ActionAdd
from autotest.anor.mcg.action_list.action_list import ActionList
from autotest.anor.mcg.overload_add.overload_add import OverloadAdd
from autotest.anor.mcg.overload_list.overload_list import OverloadList
from autotest.core.md.base_page import BasePage
from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.sales_navbar import SalesNavbar
from autotest.trade.tdeal.order.order_cancelled_list.order_cancelled_list import OrderCancelledList
from autotest.trade.tdeal.order.order_list.orders_page import OrdersPage
from autotest.anor.mdeal.order.order_add.create_order_page import CreateOrderPage
from autotest.anor.mdeal.order.order_add.goods_page import GoodsPage
from autotest.anor.mdeal.order.order_add.final_page import FinalPage
from utils.driver_setup import driver


def open_new_window(driver, url):
    time.sleep(2)
    driver.execute_script("window.open('');")
    all_windows = driver.window_handles
    driver.switch_to.window(all_windows[-1])
    driver.get(url)
    time.sleep(2)


def switch_to_main_window(driver):
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)
    # print("Returned to main window:", driver.current_url)


def test_order(driver):
    # ------------------------------------------------------------------------------------------------------------------
    # Login_page
    # ------------------------------------------------------------------------------------------------------------------
    login_page = LoginPage(driver)
    login_page.fill_form('admin@auto_test', 'greenwhite')
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
    after_orders_count = orders_page.check_order()
    orders_page.click_add_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Create_order_page
    # ------------------------------------------------------------------------------------------------------------------
    create_order_page = CreateOrderPage(driver)
    order_request_number = random.randint(1, 9999)
    time.sleep(2)
    create_order_page.element_visible()
    create_order_page.fill_form(order_request_number)
    create_order_page.click_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Goods_page / Action / Overload
    # ------------------------------------------------------------------------------------------------------------------
    number = random.randint(10, 20)
    # ------------------------------------------------------------------------------------------------------------------
    goods_page = GoodsPage(driver)
    time.sleep(2)
    goods_page.element_visible()
    goods_page.fill_form(number)
    # ------------------------------------------------------------------------------------------------------------------
    # Overload
    # ------------------------------------------------------------------------------------------------------------------
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    # ------------------------------------------------------------------------------------------------------------------
    if number >= 10:
        goods_page.click_overload_button()
        overload = goods_page.overload_is_visible()
        if overload is False:
            # ------------------------------------------------------------------------------------------------------------------
            # Overload add:
            # ------------------------------------------------------------------------------------------------------------------
            open_new_window(driver, cut_url + 'anor/mcg/overload+add')
            overload_add = OverloadAdd(driver)
            overload_add.element_visible()
            overload_add.input_name('for_order_test')
            overload_add.input_product()
            overload_add.input_conditions_quantity('10')
            overload_add.input_overload_product()
            overload_add.input_overload_product_quantity('1')
            overload_add.click_save_button()
            time.sleep(2)
            print('Overload add:')
            # ------------------------------------------------------------------------------------------------------------------
            switch_to_main_window(driver)
            driver.refresh()
            create_order_page.fill_form(order_request_number)
            create_order_page.click_button()
            number = random.randint(10, 20)
            goods_page.element_visible()
            goods_page.fill_form(number)
    # ------------------------------------------------------------------------------------------------------------------
    # Action
    # ------------------------------------------------------------------------------------------------------------------
    if number >= 10:
        goods_page.click_action_button()
        action = goods_page.action_is_visible()
        if action is False:
            # ------------------------------------------------------------------------------------------------------------------
            # Action add:
            # ------------------------------------------------------------------------------------------------------------------
            open_new_window(driver, cut_url + 'anor/mcg/action+add')
            action_add = ActionAdd(driver)
            action_add.element_visible()
            action_add.input_name('for_order_test')
            action_add.input_end_date('31.12.2024')
            action_add.input_room()
            action_add.input_bonus_warehouse()
            action_add.click_step_button()
            action_add.input_type_condition()
            action_add.input_inventory()
            action_add.input_inventory_quantity('10')
            action_add.input_bonus_inventory()
            action_add.input_bonus_inventory_quantity('1')
            action_add.click_save_button()
            time.sleep(2)
            print('Action add:')
            # ------------------------------------------------------------------------------------------------------------------
            switch_to_main_window(driver)
            driver.refresh()
            create_order_page.fill_form(order_request_number)
            create_order_page.click_button()
            number = random.randint(10, 20)
            goods_page.element_visible()
            goods_page.fill_form(number)
    # ------------------------------------------------------------------------------------------------------------------
    goods_page.click_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Final page
    # ------------------------------------------------------------------------------------------------------------------
    final_page = FinalPage(driver)
    final_page.fill_form()
    final_page.click_save_button()
    time.sleep(5)
    # ------------------------------------------------------------------------------------------------------------------
    # Check count
    # ------------------------------------------------------------------------------------------------------------------
    orders_page.element_visible()
    before_orders_count = orders_page.check_order()
    time.sleep(0.5)
    print(f"After count: {after_orders_count}")
    print(f"Before count: {before_orders_count}")
    try:
        assert before_orders_count == after_orders_count + 1, f"Error: expected number {after_orders_count + 1}, " \
                                                              f"but the expected number {before_orders_count}"
        print("Order successfully added:")
    except AssertionError as e:
        print(f"{str(e)}")
        raise
    # ------------------------------------------------------------------------------------------------------------------
    # Delete order
    # ------------------------------------------------------------------------------------------------------------------
    orders_page.click_first_elem_button()
    orders_page.click_change_status_one_button(index=7)
    print(f'Delete order')
    # ------------------------------------------------------------------------------------------------------------------
    # Delete cancelled
    # ------------------------------------------------------------------------------------------------------------------
    open_new_window(driver, cut_url + 'trade/tdeal/order/order_cancelled_list')
    cancelled_list = OrderCancelledList(driver)
    cancelled_list.element_visible()
    cancelled_list.click_first_elem_button()
    cancelled_list.click_delete_one_button()
    print(f'Delete cancelled')
    # ------------------------------------------------------------------------------------------------------------------
    # Delete action
    # ------------------------------------------------------------------------------------------------------------------
    open_new_window(driver, cut_url + 'anor/mcg/action_list')
    action_list = ActionList(driver)
    action_list.element_visible()
    action_list.click_first_elem_button()
    action_list.click_delete_one_button()
    time.sleep(1)
    print(f'Delete action')
    # ------------------------------------------------------------------------------------------------------------------
    # Delete overload
    # ------------------------------------------------------------------------------------------------------------------
    open_new_window(driver, cut_url + 'anor/mcg/overload_list')
    overload_list = OverloadList(driver)
    overload_list.click_first_elem_button()
    overload_list.click_status_one_button()
    time.sleep(1)
    print(f'Delete overload')
    # ------------------------------------------------------------------------------------------------------------------



