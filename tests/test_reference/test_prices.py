import time
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
    # email = 'admin@test'
    # password = 'greenwhite'
    # ------------------------------------------------------------------------------------------------------------------
    login_page = LoginPage(driver)
    login_page.fill_form(email, password,
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
    dashboard_page.click_reference_button(dashboard_page.reference_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Reference_navbar
    # ------------------------------------------------------------------------------------------------------------------
    reference_navbar = ReferenceNavbar(driver)
    time.sleep(2)
    reference_navbar.element_visible(ReferenceNavbar.header)
    reference_navbar.click_button_prices(ReferenceNavbar.prices_button)
    # ------------------------------------------------------------------------------------------------------------------
    # List
    # ------------------------------------------------------------------------------------------------------------------
    list = PriceTypeList(driver)
    time.sleep(2)
    list.element_visible(PriceTypeList.list_header)
    list.click_add_button(PriceTypeList.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Add
    # ------------------------------------------------------------------------------------------------------------------
    code = "1"
    name = "add_1"
    # ------------------------------------------------------------------------------------------------------------------
    add = PriceTypeAdd(driver)
    time.sleep(2)
    add.element_visible(PriceTypeAdd.header)
    add.input_code(PriceTypeAdd.code_input, code)
    add.input_name(PriceTypeAdd.name_input, name)
    add.input_currency_name(PriceTypeAdd.currency_name_input,
                            PriceTypeAdd.currency_name)
    add.click_save_button(PriceTypeAdd.save_button)
    print('Price: Add')
    # ------------------------------------------------------------------------------------------------------------------
    # View
    # ------------------------------------------------------------------------------------------------------------------
    time.sleep(2)
    list.element_visible(PriceTypeList.list_header)
    list.click_code_button(PriceTypeList.code_button)
    list.click_first_elem_button(PriceTypeList.list_first_elem)
    list.click_view_button(PriceTypeList.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    view = PriceTypeIdView(driver)
    view.element_visible(PriceTypeIdView.card_title_header)
    view.click_close_button(PriceTypeIdView.close_button)
    print('Price: View')
    # ------------------------------------------------------------------------------------------------------------------
    # Edit
    # ------------------------------------------------------------------------------------------------------------------
    time.sleep(2)
    list.element_visible(PriceTypeList.list_header)
    list.click_first_elem_button(PriceTypeList.list_first_elem)
    list.click_edit_button(PriceTypeList.edit_button)
    # ------------------------------------------------------------------------------------------------------------------
    name_text = "add_1_edit"
    # ------------------------------------------------------------------------------------------------------------------
    edit = PriceTypeIdEdit(driver)
    time.sleep(2)
    edit.element_visible(PriceTypeIdEdit.card_title_header)
    edit.input_name_edit(PriceTypeIdEdit.name_input, name_text)
    edit.click_save_button(PriceTypeIdEdit.save_button)
    print('Price: Edit')
    # ------------------------------------------------------------------------------------------------------------------
    # Status (inactive)
    # ------------------------------------------------------------------------------------------------------------------
    time.sleep(2)
    list.element_visible(PriceTypeList.list_header)
    list.click_first_elem_button(PriceTypeList.list_first_elem)
    list.click_status_one_button(PriceTypeList.status_one_button,
                                 PriceTypeList.click_yes_button)
    driver.refresh()
    list.click_filter_button(PriceTypeList.filter_button)
    list.click_show_all_button(PriceTypeList.show_all_button)
    print('Price: inactive')
    # ------------------------------------------------------------------------------------------------------------------
    # Status (active)
    # ------------------------------------------------------------------------------------------------------------------
    time.sleep(2)
    list.element_visible(PriceTypeList.list_header)
    list.click_code_button(PriceTypeList.code_button)
    list.click_first_elem_button(PriceTypeList.list_first_elem)
    list.click_status_one_button(PriceTypeList.status_one_button,
                                 PriceTypeList.click_yes_button)
    print('Price: active')
    # ------------------------------------------------------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------------------------------------------------------
    time.sleep(2)
    list.element_visible(PriceTypeList.list_header)
    list.click_first_elem_button(PriceTypeList.list_first_elem)
    list.click_delete_one_button(PriceTypeList.product_delete_one_button,
                                 PriceTypeList.click_yes_delete_button)
    print('Price: Delete')
    # ------------------------------------------------------------------------------------------------------------------
    # Add-2
    # ------------------------------------------------------------------------------------------------------------------
    time.sleep(2)
    list.element_visible(PriceTypeList.list_header)
    list.click_add_button(PriceTypeList.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    code = "1"
    name = "add_2"
    # ------------------------------------------------------------------------------------------------------------------
    driver.refresh()
    time.sleep(1)
    add.element_visible(PriceTypeAdd.header)
    add.input_code(PriceTypeAdd.code_input, code)
    add.input_name(PriceTypeAdd.name_input, name)
    add.input_currency_name(PriceTypeAdd.currency_name_input,
                            PriceTypeAdd.currency_name)
    add.click_save_button(PriceTypeAdd.save_button)
    print('Price: Add-2')
    # ------------------------------------------------------------------------------------------------------------------
    # Status (inactive) (many)
    # ------------------------------------------------------------------------------------------------------------------
    time.sleep(2)
    list.element_visible(PriceTypeList.list_header)
    list.click_code_button(PriceTypeList.code_button)
    list.click_checkbox_button(PriceTypeList.checkbox_button)
    list.click_status_many_button(PriceTypeList.status_many_button,
                                  PriceTypeList.passive_many_button,
                                  PriceTypeList.click_status_yes_button)
    driver.refresh()
    list.click_filter_button(PriceTypeList.filter_button)
    list.click_show_all_button(PriceTypeList.show_all_button)
    print('Price: inactive (many)')
    # ------------------------------------------------------------------------------------------------------------------
    # Status (active) (many)
    # ------------------------------------------------------------------------------------------------------------------
    list.element_visible(PriceTypeList.list_header)
    list.click_code_button(PriceTypeList.code_button)
    list.click_checkbox_button(PriceTypeList.checkbox_button)
    list.click_status_many_button(PriceTypeList.status_many_button,
                                  PriceTypeList.passive_many_button,
                                  PriceTypeList.click_status_yes_button)
    print('Price: active (many)')
    # ------------------------------------------------------------------------------------------------------------------
    # Delete (many)
    # ------------------------------------------------------------------------------------------------------------------
    driver.refresh()
    list.element_visible(PriceTypeList.list_header)
    list.click_code_button(PriceTypeList.code_button)
    list.click_checkbox_button(PriceTypeList.checkbox_button)
    list.click_delete_many_button(PriceTypeList.delete_many_button,
                                  PriceTypeList.click_delete_yes_button)
    driver.close()
    print('Price: Delete (many)')
    # ------------------------------------------------------------------------------------------------------------------
