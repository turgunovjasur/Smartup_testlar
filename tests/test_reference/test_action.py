from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.reference_navbar import ReferenceNavbar
from autotest.anor.mcg.action_list.action_list import ActionList
from autotest.anor.mcg.action_add.action_add import ActionAdd
from autotest.anor.mcg.action_view.action_view import ActionIdView
from autotest.anor.mcg.action_edit.action_edit import ActionIdEdit
from utils.driver_setup import driver


def test_actions(driver):
    # ------------------------------------------------------------------------------------------------------------------
    # Login_page:
    # ------------------------------------------------------------------------------------------------------------------
    login_page = LoginPage(driver)
    login_page.fill_form('admin@auto_test', 'greenwhite')
    login_page.click_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Dashboard_page:
    # ------------------------------------------------------------------------------------------------------------------
    dashboard_page = DashboardPage(driver)
    try:
        dashboard_page.element_visible_session()
        dashboard_page.click_button_delete_session()
    except:
        pass
    dashboard_page.element_visible()
    dashboard_page.click_hover_show_button()
    dashboard_page.click_reference_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Reference_navbar
    # ------------------------------------------------------------------------------------------------------------------
    reference_navbar = ReferenceNavbar(driver)
    reference_navbar.click_action_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Action list:
    # ------------------------------------------------------------------------------------------------------------------
    action_list = ActionList(driver)
    action_list.element_visible()
    action_list.click_add_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Action add:
    # ------------------------------------------------------------------------------------------------------------------
    name_elem = 'action_add'
    end_date = '31.12.2024'
    inventory_quantity_elem = '10'
    bonus_inventory_quantity_elem = '1'
    # ------------------------------------------------------------------------------------------------------------------
    action_add = ActionAdd(driver)
    action_add.element_visible()
    action_add.input_name(name_elem)
    action_add.input_end_date(end_date)
    action_add.input_room()
    action_add.input_bonus_warehouse()
    action_add.click_step_button()
    action_add.input_type_condition()
    action_add.input_inventory()
    action_add.input_inventory_quantity(inventory_quantity_elem)
    action_add.input_bonus_inventory()
    action_add.input_bonus_inventory_quantity(bonus_inventory_quantity_elem)
    action_add.click_save_button()
    print('Action add:')
    # ------------------------------------------------------------------------------------------------------------------
    # Action view:
    # ------------------------------------------------------------------------------------------------------------------
    action_list.find_and_click_checkbox(name_elem)
    action_list.click_view_button()
    # ------------------------------------------------------------------------------------------------------------------
    action_view = ActionIdView(driver)
    action_view.element_visible()
    name = action_view.get_elements()
    try:
        assert name_elem == name, f"Add: {name_elem}, View: {name}"
        print(f"Successfully! Added: {name_elem}, Seen: {name}")
    except AssertionError as e:
        print(f"{str(e)}")
        raise

    action_view.click_close_button()
    print('Action view:')
    # ------------------------------------------------------------------------------------------------------------------
    # Action edit:
    # ------------------------------------------------------------------------------------------------------------------
    action_list.find_and_click_checkbox(name_elem)
    action_list.click_edit_button()
    # ------------------------------------------------------------------------------------------------------------------
    name_text = "action_edit"
    inventory_quantity_elem = '11'
    bonus_inventory_quantity_elem = '2'
    # ------------------------------------------------------------------------------------------------------------------
    action_edit = ActionIdEdit(driver)
    action_edit.element_visible()
    action_edit.input_name(name_text)
    action_edit.click_step_button()
    action_edit.input_inventory_quantity(inventory_quantity_elem)
    action_edit.input_bonus_inventory_quantity(bonus_inventory_quantity_elem)
    action_edit.click_save_button()
    print('Action edit:')
    # ------------------------------------------------------------------------------------------------------------------
    # Action inactive:
    # ------------------------------------------------------------------------------------------------------------------
    action_list.find_and_click_checkbox(name_text)
    action_list.click_status_one_button()
    print('Action inactive:')
    # ------------------------------------------------------------------------------------------------------------------
    # Action active:
    # ------------------------------------------------------------------------------------------------------------------
    action_list = ActionList(driver)
    action_list.element_visible()
    action_list.click_filter_button()
    action_list.click_show_all_button()
    action_list.find_and_click_checkbox(name_text)
    action_list.click_status_one_button()
    print('Action active:')
    # ------------------------------------------------------------------------------------------------------------------
    # Action delete:
    # ------------------------------------------------------------------------------------------------------------------
    action_list.find_and_click_checkbox(name_text)
    action_list.click_delete_one_button()
    print('Action delete:')
    # ------------------------------------------------------------------------------------------------------------------
    # Action add_2:
    # ------------------------------------------------------------------------------------------------------------------
    name_elem = 'action_add'
    inventory_quantity_elem = '10'
    bonus_inventory_quantity_elem = '1'
    # ------------------------------------------------------------------------------------------------------------------
    driver.refresh()
    action_list = ActionList(driver)
    action_list.element_visible()
    action_list.click_add_button()
    # ------------------------------------------------------------------------------------------------------------------
    action_add = ActionAdd(driver)
    action_add.element_visible()
    action_add.input_name(name_elem)
    action_add.input_end_date(end_date)
    action_add.input_room()
    action_add.input_bonus_warehouse()
    action_add.click_step_button()
    action_add.input_type_condition()
    action_add.input_inventory()
    action_add.input_inventory_quantity(inventory_quantity_elem)
    action_add.input_bonus_inventory()
    action_add.input_bonus_inventory_quantity(bonus_inventory_quantity_elem)
    action_add.click_save_button()
    print('Action add_2:')
    # ------------------------------------------------------------------------------------------------------------------
    # Action inactive (many):
    # ------------------------------------------------------------------------------------------------------------------
    action_list = ActionList(driver)
    action_list.element_visible()
    action_list.find_and_click_checkbox(name_elem, checkbox=True)
    action_list.click_status_many_button()
    print('Action inactive (many):')
    # ------------------------------------------------------------------------------------------------------------------
    # Action active (many):
    # ------------------------------------------------------------------------------------------------------------------
    action_list = ActionList(driver)
    action_list.element_visible()
    action_list.click_filter_button()
    action_list.click_show_all_button()
    action_list.click_row_button()
    action_list.find_and_click_checkbox(name_elem, checkbox=True)
    action_list.click_status_many_button()
    print('Action active (many):')
    # ------------------------------------------------------------------------------------------------------------------
    # Action delete (many):
    # ------------------------------------------------------------------------------------------------------------------
    action_list = ActionList(driver)
    action_list.element_visible()
    action_list.find_and_click_checkbox(name_elem, checkbox=True)
    action_list.click_delete_many_button()
    print('Action delete (many):')
    # ------------------------------------------------------------------------------------------------------------------
