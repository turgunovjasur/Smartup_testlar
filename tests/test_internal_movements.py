from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.warehouse_navbar import WarehouseNavbar
from autotest.anor.mkw.movement.movement_list.movement_list import MovementList
from autotest.anor.mkw.movement.movement_add.main_page import MainPage
from autotest.anor.mkw.movement.movement_add.inventory_page import InventoryPage
from autotest.anor.mkw.movement.movement_add.finish_page import FinishPage
from autotest.anor.mkw.movement.movement_view.movement_id import MovementId
from utils.driver_setup import driver


def test_internal_movements(driver):
    # Login_page
    ##############################################################################
    email = 'admin@auto_test'
    password = ''
    ##############################################################################
    login_page = LoginPage(driver)
    login_page.fill_form(email,
                         password,
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
    # Warehouse_modal
    ##############################################################################
    warehouse_modal = WarehouseNavbar(driver)
    warehouse_modal.element_visible(warehouse_modal.warehouse_navbar_header)
    warehouse_modal.click_button_internal_movements(WarehouseNavbar.internal_movements_button)
    ##############################################################################
    # Movement_list
    ##############################################################################
    movement_list = MovementList(driver)
    movement_list.element_visible(MovementList.movement_list_header)
    movement_list.click_button(MovementList.movement_list_header)
    ##############################################################################
    # Main_page
    ##############################################################################
    main_page = MainPage(driver)
    main_page.element_visible(MainPage.main_page_header)
    main_page.fill_form(MainPage.movement_no_input,
                        MainPage.consignor_warehouse,
                        MainPage.consignor_warehouse_elem,
                        MainPage.consignee_warehouse,
                        MainPage.consignee_warehouse_elem)
    random_number = main_page.random_number()
    print(f"random_number: {random_number}")
    main_page.click_button(MainPage.next_button)
    ##############################################################################
    # Inventory_page
    ##############################################################################
    inventory_page = InventoryPage(driver)
    inventory_page.element_visible(InventoryPage.inventory_page_header_xpath)
    inventory_page.fill_form(InventoryPage.inventory_input,
                             InventoryPage.inventory_input_elem,
                             InventoryPage.quantity_input,
                             InventoryPage.quantity)
    inventory_page.click_button(InventoryPage.next_button)
    ##############################################################################
    # Finish_page
    ##############################################################################
    finish_page = FinishPage(driver)
    finish_page.element_visible(FinishPage.finish_page_header)
    finish_page.fill_form(FinishPage.status_input,
                          FinishPage.status_input_elem)
    finish_page.click_button(FinishPage.next_button_xpath,
                             FinishPage.save_button_xpath)
    ##############################################################################
    # Check Test
    # Movement_list
    ##############################################################################
    movement_list = MovementList(driver)
    movement_list.element_visible(MovementList.movement_list_header)
    movement_list.fill_form(MovementList.movement_list_first,
                            MovementList.view_button)
    ##############################################################################
    # Movement_id
    ##############################################################################
    movement_id = MovementId(driver)
    movement_id.element_visible(MovementId.movement_id_header)
    elements = movement_id.get_elements()
    number_id = elements['number']
    print(f"number_id: {number_id}")

    try:
        assert random_number == number_id, f"Random and ID not equal! {random_number} not equal {number_id}"
        print("Successfully!")
    except AssertionError as e:
        print(f"{str(e)}")
        raise
    ##############################################################################
