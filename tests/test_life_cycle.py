import random
import time

from autotest.anor.mcg.action_add.action_add import ActionAdd
from autotest.anor.mcg.action_list.action_list import ActionList
from autotest.anor.mcg.overload_add.overload_add import OverloadAdd
from autotest.anor.mcg.overload_list.overload_list import OverloadList
from autotest.anor.mkw.balance.balance_list.balance_list import BalanceList
from autotest.anor.mkw.init_balance.init_inventory_balance_add.init_inventory_balance_add import InitInventoryBalanceAdd
from autotest.anor.mkw.init_balance.init_inventory_balance_list.init_inventory_balance_list import \
    InitInventoryBalanceList
from autotest.anor.mr.product.inventory_add.inventory_new import InventoryNew
from autotest.anor.mr.product.inventory_list.inventory_list import InventoryList
from autotest.anor.mr.product.product_set_price.product_set_price import ProductSetPrice
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


def test_life_cycle(driver):
    # ------------------------------------------------------------------------------------------------------------------
    # Login_page
    # ------------------------------------------------------------------------------------------------------------------
    login_page = LoginPage(driver)
    login_page.fill_form('admin@test', 'greenwhite')
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

    filial_name = "AUTO TEST"
    dashboard_page.click_hover_show_button(filial_name)
    # ------------------------------------------------------------------------------------------------------------------
    # Product add
    # ------------------------------------------------------------------------------------------------------------------
    base_page = BasePage(driver)
    cut_url = base_page.cut_url()
    # open_new_window(driver, cut_url + 'anor/mr/product/inventory_list')  # InventoryList
    # inventory_list = InventoryList(driver)
    # inventory_list.element_visible()
    # inventory_list.click_add_button()
    # # ------------------------------------------------------------------------------------------------------------------
    # inventory_new = InventoryNew(driver)
    # inventory_new.element_visible()
    #
    # name_elem = "test_life_cycle"
    name_elem = "return_uchun"
    # inventory_new.input_name(name_elem)
    # inventory_new.input_measurement()
    # inventory_new.click_goods_checkbox()
    # inventory_new.click_product_checkbox()
    # inventory_new.input_order(1)  # product_order
    # inventory_new.click_save_button()
    # print('product add')
    # # ------------------------------------------------------------------------------------------------------------------
    # inventory_list.element_visible()
    # inventory_list.find_and_click_checkbox("test_life_cycle")  # name_elem
    # inventory_list.click_set_price_button()
    # # ------------------------------------------------------------------------------------------------------------------
    # price1 = 8000
    # price2 = 10000
    # product_set_price = ProductSetPrice(driver)
    # product_set_price.input_set_price(price1, price2)
    # product_set_price.click_save_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory balance add
    # ------------------------------------------------------------------------------------------------------------------
    # open_new_window(driver, cut_url + 'anor/mkw/init_balance/init_inventory_balance_list')  # InitInventoryBalanceList
    # init_inventory_balance_list = InitInventoryBalanceList(driver)
    # init_inventory_balance_list.click_add_button()
    # # ------------------------------------------------------------------------------------------------------------------
    # init_inventory_balance_add = InitInventoryBalanceAdd(driver)
    # #
    # balance_number = random.randint(1, 999999)
    # print(f"balance_number: {balance_number}")
    # init_inventory_balance_add.input_balance_number(balance_number)  # balance_number
    #
    # init_inventory_balance_add.input_warehouse_name()
    # init_inventory_balance_add.input_product_name()
    #
    # card_code = random.randint(1, 999)
    # init_inventory_balance_add.input_card_code(card_code)  # card_code
    #
    # quantity = random.randint(1, 11)
    # init_inventory_balance_add.input_quantity(quantity)  # quantity
    #
    # init_inventory_balance_add.input_price(price1)
    # init_inventory_balance_add.click_save_button()
    # init_inventory_balance_add.click_reload_button()
    # time.sleep(0.5)
    # init_inventory_balance_add.check_list_balance(balance_number)
    # init_inventory_balance_add.click_post_one_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Balance list -> first check
    # ------------------------------------------------------------------------------------------------------------------
    open_new_window(driver, cut_url + 'anor/mkw/balance/balance_list')  # BalanceList
    balance_list = BalanceList(driver)
    balance_list.click_reload_button()
    # print(name_elem)
    row_data = balance_list.check_list_balance(name_elem)
    print(row_data)
    if row_data:
        first_elem = row_data[0]
        print(f"Birinchi element: {first_elem}")
