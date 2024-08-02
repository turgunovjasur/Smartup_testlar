import time

from autotest.core.md.login_page import LoginPage
from autotest.trade.tdeal.sales_dashboard.dashboard_page import DashboardPage
from autotest.trade.tdeal.sales_dashboard.sales_modal import SalesModal
from autotest.trade.tdeal.order.order_list.orders_page import OrdersPage
from autotest.anor.mdeal.order.order_add.create_order_page import CreateOrderPage
from autotest.anor.mdeal.order.order_add.goods_page import GoodsPage
from autotest.anor.mdeal.order.order_add.final_page import FinalPage

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from element_xpath.xpaths import Xpath

from utils.driver_setup import driver


def test_all(driver):

    # Login_page
    login_page = LoginPage(driver)
    time.sleep(2)
    login_page.fill_form(Xpath.email, Xpath.password, Xpath.email_xpath, Xpath.password_xpath)
    login_page.click_button(Xpath.signup_xpath)


    # Dashboard_page
    dashboard_page = DashboardPage(driver)
    time.sleep(2)
    dashboard_page.element_visible(Xpath.dashboard_header_xpath)
    dashboard_page.click_button(Xpath.sales_button_xpath)


    # Sales_modal
    sales_modal = SalesModal(driver)
    time.sleep(2)
    sales_modal.element_visible(Xpath.sales_modal_header_xpath)
    sales_modal.click_button(Xpath.orders_button_xpath)


    # Order_page
    orders_page = OrdersPage(driver)
    time.sleep(2)
    orders_page.element_visible(Xpath.order_page_header_xpath)
    count_orders = orders_page.check_count(Xpath.count_xpath)
    print(f"First count: {count_orders}")
    orders_page.click_button(Xpath.create_button_xpath)


    # Create_order_page
    create_order_page = CreateOrderPage(driver)
    time.sleep(2)
    create_order_page.element_visible(Xpath.create_order_header_xpath)
    create_order_page.fill_form(Xpath.order_request, Xpath.order_request_xpath,
                                Xpath.room_xpath, Xpath.robot_xpath, Xpath.client_xpath,
                                Xpath.room_elem_xpath, Xpath.robot_elem_xpath, Xpath.client_elem_xpath)
    create_order_page.click_button(Xpath.create_order_next_button_xpath)


    # Goods_page
    goods_page = GoodsPage(driver)
    time.sleep(2)
    goods_page.element_visible(Xpath.goods_page_header_xpath)
    goods_page.fill_form(Xpath.name_input_xpath, Xpath.name_elem_xpath, Xpath.qty_input_xpath, Xpath.qty)
    goods_page.click_button(Xpath.goods_page_next_button_xpath)


    # Final page
    final_page = FinalPage(driver)
    time.sleep(2)
    final_page.fill_form(Xpath.payment_type_input_xpath, Xpath.payment_elem_xpath,
                         Xpath.status_input_xpath, Xpath.status_elem_xpath)
    final_page.click_save_button(Xpath.save_button_xpath, Xpath.yes_button_xpath)


    # Check count
    time.sleep(2)
    driver.refresh()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Xpath.order_page_header_xpath)))

    check_orders_page = OrdersPage(driver)
    check_orders_page.element_visible(Xpath.order_page_header_xpath)
    time.sleep(2)
    new_count_orders = check_orders_page.check_count(Xpath.count_xpath)
    print(f"New count: {new_count_orders}")

    try:
        assert new_count_orders == count_orders + 1, f"Error: expected number {count_orders + 1}, but the expected number {new_count_orders}"
        print("Product successfully added")
    except AssertionError as e:
        print(f"{str(e)}")
        raise