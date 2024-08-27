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
    email = 'admin@auto_test'
    password = 'greenwhite'
    # ------------------------------------------------------------------------------------------------------------------
    login_page = LoginPage(driver)
    login_page.fill_form(email,
                         password,
                         LoginPage.email_xpath,
                         LoginPage.password_xpath)
    login_page.click_button(LoginPage.signup_xpath)
    # ------------------------------------------------------------------------------------------------------------------
    # Dashboard_page
    # ------------------------------------------------------------------------------------------------------------------
    dashboard_page = DashboardPage(driver)
    try:
        dashboard_page.element_visible_session(DashboardPage.active_session_header)
        dashboard_page.click_button_delete_session(DashboardPage.delete_session_button)
    except:
        pass
    dashboard_page.element_visible(dashboard_page.dashboard_header)
    dashboard_page.click_hover_show_button(DashboardPage.hover_show_button,
                                           DashboardPage.filial_button)
    dashboard_page.click_warehouse_button(dashboard_page.warehouse_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Warehouse_navbar
    # ------------------------------------------------------------------------------------------------------------------
    warehouse_navbar = WarehouseNavbar(driver)
    warehouse_navbar.element_visible(warehouse_navbar.warehouse_navbar_header)
    warehouse_navbar.click_button_inventory_receipts(WarehouseNavbar.inventory_receipts_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Input_list
    # ------------------------------------------------------------------------------------------------------------------
    input_list = InputList(driver)
    input_list.element_visible(InputList.input_list_header)
    input_list.click_button(InputList.create_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Main_page
    # ------------------------------------------------------------------------------------------------------------------
    main_page = MainPage(driver)
    main_page.element_visible(MainPage.main_page_header)
    main_page.fill_form(MainPage.input_number_input,
                        MainPage.warehouse_input,
                        MainPage.warehouse_elem,
                        MainPage.extra_cost_enabled_checkbox)
    random_receipt = main_page.random_number()
    print(f"random son:{random_receipt}")
    main_page.click_button(MainPage.next_step_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Purchase_page
    # ------------------------------------------------------------------------------------------------------------------
    quantity = "1"
    price_start = 120000
    margin_start = 20
    vat_start = 12
    amount_start = int(quantity) * price_start
    # ------------------------------------------------------------------------------------------------------------------
    purchase_page = PurchasePage(driver)
    purchase_page.element_visible(PurchasePage.purchase_page_header)
    purchase_page.fill_form(PurchasePage.purchases_input,
                            PurchasePage.purchases_elem,
                            PurchasePage.quantity_input,
                            quantity)
    purchase_page.calculate(price_start,
                            PurchasePage.price_finish,
                            margin_start,
                            PurchasePage.margin_finish,
                            vat_start,
                            PurchasePage.vat_finish,
                            amount_start,
                            PurchasePage.amount_finish)
    numbers = purchase_page.check_number()

    price = numbers['price']
    margin = numbers['margin']
    vat = numbers['vat']
    amount = numbers['amount']

    purchase_page.click_button(PurchasePage.next_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Extra_cost_page
    # ------------------------------------------------------------------------------------------------------------------
    extra_cost_page = ExtraCostPage(driver)
    extra_cost_page.element_visible(ExtraCostPage.extra_cost_page_header)
    extra_cost_page.click_button(ExtraCostPage.next_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Finish_page
    # ------------------------------------------------------------------------------------------------------------------
    finish_page = FinishPage(driver)
    finish_page.element_visible(FinishPage.finish_page_header)
    finish_page.fill_form(FinishPage.status_input,
                          finish_page.status)
    finish_page.click_button(FinishPage.next_button,
                             FinishPage.save_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Check_Input_list
    # Input_list
    # ------------------------------------------------------------------------------------------------------------------
    input_list = InputList(driver)
    input_list.element_visible(InputList.input_list_header)
    input_list.click_2x(InputList.date_button)
    input_list.fill_form(InputList.first_element,
                         InputList.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Input_id
    # ------------------------------------------------------------------------------------------------------------------
    input_id = InputId(driver)
    input_id.element_visible(InputId.input_id_header)
    input_id.fill_form(InputId.inventory_button)
    elements = input_id.get_elements()
    total_amount = elements['start_total_amount']
    quantity = elements['quantity']
    print(f"start_total_amount: {total_amount}")
    print(f"quantity: {quantity}")

    try:
        assert quantity * price == total_amount, f"Input id: {total_amount}, Purchase page: {quantity * price}"
        print("Successfully!")
    except AssertionError as e:
        print(f"{str(e)}")
        raise
    # ------------------------------------------------------------------------------------------------------------------
