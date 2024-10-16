from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.warehouse_navbar import WarehouseNavbar
from autotest.anor.mkw.input.input_list.input_list import InputList
from autotest.anor.mkw.input.input_add.main_page import MainPage
from autotest.anor.mkw.input.input_add.purchase_page import PurchasePage
from autotest.anor.mkw.input.input_add.extra_cost import ExtraCostPage
from autotest.anor.mkw.input.input_add.finish_page import FinishPage
from autotest.anor.mkw.input.input_view.input_id import InputId
from utils.driver_setup import driver


def test_inventory_receipts(driver):
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
    warehouse_navbar.click_button_inventory_receipts()
    # ------------------------------------------------------------------------------------------------------------------
    # Input_list
    # ------------------------------------------------------------------------------------------------------------------
    input_list = InputList(driver)
    input_list.element_visible()
    input_list.click_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Main_page
    # ------------------------------------------------------------------------------------------------------------------
    main_page = MainPage(driver)
    main_page.element_visible()
    main_page.fill_form()
    random_receipt = main_page.random_number()
    print(f"random son:{random_receipt}")
    main_page.click_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Purchase_page
    # ------------------------------------------------------------------------------------------------------------------
    quantity = 1
    # ------------------------------------------------------------------------------------------------------------------
    purchase_page = PurchasePage(driver)
    purchase_page.element_visible()
    purchase_page.fill_form()
    purchase_page.calculate(quantity)
    purchase_page.click_button()
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
    finish_page.fill_form()
    finish_page.click_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Check_Input_list
    # Input_list
    # ------------------------------------------------------------------------------------------------------------------
    input_list = InputList(driver)
    input_list.element_visible()
    input_list.click_2x()
    input_list.fill_form()
    # ------------------------------------------------------------------------------------------------------------------
    # Input_id
    # ------------------------------------------------------------------------------------------------------------------
    input_id = InputId(driver)
    input_id.element_visible()
    input_id.fill_form()
    # ------------------------------------------------------------------------------------------------------------------
