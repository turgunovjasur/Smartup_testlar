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
    # Warehouse_modal
    # ------------------------------------------------------------------------------------------------------------------
    warehouse_modal = WarehouseNavbar(driver)
    warehouse_modal.element_visible()
    warehouse_modal.click_button_internal_movements()
    # ------------------------------------------------------------------------------------------------------------------
    # Movement_list
    # ------------------------------------------------------------------------------------------------------------------
    movement_list = MovementList(driver)
    movement_list.element_visible(MovementList.movement_list_header)
    movement_list.click_button(MovementList.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Main_page
    # ------------------------------------------------------------------------------------------------------------------
    main_page = MainPage(driver)
    main_page.element_visible(MainPage.main_page_header)
    main_page.fill_form(MainPage.movement_number_input,
                        MainPage.from_warehouses_input,
                        MainPage.from_warehouses_elem,
                        MainPage.to_warehouses_input,
                        MainPage.to_warehouses_elem)
    random_number = main_page.random_number()
    print(f"random_number: {random_number}")
    main_page.click_button(MainPage.next_step_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_page
    # ------------------------------------------------------------------------------------------------------------------
    quantity = "1"
    # ------------------------------------------------------------------------------------------------------------------
    inventory_page = InventoryPage(driver)
    inventory_page.element_visible(InventoryPage.inventory_page_header)
    inventory_page.fill_form(InventoryPage.fast_search_input,
                             InventoryPage.fast_search_elem,
                             InventoryPage.quantity_input, quantity)
    inventory_page.click_button(InventoryPage.next_step_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Finish_page
    # ------------------------------------------------------------------------------------------------------------------
    text_area_text = "TEST"
    # ------------------------------------------------------------------------------------------------------------------
    finish_page = FinishPage(driver)
    finish_page.element_visible(FinishPage.finish_page_header)
    finish_page.fill_form(FinishPage.status_input,
                          FinishPage.status_elem,
                          FinishPage.text_area_input, text_area_text)
    finish_page.click_button(FinishPage.next_step_button,
                             FinishPage.yes_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Check Test
    # Movement_list
    # ------------------------------------------------------------------------------------------------------------------
    movement_list = MovementList(driver)
    movement_list.element_visible(MovementList.movement_list_header)
    movement_list.fill_form(MovementList.movement_list_first_elem,
                            MovementList.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Movement_id
    # ------------------------------------------------------------------------------------------------------------------
    movement_id = MovementId(driver)
    movement_id.element_visible(MovementId.card_title_header)
    movement_id.fill_form(MovementId.navi_inventory_button)
    elements = movement_id.check_number()
    print(f"movement_number: {elements}")

    try:
        assert random_number == elements, f"Random and ID not equal! {random_number} not equal {elements}"
        print("Successfully!")
    except AssertionError as e:
        print(f"{str(e)}")
        raise
    # ------------------------------------------------------------------------------------------------------------------
