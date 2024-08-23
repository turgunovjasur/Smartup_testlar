import time
from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.warehouse_navbar import WarehouseNavbar
from autotest.anor.mkw.purchase.purchase_list.purchase_list import PurchaseList
from autotest.anor.mkw.purchase.purchase_add.main_page import MainPage
from autotest.anor.mkw.purchase.purchase_add.inventory_page import InventoryPage
from autotest.anor.mkw.purchase.purchase_add.extra_cost_page import ExtraCostPage
from autotest.anor.mkw.purchase.purchase_add.finish_page import FinishPage
from autotest.anor.mkw.purchase.purchase_add.purchase_view.purchase_id import PurchaseId
from utils.driver_setup import driver


def test_purchase(driver):
    ##############################################################################
    # Login_page
    ##############################################################################
    email = 'admin@auto_test'
    password = ''
    ##############################################################################
    login_page = LoginPage(driver)
    login_page.fill_form(email, password,
                         LoginPage.email_xpath,
                         LoginPage.password_xpath)
    login_page.click_button(LoginPage.signup_xpath)
    ##############################################################################
    # Dashboard_page
    ##############################################################################
    dashboard_page = DashboardPage(driver)
    try:
        dashboard_page.element_visible_session(DashboardPage.active_session_header)
        dashboard_page.click_button_delete_session(DashboardPage.delete_session_button)
    except:
        pass
    dashboard_page.element_visible(dashboard_page.dashboard_header_xpath)
    dashboard_page.click_hover_show_button(DashboardPage.hover_show_button, DashboardPage.filial_button)
    dashboard_page.click_warehouse_button(dashboard_page.warehouse_button)
    ##############################################################################
    # Warehouse_navbar
    ##############################################################################
    warehouse_navbar = WarehouseNavbar(driver)
    warehouse_navbar.element_visible(warehouse_navbar.warehouse_navbar_header)
    warehouse_navbar.click_button_purchases(WarehouseNavbar.purchases_button)
    ##############################################################################
    # Purchase_list
    ##############################################################################
    purchase_list = PurchaseList(driver)
    purchase_list.element_visible(PurchaseList.purchase_list_header)
    purchase_list.click_button(PurchaseList.add_button)
    ##############################################################################
    # Main_page
    ##############################################################################
    purchase_main = MainPage(driver)
    purchase_main.element_visible(MainPage.main_page_header)
    purchase_main.fill_form(MainPage.ref_types_input, MainPage.ref_types_element, MainPage.payment_type_input,
                            MainPage.payment_type_element, MainPage.with_input_input, MainPage.warehouse_input,
                            MainPage.warehouse_element, MainPage.with_extra_costs_button)
    purchase_main.click_button(MainPage.next_step_button)
    ##############################################################################
    # Inventory_page
    ##############################################################################
    quantity = "10"
    price = "120000"
    margin_value = "20"
    vat_percent = "12"
    ##############################################################################
    inventory_page = InventoryPage(driver)
    inventory_page.element_visible(InventoryPage.inventory_page_header)
    inventory_page.fill_form(InventoryPage.fast_search_input,
                             InventoryPage.fast_search_element,
                             InventoryPage.quantity_input, quantity,
                             InventoryPage.price_input, price,
                             InventoryPage.side_scrolling,
                             InventoryPage.margin_value_button,
                             InventoryPage.margin_value_input, margin_value,
                             InventoryPage.vat_percent_input, vat_percent,
                             InventoryPage.get_amount,
                             InventoryPage.get_margin_amount,
                             InventoryPage.get_vat_amount,
                             InventoryPage.get_total_amount)
    numbers = inventory_page.check_number()
    start_amount = numbers['start_amount']  # 1_200_000
    start_margin_amount = numbers['start_margin_amount']  # 200
    start_vat_amount = numbers['start_vat_amount']  # 144_024
    start_total_amount = numbers['start_total_amount']  # 1_344_224
    inventory_page.click_button(InventoryPage.next_step_button)
    ##############################################################################
    # Extra_cost_page
    ##############################################################################
    extra_cost_page = ExtraCostPage(driver)
    extra_cost_page.element_visible(ExtraCostPage.extra_cost_page_header)
    extra_cost_page.click_button(ExtraCostPage.next_step_button)
    ##############################################################################
    # Final_page
    ##############################################################################
    finish_page = FinishPage(driver)
    finish_page.element_visible(FinishPage.finish_page_header)
    random_number = finish_page.random_number(FinishPage.purchase_number_input)
    print(f"random_number:{random_number}")
    finish_page.click_button(FinishPage.finish_page_save_button,
                             FinishPage.finish_page_yes_button)
    ##############################################################################
    # Check_purchase
    # Purchase_list
    ##############################################################################
    purchase_list = PurchaseList(driver)
    purchase_list.element_visible(PurchaseList.purchase_list_header)
    purchase_list.click_2x(PurchaseList.barcode_button)
    purchase_list.open_purchase_list(PurchaseList.first_list_purchase,
                                     PurchaseList.view_button)
    ##############################################################################
    # Purchase_id
    ##############################################################################
    purchase_id = PurchaseId(driver)
    purchase_id.element_visible(PurchaseId.purchase_id_header_xpath)
    purchase_number = purchase_id.get_purchase_number()
    print(f"purchase_number: {purchase_number}")
    purchase_id.fill_form(PurchaseId.inventory_button)
    total_amount_margin = purchase_id.get_elements()  # 1_200_200

    try:
        assert total_amount_margin == start_amount + start_margin_amount, f"Purchase id: {total_amount_margin}, Inventory page: {start_amount + start_margin_amount}"
        assert random_number == purchase_number, f"Error random number: {random_number} != {purchase_number}"
        print("Successfully!")
    except AssertionError as e:
        print(f"{str(e)}")
        raise
    ##############################################################################