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
    dashboard_page.click_warehouse_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Warehouse_navbar
    # ------------------------------------------------------------------------------------------------------------------
    warehouse_navbar = WarehouseNavbar(driver)
    warehouse_navbar.element_visible()
    warehouse_navbar.click_button_purchases()
    # ------------------------------------------------------------------------------------------------------------------
    # Purchase_list
    # ------------------------------------------------------------------------------------------------------------------
    purchase_list = PurchaseList(driver)
    purchase_list.element_visible()
    purchase_list.click_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Main_page
    # ------------------------------------------------------------------------------------------------------------------
    purchase_main = MainPage(driver)
    purchase_main.element_visible()
    purchase_main.fill_form()
    purchase_main.click_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_page
    # ------------------------------------------------------------------------------------------------------------------
    quantity = "10"
    price = "120000"
    margin_value = "20"
    vat_percent = "12"
    # ------------------------------------------------------------------------------------------------------------------
    inventory_page = InventoryPage(driver)
    inventory_page.element_visible()
    inventory_page.fill_form(quantity, price, margin_value, vat_percent)
    inventory_page.click_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Extra_cost_page
    # ------------------------------------------------------------------------------------------------------------------
    extra_cost_page = ExtraCostPage(driver)
    extra_cost_page.element_visible()
    extra_cost_page.click_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Finish_page
    # ------------------------------------------------------------------------------------------------------------------
    finish_page = FinishPage(driver)
    finish_page.element_visible()
    random_number = finish_page.random_number()
    print(f"random_number:{random_number}")
    finish_page.click_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Check_purchase
    # Purchase_list
    # ------------------------------------------------------------------------------------------------------------------
    purchase_list = PurchaseList(driver)
    purchase_list.element_visible()
    purchase_list.click_2x()
    purchase_list.open_purchase_list()
    # ------------------------------------------------------------------------------------------------------------------
    # Purchase_id
    # ------------------------------------------------------------------------------------------------------------------
    purchase_id = PurchaseId(driver)
    purchase_id.element_visible()
    purchase_number = purchase_id.get_purchase_number()
    print(f"purchase_number: {purchase_number}")
    purchase_id.fill_form()

    try:
        assert random_number == purchase_number, f"Error random number: {random_number} != {purchase_number}"
        print("Successfully!")
    except AssertionError as e:
        print(f"{str(e)}")
        raise
    # ------------------------------------------------------------------------------------------------------------------
