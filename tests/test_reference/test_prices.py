from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.anor.mkr.price_type_add.price_type_add import PriceTypeAdd
from autotest.anor.mkr.price_type_edit.price_type_id import PriceTypeIdEdit
from autotest.anor.mkr.price_type_list.price_type_list import PriceTypeList
from autotest.anor.mkr.price_type_view.price_type_id import PriceTypeIdView
from autotest.trade.intro.dashboard.reference_navbar import ReferenceNavbar
from utils.driver_setup import driver


def test_prices(driver):
    # ------------------------------------------------------------------------------------------------------------------
    # Login_page
    # ------------------------------------------------------------------------------------------------------------------
    email = 'admin@auto_test'
    password = 'greenwhite'
    # ------------------------------------------------------------------------------------------------------------------
    login_page = LoginPage(driver)
    login_page.fill_form(email, password)
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
    dashboard_page.click_reference_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Reference_navbar
    # ------------------------------------------------------------------------------------------------------------------
    reference_navbar = ReferenceNavbar(driver)
    reference_navbar.element_visible()
    reference_navbar.click_button_prices()
    # ------------------------------------------------------------------------------------------------------------------
    # List
    # ------------------------------------------------------------------------------------------------------------------
    list = PriceTypeList(driver)
    list.element_visible()
    list.click_add_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Add
    # ------------------------------------------------------------------------------------------------------------------
    code = "1"
    name = "add_1"
    # ------------------------------------------------------------------------------------------------------------------
    add = PriceTypeAdd(driver)
    add.element_visible()
    add.input_code(code)
    add.input_name(name)
    add.input_currency_name()
    add.click_save_button()
    print('Price: Add')
    # ------------------------------------------------------------------------------------------------------------------
    # View
    # ------------------------------------------------------------------------------------------------------------------
    list.element_visible()
    list.click_code_button()
    list.find_and_click_checkbox(name)
    list.click_view_button()
    # ------------------------------------------------------------------------------------------------------------------
    view = PriceTypeIdView(driver)
    view.element_visible()
    view.click_close_button()
    print('Price: View')
    # ------------------------------------------------------------------------------------------------------------------
    # Edit
    # ------------------------------------------------------------------------------------------------------------------
    list.element_visible()
    list.find_and_click_checkbox(name)
    list.click_edit_button()
    # ------------------------------------------------------------------------------------------------------------------
    name_text = "add_1_edit"
    # ------------------------------------------------------------------------------------------------------------------
    edit = PriceTypeIdEdit(driver)
    edit.element_visible()
    edit.input_name_edit(name_text)
    edit.click_save_button()
    print('Price: Edit')
    # ------------------------------------------------------------------------------------------------------------------
    # Status (inactive)
    # ------------------------------------------------------------------------------------------------------------------
    list.element_visible()
    list.find_and_click_checkbox(name_text)
    list.click_status_one_button()
    driver.refresh()
    list.click_filter_button()
    list.click_show_all_button()
    print('Price: inactive')
    # ------------------------------------------------------------------------------------------------------------------
    # Status (active)
    # ------------------------------------------------------------------------------------------------------------------
    list.element_visible()
    list.click_code_button()
    list.find_and_click_checkbox(name_text)
    list.click_status_one_button()
    print('Price: active')
    # ------------------------------------------------------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------------------------------------------------------
    list.element_visible()
    list.find_and_click_checkbox(name_text)
    list.click_delete_one_button()
    print('Price: Delete')
    # ------------------------------------------------------------------------------------------------------------------
    # Add-2
    # ------------------------------------------------------------------------------------------------------------------
    driver.refresh()
    list.element_visible()
    list.click_add_button()
    # ------------------------------------------------------------------------------------------------------------------
    code = "1"
    name = "add_2"
    # ------------------------------------------------------------------------------------------------------------------
    add.element_visible()
    add.input_code(code)
    add.input_name(name)
    add.input_currency_name()
    add.click_save_button()
    print('Price: Add-2')
    # ------------------------------------------------------------------------------------------------------------------
    # Status (inactive) (many)
    # ------------------------------------------------------------------------------------------------------------------
    list.element_visible()
    # list.click_code_button()
    list.find_and_click_checkbox(name, checkbox=True)
    list.click_status_many_button()
    driver.refresh()
    list.click_filter_button()
    list.click_show_all_button()
    print('Price: inactive (many)')
    # ------------------------------------------------------------------------------------------------------------------
    # Status (active) (many)
    # ------------------------------------------------------------------------------------------------------------------
    list.element_visible()
    # list.click_code_button()
    list.find_and_click_checkbox(name, checkbox=True)
    list.click_status_many_button()
    print('Price: active (many)')
    # ------------------------------------------------------------------------------------------------------------------
    # Delete (many)
    # ------------------------------------------------------------------------------------------------------------------
    driver.refresh()
    list.element_visible()
    # list.click_code_button()
    list.find_and_click_checkbox(name, checkbox=True)
    list.click_delete_many_button()
    driver.close()
    print('Price: Delete (many)')
    # ------------------------------------------------------------------------------------------------------------------
