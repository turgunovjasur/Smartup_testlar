from autotest.anor.mcg.overload_add.overload_add import OverloadAdd
from autotest.anor.mcg.overload_list.overload_list import OverloadList
from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.reference_navbar import ReferenceNavbar

from utils.driver_setup import driver


def test_overload(driver):
    # ------------------------------------------------------------------------------------------------------------------
    # Login_page:
    # ------------------------------------------------------------------------------------------------------------------
    email = 'admin@auto_test'
    password = 'greenwhite'
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
    reference_navbar.click_action_button(ReferenceNavbar.overload_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Overload list:
    # ------------------------------------------------------------------------------------------------------------------
    overload_list = OverloadList(driver)
    overload_list.element_visible(OverloadList.header)
    overload_list.click_add_button(OverloadList.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Overload add:
    # ------------------------------------------------------------------------------------------------------------------
    overload_add = OverloadAdd(driver)
    overload_add.element_visible(OverloadAdd.header)
    overload_add.input_name(OverloadAdd.name_input,
                            OverloadAdd.name_elem)
    overload_add.input_product(OverloadAdd.product_input,
                               OverloadAdd.product_elem)
    overload_add.input_conditions_quantity(OverloadAdd.conditions_quantity_input,
                                           OverloadAdd.conditions_quantity)
    overload_add.input_overload_product(OverloadAdd.overload_product_input,
                                        OverloadAdd.overload_product)
    overload_add.input_overload_product_quantity(OverloadAdd.overload_product_quantity_input,
                                                 OverloadAdd.overload_product_quantity)
    overload_add.click_save_button(OverloadAdd.save_button,
                                   OverloadAdd.yes_button)
    print('click_save_button')
    # ------------------------------------------------------------------------------------------------------------------
    # Overload delete:
    # ------------------------------------------------------------------------------------------------------------------
    overload_list = OverloadList(driver)
    overload_list.element_visible(OverloadList.header)
    overload_list.click_first_elem_button(OverloadList.list_first_elem)
    overload_list.click_delete_one_button(OverloadList.delete_one_button,
                                          OverloadList.click_yes_delete_button)
    print('click_delete_one_button')
    # ------------------------------------------------------------------------------------------------------------------
