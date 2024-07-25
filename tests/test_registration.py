import time

from pages.login_page import LoginPage
from pages.dashboart_page import DashboartPage
from pages.sales_modal import SalesModal
from pages.orders_page import OrdersPage
from pages.goods_page import GoodsPage
from pages.final_page import FinalPage
from pages.create_order_page import CreateOrderPage
from utils.driver_setup import driver


def test_registration(driver):

    # Login page
    login = "admin@test"
    password = 'greenwhite'

    login_xpath = "//div/input[@placeholder='Логин@компания']"
    password_xpath = "//div/input[@placeholder='Пароль']"
    signup_xpath = "//div/button[contains(text(), 'Войти')]"

    # Dashboard page
    dashboard_header_xpath = "//div/h3[contains(text(), 'Trade')]"
    dashboard_expected_text = "Trade"
    dashboard_error_message = "Trade sahifa ochilmadi!"
    sales_button_xpath = "//li/a/span[contains(text(), 'Продажа')]"

    # Sales modal
    sales_modal_header_xpath = "//h3/span[contains(text(), 'Продажа')]"
    sales_modal_expected_text = "Продажа"
    sales_modal_error_message = "Sales_modal sahifasi ochilmadi!"
    orders_button_xpath = "//a/span[contains(text(), 'Заказы')]"

    # Orders page
    orders_header_xpath = "//ul/li/a[contains(text(), 'Опросники')]"
    orders_expected_text = "Опросники"
    orders_error_message = "Order_page sahifa ochilmadi!"
    create_button_xpath = "//div/button[contains(text(), 'Создать')]"
    count_xpath = "//div[contains(@class, 'sg-cell') and contains(@class, 'col-sm-4') and contains(@class, 'ng-binding')]"

    # Create order page
    create_order_header_xpath = "//div/h3/t[contains(text(), 'Основное')]"
    create_order_expected_text = "Основное"
    create_order_error_message = "Create_order_page Sahifa ochilmadi"
    workspace_xpath = "(//div/input[@placeholder='Поиск...'])[1]"
    workspace_elem_xpath = '//*[@id="kt_content"]/div[2]/div/b-page/div/div/div/div/div/form[1]/div/div/div[2]/b-input/div/div[2]/div[1]/div[1]/div'
    staff_unit_xpath = "(//div/input[@placeholder='Поиск...'])[2]"
    staff_unit_elem_xpath = '//*[@id="kt_content"]/div[2]/div/b-page/div/div/div/div/div/form[1]/div/div/div[3]/div[1]/b-input/div/div[2]/div[2]/div[1]/div/div[1]'
    client_xpath = "(//div/input[@placeholder='Поиск...'])[3]"
    client_elem_xpath = '//*[@id="kt_content"]/div[2]/div/b-page/div/div/div/div/div/form[1]/div/div/div[4]/b-input/div/div[2]/div[2]/div[1]/div/div[2]'
    next_button_xpath = "//span/t[contains(text(), 'Далее')]"

    # Goods page
    goods_header_xpath = "//div/h3/t[contains(text(), 'ТМЦ')]"
    goods_expected_text = "ТМЦ"
    goods_error_message = "Goods_page sahifa ochilmadi!"
    name_input_xpath = "(//div/input[@placeholder='Поиск...'])[7]"
    name_elem_xpath = "(//div[@class = 'col-sm-12 ng-binding'])[1]"
    qty_input_xpath = "(//div/input[@ng-if='item.product_id'])[1]"
    goods_next_button_xpath = "//span/t[contains(text(), 'Далее')]"
    name = 'Coca-Cola 1.5L / Coca-Cola Uzbekistan / Узбекистан'
    qty = '3'

    # Final page
    payment_type_input_xpath = '//*[@id="kt_content"]/div[2]/div/b-page/div/div/div/div/div/form[3]/div/div[2]/div/div/div[2]/b-input/div/div[1]/div/input'
    payment_elem_xpath = '//*[@id="kt_content"]/div[2]/div/b-page/div/div/div/div/div/form[3]/div/div[2]/div/div/div[2]/b-input/div/div[2]/div[1]/div/div'
    status_input_xpath = '//*[@id="kt_content"]/div[2]/div/b-page/div/div/div/div/div/form[3]/div/div[3]/div/div/div[6]/div'
    status_elem_xpath = '//*[@id="ui-select-choices-row-1-0"]/span'
    save_button_xpath = "//span/t[contains(text(), 'Сохранить')]"
    yes_button_xpath = "//div/button[contains(text(), 'да')]"




    ######### Login #########

    login_page = LoginPage(driver)
    login_page.fill_registration_form(login, password, login_xpath, password_xpath)
    login_page.click_sign_up_button(signup_xpath)

    # Dashboard
    dashboard_page = DashboartPage(driver)
    dashboard_page.check_page(dashboard_header_xpath, dashboard_expected_text, dashboard_error_message)
    dashboard_page.click_button(sales_button_xpath)

    # Sales modal
    sales_modal = SalesModal(driver)
    sales_modal.check_modal(sales_modal_header_xpath, sales_modal_expected_text, sales_modal_error_message)
    sales_modal.click_button(orders_button_xpath)

    # Orders page
    orders_page = OrdersPage(driver)
    orders_page.check_page(orders_header_xpath, orders_expected_text, orders_error_message)
    count_orders = orders_page.check_count(count_xpath)
    print(f"Boshlang'ich soni: {count_orders}")
    orders_page.click_create_button(create_button_xpath)

    # Create order page
    workspace = 'Family Group'
    staff_unit = 'BetterCall'
    client = '"SUXROB KAMOLOVICH NONLARI" OK'
    create_orders_page = CreateOrderPage(driver)
    create_orders_page.check_page(create_order_header_xpath, create_order_expected_text, create_order_error_message)
    create_orders_page.fill_form(workspace, staff_unit, client, workspace_xpath, workspace_elem_xpath,
                                 staff_unit_xpath, staff_unit_elem_xpath,
                                 client_xpath, client_elem_xpath)
    create_orders_page.click_next_button(next_button_xpath)

    # Goods page
    goods_page = GoodsPage(driver)
    orders_page.check_page(goods_header_xpath, goods_expected_text, goods_error_message)
    goods_page.fill_form(name_input_xpath, name_elem_xpath, qty_input_xpath, qty)
    goods_page.click_next_button(goods_next_button_xpath)

    # Final page
    payment_type = 'Наличные деньги'
    status = 'Черновик'
    final_page = FinalPage(driver)
    final_page.fill_form(payment_type, status, payment_type_input_xpath, payment_elem_xpath, status_input_xpath,
                         status_elem_xpath)
    final_page.click_save_button(save_button_xpath, yes_button_xpath)



    ######## Cauntni tekshirish #######

    time.sleep(5)
    driver.refresh()
    time.sleep(5)

    orders_header_xpath = "//ul/li/a[contains(text(), 'Опросники')]"
    orders_expected_text = "Опросники"
    orders_error_message = "Order_page sahifa ochilmadi!"
    count_xpath = "//div[contains(@class, 'sg-cell') and contains(@class, 'col-sm-4') and contains(@class, 'ng-binding')]"

    check_orders_page = OrdersPage(driver)
    check_orders_page.check_page(orders_header_xpath, orders_expected_text, orders_error_message)
    time.sleep(5)
    new_count_orders = check_orders_page.check_count(count_xpath)
    print(f"Yangi soni: {new_count_orders}")

    try:
        assert new_count_orders == count_orders + 1, f"Xatolik: Kutilgan son {count_orders + 1}, ammo haqiqiy son {new_count_orders}"
        print("\033[92mMahsulot muvaffaqiyatli qo'shildi\033[0m")  # Yashil rangda xabar
    except AssertionError as e:
        print(f"\033[91m{str(e)}\033[0m")  # Qizil rangda xato xabari
        raise  # Xatoni qayta ko'tarish
















# def test_all(driver):
#     login = "admin@test"
#     password = 'greenwhite'
#
#     login_page = LoginPage(driver)
#     login_page.fill_registration_form(login, password)
#     login_page.click_sign_up_button()
#
#     dashboard_page = DashboartPage(driver, 'Core')
#     dashboard_page.check_page()
#     dashboard_page.click_button()
#
#     sales_modal = SalesModal(driver)
#     sales_modal.check_modal()
#     sales_modal.click_button()
#
#     orders_page = OrdersPage(driver)
#     orders_page.check_page()
#     time.sleep(5)
#     count_orders = orders_page.check_count()
#     print(f"Boshlang'ich soni: {count_orders}")
#     orders_page.click_create_button()
#
#     workspace = 'Family Group'
#     staff_unit = 'BetterCall'
#     client = 'debtor'
#
#     create_orders_page = CreateOrderPage(driver)
#     create_orders_page.check_page()
#     create_orders_page.fill_form(workspace, staff_unit, client)
#     create_orders_page.click_next_button()
#
#     name = 'Product 2'
#     qty = '3'
#
#     goods_page = GoodsPage(driver)
#     goods_page.fill_form(qty)
#     goods_page.click_next_button()
#
#     payment_type = 'Наличные деньги'
#     status = 'Черновик'
#
#     final_page = FinalPage(driver)
#     final_page.fill_form(payment_type, status)
#     final_page.click_save_button()
#
#     time.sleep(5)
#     driver.refresh()
#     time.sleep(5)
#
#     check_orders_page = OrdersPage(driver)
#     check_orders_page.check_page()
#     time.sleep(5)
#     new_count_orders = check_orders_page.check_count()
#     print(f"Yangi soni: {new_count_orders}")
#
#     try:
#         assert new_count_orders == count_orders + 1, f"Xatolik: Kutilgan son {count_orders + 1}, ammo haqiqiy son {new_count_orders}"
#         print("\033[92mMahsulot muvaffaqiyatli qo'shildi\033[0m")  # Yashil rangda xabar
#     except AssertionError as e:
#         print(f"\033[91m{str(e)}\033[0m")  # Qizil rangda xato xabari
#         raise  # Xatoni qayta ko'tarish


# LOGIN_INPUT = (By.XPATH, "//div/input[@placeholder='Логин@компания']")
# PASSWORD_INPUT = (By.XPATH, "//div/input[@placeholder='Пароль']")
# SIGN_UP_BUTTON = (By.XPATH, "//div/button[contains(text(), 'Войти')]")