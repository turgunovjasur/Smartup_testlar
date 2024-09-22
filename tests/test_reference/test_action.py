import time

from autotest.anor.mcg.action_add.action_add import ActionAdd
from autotest.anor.mcg.action_list.action_list import ActionList
from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.reference_navbar import ReferenceNavbar

from utils.driver_setup import driver


def test_action(driver):
    # ------------------------------------------------------------------------------------------------------------------
    # Login_page:
    # ------------------------------------------------------------------------------------------------------------------
    email = 'admin@auto_test'
    password = 'greenwhite'
    # email = 'admin@test'
    # password = 'greenwhite'
    # ------------------------------------------------------------------------------------------------------------------
    login_page = LoginPage(driver)
    login_page.fill_form(email, password,
                         LoginPage.email_xpath,
                         LoginPage.password_xpath)
    login_page.click_button(LoginPage.signup_xpath)
    # ------------------------------------------------------------------------------------------------------------------
    # Dashboard_page:
    # ------------------------------------------------------------------------------------------------------------------
    dashboard_page = DashboardPage(driver)
    try:
        dashboard_page.element_visible_session(DashboardPage.active_session_header)
        dashboard_page.click_button_delete_session(DashboardPage.delete_session_button)
    except:
        pass
    dashboard_page.element_visible(dashboard_page.dashboard_header)
    dashboard_page.click_hover_show_button(DashboardPage.hover_show_button, DashboardPage.filial_button)
    dashboard_page.click_reference_button(dashboard_page.reference_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Reference_navbar
    # ------------------------------------------------------------------------------------------------------------------
    reference_navbar = ReferenceNavbar(driver)
    reference_navbar.click_action_button(ReferenceNavbar.action_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Action list:
    # ------------------------------------------------------------------------------------------------------------------
    action_list = ActionList(driver)
    action_list.element_visible(ActionList.header)
    action_list.click_add_button(ActionList.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Action add:
    # ------------------------------------------------------------------------------------------------------------------
    action_add = ActionAdd(driver)
    action_add.element_visible(ActionAdd.header)
    action_add.input_name(ActionAdd.name_input,
                          ActionAdd.name_elem)
    action_add.input_bonus_warehouse(ActionAdd.bonus_warehouse_input,
                                     ActionAdd.bonus_warehouse_elem)
    action_add.click_step_button(ActionAdd.next_step_button)
    action_add.input_type_condition(ActionAdd.type_condition_input,
                                    ActionAdd.type_condition_elem)
    action_add.input_inventory(ActionAdd.inventory_input,
                               ActionAdd.inventory_elem)
    action_add.input_inventory_quantity(ActionAdd.inventory_quantity_input,
                                        ActionAdd.inventory_quantity_elem)
    action_add.input_bonus_inventory(ActionAdd.bonus_inventory_input,
                                     ActionAdd.bonus_inventory_elem)
    action_add.input_bonus_inventory_quantity(ActionAdd.bonus_inventory_quantity_input,
                                              ActionAdd.bonus_inventory_quantity_elem)
    action_add.click_save_button(ActionAdd.save_button,
                                 ActionAdd.yes_button)
    print('click_save_button')
    # ------------------------------------------------------------------------------------------------------------------
    # Action delete:
    # ------------------------------------------------------------------------------------------------------------------
    action_list = ActionList(driver)
    action_list.element_visible(ActionList.header)
    action_list.click_first_elem_button(ActionList.action_list_first_elem)
    action_list.click_delete_one_button(ActionList.action_delete_one_button,
                                        ActionList.click_yes_delete_button)
    print('click_delete_one_button')
    # ------------------------------------------------------------------------------------------------------------------






























    # ------------------------------------------------------------------------------------------------------------------