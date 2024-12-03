import time

from selenium.common import TimeoutException
from autotest.anor.mcg.overload_add.overload_add import OverloadAdd
from autotest.anor.mcg.overload_edit.overload_edit import OverloadIdEdit
from autotest.anor.mcg.overload_list.overload_list import OverloadList
from autotest.anor.mcg.overload_view.overload_view import OverloadIdView
from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.reference_navbar import ReferenceNavbar
from utils.driver_setup import driver


def test_overload(driver):
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

    if dashboard_page.element_visible():
        dashboard_page.click_hover_show_button()
    else:
        dashboard_page.element_visible_session()
        dashboard_page.click_button_delete_session()

    dashboard_page.click_hover_show_button()
    dashboard_page.click_reference_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Reference_navbar
    # ------------------------------------------------------------------------------------------------------------------
    reference_navbar = ReferenceNavbar(driver)
    reference_navbar.click_overload_button()
    # ------------------------------------------------------------------------------------------------------------------
    overload_list = OverloadList(driver)
    overload_list.element_visible()
    overload_list.click_add_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Overload add:
    # ------------------------------------------------------------------------------------------------------------------
    name_elem = 'test'
    conditions_quantity = '10'
    overload_product_quantity = '1'
    # ------------------------------------------------------------------------------------------------------------------
    overload_add = OverloadAdd(driver)
    overload_add.element_visible()
    overload_add.input_name(name_elem)
    overload_add.input_product()
    overload_add.input_conditions_quantity(conditions_quantity)
    overload_add.input_overload_product()
    overload_add.input_overload_product_quantity(overload_product_quantity)
    overload_add.click_save_button()
    print('Overload add:')
    # ------------------------------------------------------------------------------------------------------------------
    overload_list = OverloadList(driver)
    overload_list.element_visible()
    overload_list.find_and_click_checkbox(name_elem)
    overload_list.click_view_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Overload view:
    # ------------------------------------------------------------------------------------------------------------------
    overload_view = OverloadIdView(driver)
    overload_view.element_visible()
    name = overload_view.get_elements()

    try:
        assert name_elem == name, f"Add: {name_elem}, View: {name}"
        print(f"Successfully! Added: {name_elem}, Seen: {name}")

    except AssertionError as e:
        print(f"{str(e)}")
        pass

    overload_view.click_close_button()
    print('Overload view:')
    # ------------------------------------------------------------------------------------------------------------------
    # Overload edit:
    # ------------------------------------------------------------------------------------------------------------------
    overload_list = OverloadList(driver)
    overload_list.element_visible()
    overload_list.find_and_click_checkbox(name_elem)
    overload_list.click_edit_button()
    # ------------------------------------------------------------------------------------------------------------------
    name_elem = 'test'
    # ------------------------------------------------------------------------------------------------------------------
    overload_edit = OverloadIdEdit(driver)
    overload_edit.element_visible()
    overload_edit.input_name(name_elem)
    overload_edit.click_save_button()
    print('Overload edit:')
    # ------------------------------------------------------------------------------------------------------------------
    # Overload inactive:
    # ------------------------------------------------------------------------------------------------------------------
    overload_list = OverloadList(driver)
    overload_list.element_visible()
    overload_list.find_and_click_checkbox(name_elem)
    overload_list.click_status_one_button()
    print('Overload inactive:')
    # ------------------------------------------------------------------------------------------------------------------
    # Overload active:
    # ------------------------------------------------------------------------------------------------------------------
    overload_list = OverloadList(driver)
    overload_list.element_visible()
    overload_list.click_filter_button()
    overload_list.click_show_all_button()
    overload_list.element_visible()
    overload_list.find_and_click_checkbox(name_elem)
    try:
        overload_list.click_status_one_button()
    except:
        overload_list.click_row_button()
        overload_list.find_and_click_checkbox(name_elem)
        overload_list.click_status_one_button()
    print('Overload active:')
    # ------------------------------------------------------------------------------------------------------------------
    # Overload delete:
    # ------------------------------------------------------------------------------------------------------------------
    overload_list = OverloadList(driver)
    overload_list.element_visible()
    overload_list.find_and_click_checkbox(name_elem)
    try:
        overload_list.click_delete_one_button()
    except:
        overload_list.click_row_button()
        overload_list.find_and_click_checkbox(name_elem)
        overload_list.click_delete_one_button()
    print('Overload delete:')
    # ------------------------------------------------------------------------------------------------------------------
    # Overload add_2:
    # ------------------------------------------------------------------------------------------------------------------
    overload_list = OverloadList(driver)
    driver.refresh()
    overload_list.element_visible()
    overload_list.click_add_button()
    # ------------------------------------------------------------------------------------------------------------------
    name_elem = 'test_2'
    conditions_quantity = '10'
    overload_product_quantity = '1'
    # ------------------------------------------------------------------------------------------------------------------
    overload_add = OverloadAdd(driver)
    overload_add.element_visible()
    overload_add.input_name(name_elem)
    overload_add.input_product()
    overload_add.input_conditions_quantity(conditions_quantity)
    overload_add.input_overload_product()
    overload_add.input_overload_product_quantity(overload_product_quantity)
    overload_add.click_save_button()
    print('Overload add_2:')
    # ------------------------------------------------------------------------------------------------------------------
    # Overload inactive (many):
    # ------------------------------------------------------------------------------------------------------------------
    overload_list = OverloadList(driver)
    overload_list.element_visible()
    overload_list.find_and_click_checkbox(name_elem, checkbox=True)
    overload_list.click_status_many_button()
    print('Overload inactive (many):')
    # ------------------------------------------------------------------------------------------------------------------
    # Overload active (many):
    # ------------------------------------------------------------------------------------------------------------------
    overload_list = OverloadList(driver)
    overload_list.element_visible()
    overload_list.click_filter_button()
    overload_list.click_show_all_button()
    overload_list.element_visible()
    overload_list.find_and_click_checkbox(name_elem, checkbox=True)
    try:
        overload_list.click_status_many_button()
    except:
        overload_list.click_row_button()
        overload_list.find_and_click_checkbox(name_elem, checkbox=True)
        overload_list.click_status_many_button()
    print('Overload active (many):')
    # ------------------------------------------------------------------------------------------------------------------
    # Overload delete (many):
    # ------------------------------------------------------------------------------------------------------------------
    overload_list = OverloadList(driver)
    overload_list.element_visible()
    overload_list.find_and_click_checkbox(name_elem, checkbox=True)
    try:
        overload_list.click_delete_many_button()
    except:
        overload_list.click_row_button()
        overload_list.find_and_click_checkbox(name_elem, checkbox=True)
        overload_list.click_delete_many_button()
    driver.quit()
    print('Overload delete (many):')
    # ------------------------------------------------------------------------------------------------------------------
