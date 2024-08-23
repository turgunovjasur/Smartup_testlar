import time

from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.sales_navbar import SalesNavbar
from autotest.trade.tdeal.order.order_list.orders_page import OrdersPage
from autotest.anor.mdeal.order.order_add.create_order_page import CreateOrderPage
from autotest.anor.mdeal.order.order_add.goods_page import GoodsPage
from autotest.anor.mdeal.order.order_add.final_page import FinalPage

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from utils.driver_setup import driver


def test_all(driver):

    # Login_page
    login_page = LoginPage(driver)
    time.sleep(2)
    login_page.fill_form(LoginPage.email, LoginPage.password, LoginPage.email_xpath, LoginPage.password_xpath)
    login_page.click_button(LoginPage.signup_xpath)

    # Dashboard_page
    dashboard_page = DashboardPage(driver)
    time.sleep(2)
    dashboard_page.element_visible(dashboard_page.dashboard_header_xpath)
    dashboard_page.click_sales_button(dashboard_page.sales_button)

    # Sales_modal
    sales_modal = SalesNavbar(driver)
    time.sleep(2)
    sales_modal.element_visible(sales_modal.sales_navbar_header_xpath)
    sales_modal.click_button(sales_modal.orders_button_xpath)

    # Order_page
    orders_page = OrdersPage(driver)
    time.sleep(2)
    orders_page.element_visible(orders_page.order_page_header_xpath)
    count_orders = orders_page.check_count(orders_page.count_xpath)
    print(f"First count: {count_orders}")
    orders_page.click_button(orders_page.create_button_xpath)

    # Create_order_page
    create_order_page = CreateOrderPage(driver)
    time.sleep(2)
    create_order_page.element_visible(create_order_page.create_order_header_xpath)
    create_order_page.fill_form(create_order_page.order_request, create_order_page.order_request_xpath,
                                create_order_page.room_xpath, create_order_page.robot_xpath, create_order_page.client_xpath,
                                create_order_page.room_elem_xpath, create_order_page.robot_elem_xpath, create_order_page.client_elem_xpath)
    create_order_page.click_button(create_order_page.create_order_next_button_xpath)

    # Goods_page
    goods_page = GoodsPage(driver)
    time.sleep(2)
    goods_page.element_visible(GoodsPage.goods_page_header_xpath)
    goods_page.fill_form(GoodsPage.name_input_xpath, GoodsPage.name_elem_xpath, GoodsPage.qty_input_xpath, GoodsPage.qty)
    goods_page.click_button(GoodsPage.goods_page_next_button_xpath)

    # Final page
    final_page = FinalPage(driver)
    time.sleep(2)
    final_page.fill_form(FinalPage.payment_type_input_xpath, FinalPage.payment_elem_xpath,
                         FinalPage.status_input_xpath, FinalPage.status_elem_xpath)
    final_page.click_save_button(FinalPage.save_button_xpath, FinalPage.yes_button_xpath)

    # Check count
    time.sleep(2)
    driver.refresh()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, orders_page.order_page_header_xpath)))

    check_orders_page = OrdersPage(driver)
    check_orders_page.element_visible(orders_page.order_page_header_xpath)
    time.sleep(2)
    new_count_orders = check_orders_page.check_count(orders_page.count_xpath)
    print(f"New count: {new_count_orders}")

    try:
        assert new_count_orders == count_orders + 1, f"Error: expected number {count_orders + 1}, but the expected number {new_count_orders}"
        print("Product successfully added")
    except AssertionError as e:
        print(f"{str(e)}")
        raise