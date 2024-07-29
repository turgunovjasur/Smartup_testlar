import time

from autotest.core.md.login_page import LoginPage
from autotest.trade.tdeal.sales_dashboard.dashboard_page import DashboardPage
from autotest.trade.tdeal.sales_dashboard.sales_modal import SalesModal
from autotest.trade.tdeal.order.order_list.orders_page import OrdersPage
from autotest.anor.mdeal.order.order_add.create_order_page import CreateOrderPage
from autotest.anor.mdeal.order.order_add.goods_page import GoodsPage
from autotest.anor.mdeal.order.order_add.final_page import FinalPage

from utils.driver_setup import driver

# Login_page
login_xpath = "//div/input[@placeholder='Логин@компания']"
password_xpath = "//div/input[@placeholder='Пароль']"
signup_xpath = "//div/button[contains(text(), 'Войти')]"

# Dashboard_page
dashboard_header_xpath = "//div/h3[contains(text(), 'Trade')]"
sales_button_xpath = "//li/a/span[contains(text(), 'Продажа')]"

# Sales_modal
sales_modal_header_xpath = "//h3/span[contains(text(), 'Продажа')]"
orders_button_xpath = "//a/span[contains(text(), 'Заказы')]"

# Order_page
order_page_header_xpath = "//ul/li/a[contains(text(), 'Опросники')]"
create_button_xpath = "//div/button[contains(text(), 'Создать')]"

# Create_order_page
create_order_header_xpath = "//div/h3/t[contains(text(), 'Основное')]"

order_request = '1'
order_request_xpath = "(//div/input[@placeholder = 'Поиск...'])[1]"

room_xpath = "(//div/input[@placeholder='Поиск...'])[2]"
robot_xpath = "(//div/input[@placeholder='Поиск...'])[3]"
client_xpath = "(//div/input[@placeholder='Поиск...'])[4]"

room_elem_xpath = '//*[@id="kt_content"]/div[2]/div/b-page/div/div/div/div/div/form[1]/div/div/div[3]/b-input/div/div[2]/div[1]/div[8]'
robot_elem_xpath = '//*[@id="kt_content"]/div[2]/div/b-page/div/div/div/div/div/form[1]/div/div/div[4]/div[1]/b-input/div/div[2]/div[2]/div[1]'
client_elem_xpath = '//*[@id="kt_content"]/div[2]/div/b-page/div/div/div/div/div/form[1]/div/div/div[5]/b-input/div/div[2]/div[2]/div[1]'

create_order_next_button_xpath = "//span/t[contains(text(), 'Далее')]"

# Goods_page
goods_page_header_xpath = "//div/h3/t[contains(text(), 'ТМЦ')]"

name_input_xpath = "(//div/input[@placeholder='Поиск...'])[8]"
name_elem_xpath = '/html/body/div[3]/div/div/div[2]/div[2]/div/b-page/div/div/div/div/div/form[2]/div/div/div/div[1]/div[2]/b-pg-grid/div/div/div[1]/div[2]/div[1]/div[1]/div/b-input/div/div[2]/div[2]/div[1]'

qty_input_xpath = "(//div/input[@ng-if='item.product_id'])[1]"
qty = '3'

goods_page_next_button_xpath = "//span/t[contains(text(), 'Далее')]"

# Final page
payment_type_input_xpath = '//*[@id="kt_content"]/div[2]/div/b-page/div/div/div/div/div/form[3]/div/div[2]/div/div/div[2]/b-input/div/div[1]/div/input'
payment_elem_xpath = '//*[@id="kt_content"]/div[2]/div/b-page/div/div/div/div/div/form[3]/div/div[2]/div/div/div[2]/b-input/div/div[2]/div[1]/div/div'
status_input_xpath = "(//div/span[@class = 'btn btn-default form-control ui-select-toggle'])[3]"
status_elem_xpath = '//*[@id="ui-select-choices-row-1-0"]/span'
save_button_xpath = "//span/t[contains(text(), 'Сохранить')]"
yes_button_xpath = "//div/button[contains(text(), 'да')]"


def test_all(driver):
    email = "admin@test"
    password = 'greenwhite'

    # Login_page
    login_page = LoginPage(driver)
    time.sleep(2)
    login_page.fill_form(email, password, login_xpath, password_xpath)
    login_page.click_button(signup_xpath)

    # Dashboard_page
    dashboard_page = DashboardPage(driver)
    time.sleep(2)
    dashboard_page.element_visible(dashboard_header_xpath)
    dashboard_page.click_button(sales_button_xpath)

    # Sales_modal
    sales_modal = SalesModal(driver)
    time.sleep(2)
    sales_modal.element_visible(sales_modal_header_xpath)
    sales_modal.click_button(orders_button_xpath)

    # Order_page
    orders_page = OrdersPage(driver)
    time.sleep(2)
    orders_page.element_visible(order_page_header_xpath)
    count_xpath = "//div[contains(@class, 'sg-cell') and contains(@class, 'col-sm-4') and contains(@class, 'ng-binding')]"
    count_orders = orders_page.check_count(count_xpath)
    print(f"First count: {count_orders}")
    orders_page.click_button(create_button_xpath)

    # Create_order_page
    create_order_page = CreateOrderPage(driver)
    time.sleep(2)
    create_order_page.element_visible(create_order_header_xpath)
    create_order_page.fill_form(order_request, order_request_xpath,
                                room_xpath, robot_xpath, client_xpath,
                                room_elem_xpath, robot_elem_xpath, client_elem_xpath)
    create_order_page.click_button(create_order_next_button_xpath)

    # Goods_page
    goods_page = GoodsPage(driver)
    time.sleep(2)
    goods_page.element_visible(goods_page_header_xpath)
    goods_page.fill_form(name_input_xpath, name_elem_xpath, qty_input_xpath, qty)
    goods_page.click_button(goods_page_next_button_xpath)

    # Final page
    final_page = FinalPage(driver)
    time.sleep(2)
    final_page.fill_form(payment_type_input_xpath, payment_elem_xpath,
                         status_input_xpath, status_elem_xpath)
    final_page.click_save_button(save_button_xpath, yes_button_xpath)

    ##################################### Cauntni tekshirish #####################################
    time.sleep(5)
    driver.refresh()
    time.sleep(5)

    orders_header_xpath = "//ul/li/a[contains(text(), 'Опросники')]"
    orders_expected_text = "Опросники"
    orders_error_message = "Order_page sahifa ochilmadi!"
    count_xpath = "//div[contains(@class, 'sg-cell') and contains(@class, 'col-sm-4') and contains(@class, 'ng-binding')]"

    check_orders_page = OrdersPage(driver)
    check_orders_page.element_visible(orders_header_xpath)
    time.sleep(5)
    new_count_orders = check_orders_page.check_count(count_xpath)
    print(f"New count: {new_count_orders}")

    try:
        assert new_count_orders == count_orders + 1, f"Error: expected number {count_orders + 1}, but the expected number {new_count_orders}"
        print("\033[92mProduct successfully added\033[0m")  # Yashil rangda xabar
    except AssertionError as e:
        print(f"\033[91m{str(e)}\033[0m")  # Qizil rangda xato xabari
        raise  # Xatoni qayta ko'tarish
    ##################################### Cauntni tekshirish #####################################
