import time

from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.warehouse_modal import WarehouseModal
from autotest.anor.mkw.purchase.purchase_list.purchase_list import PurchaseList
from autotest.anor.mkw.purchase.purchase_add.main_page import MainPage
from autotest.anor.mkw.purchase.purchase_add.inventory_page import InventoryPage
from autotest.anor.mkw.purchase.purchase_add.finish_page import FinishPage

from utils.driver_setup import driver


def test_purchase(driver):

    # Login_page
    login_page = LoginPage(driver)
    time.sleep(2)
    login_page.fill_form(LoginPage.email,
                         LoginPage.password,
                         LoginPage.email_xpath,
                         LoginPage.password_xpath)
    login_page.click_button(LoginPage.signup_xpath)

    # Dashboard_page
    dashboard_page = DashboardPage(driver)
    time.sleep(2)
    dashboard_page.element_visible(dashboard_page.dashboard_header_xpath)
    dashboard_page.click_organizations_button(DashboardPage.organizations_menu,
                                              DashboardPage.organizations_xpath)

    dashboard_page.click_warehouse_button(dashboard_page.warehouse_button_xpath)

    # Warehouse_modal
    warehouse_modal = WarehouseModal(driver)
    time.sleep(2)
    warehouse_modal.element_visible(warehouse_modal.warehouse_modal_header_xpath)
    warehouse_modal.click_button(WarehouseModal.purchases_button_xpath)

    # Purchase_list
    purchase_list = PurchaseList(driver)
    time.sleep(2)
    purchase_list.element_visible(PurchaseList.purchase_list_header_xpath)
    purchase_list.click_button(PurchaseList.create_button_xpath)

    # Main_page
    purchase_main = MainPage(driver)
    time.sleep(2)
    purchase_main.element_visible(MainPage.main_page_header_xpath)
    purchase_main.fill_form(MainPage.vendor,
                            MainPage.vendor_elem_xpath)
    purchase_main.click_button(MainPage.main_page_next_button_xpath)

    # Inventory_page
    inventory_page = InventoryPage(driver)
    time.sleep(2)
    inventory_page.element_visible(InventoryPage.inventory_page_header_xpath)
    inventory_page.fill_form(InventoryPage.inventory_input, InventoryPage.inventory,
                             InventoryPage.qty_input, InventoryPage.qty,
                             InventoryPage.price_input, InventoryPage.price,
                             InventoryPage.side_scrolling_xpath,
                             InventoryPage.margin_vat,
                             InventoryPage.margin_value_input, InventoryPage.margin_value,
                             InventoryPage.vat_input, InventoryPage.vat,
                             InventoryPage.count_xpath, InventoryPage.margin_count_xpath,
                             InventoryPage.vat_amount_xpath, InventoryPage.total_amount_xpath)
    inventory_page.click_button(InventoryPage.inventory_page_next_button_xpath)


    # Final_page
    final_page = FinishPage(driver)
    time.sleep(2)
    final_page.element_visible(FinishPage.finish_page_header_xpath)
    final_page.click_button(FinishPage.finish_page_save_button_xpath,
                            FinishPage.finish_page_yes_button_xpath)



