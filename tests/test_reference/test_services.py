import time
from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.anor.mr.product.service_list.service_list import ServicesList
from autotest.anor.mr.product.service_add.service_add import ServiceAdd
from autotest.anor.mr.product.service_view.product_id import ProductIdView
from autotest.anor.mr.product.service_edit.product_id import ProductIdEdit
from autotest.trade.intro.dashboard.reference_navbar import ReferenceNavbar
from utils.driver_setup import driver


def test_services(driver):
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
    reference_navbar.element_visible(ReferenceNavbar.reference_navbar_header)
    reference_navbar.click_button_services(ReferenceNavbar.services_button)
    # ------------------------------------------------------------------------------------------------------------------
    # List
    # ------------------------------------------------------------------------------------------------------------------
    list = ServicesList(driver)
    time.sleep(2)
    list.element_visible(ServicesList.list_header)
    list.click_add_button(ServicesList.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Add
    # ------------------------------------------------------------------------------------------------------------------
    order = "1"
    name = "add_1"
    # ------------------------------------------------------------------------------------------------------------------
    add = ServiceAdd(driver)
    time.sleep(2)
    add.element_visible(ServiceAdd.header)
    add.input_name(ServiceAdd.name_input, name)
    add.input_measurement(ServiceAdd.measure_input,
                          ServiceAdd.measure_elem)
    add.input_order(ServiceAdd.order_input, order)
    add.click_save_button(ServiceAdd.save_button)
    print('Price: Add')
    # ------------------------------------------------------------------------------------------------------------------
    # View
    # ------------------------------------------------------------------------------------------------------------------
    list = ServicesList(driver)
    time.sleep(2)
    list.element_visible(ServicesList.list_header)
    list.click_first_elem_button(ServicesList.list_first_elem)
    list.click_view_button(ServicesList.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    view = ProductIdView(driver)
    view.element_visible(ProductIdView.card_title_header)
    view.click_close_button(ProductIdView.close_button)
    print('Price: View')
    # ------------------------------------------------------------------------------------------------------------------
    # Edit
    # ------------------------------------------------------------------------------------------------------------------
    list = ServicesList(driver)
    time.sleep(2)
    list.element_visible(ServicesList.list_header)
    list.click_first_elem_button(ServicesList.list_first_elem)
    list.click_edit_button(ServicesList.edit_button)
    # ------------------------------------------------------------------------------------------------------------------
    name_text = "add_1_edit"
    # ------------------------------------------------------------------------------------------------------------------
    edit = ProductIdEdit(driver)
    time.sleep(2)
    edit.element_visible(ProductIdEdit.card_title_header)
    edit.input_name_edit(ProductIdEdit.name_input, name_text)
    edit.click_save_button(ProductIdEdit.save_button)
    print('Price: Edit')
    # ------------------------------------------------------------------------------------------------------------------
    # Status (inactive)
    # ------------------------------------------------------------------------------------------------------------------
    list = ServicesList(driver)
    time.sleep(2)
    list.element_visible(ServicesList.list_header)
    list.click_first_elem_button(ServicesList.list_first_elem)
    list.click_status_one_button(ServicesList.status_one_button,
                                 ServicesList.click_yes_button)
    driver.refresh()
    list.click_filter_button(ServicesList.filter_button)
    list.click_show_all_button(ServicesList.show_all_button,
                               ServicesList.show_all_header)
    print('Price: inactive')
    # ------------------------------------------------------------------------------------------------------------------
    # Status (active)
    # ------------------------------------------------------------------------------------------------------------------
    list = ServicesList(driver)
    time.sleep(2)
    list.element_visible(ServicesList.list_header)
    list.click_first_elem_button(ServicesList.list_first_elem)
    list.click_status_one_button(ServicesList.status_one_button,
                                 ServicesList.click_yes_button)
    # driver.refresh()
    print('Price: active')
    # ------------------------------------------------------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------------------------------------------------------
    list = ServicesList(driver)
    time.sleep(2)
    list.element_visible(ServicesList.list_header)
    list.click_first_elem_button(ServicesList.list_first_elem)
    list.click_delete_one_button(ServicesList.product_delete_one_button,
                                 ServicesList.click_yes_delete_button)
    print('Price: Delete')
    # ------------------------------------------------------------------------------------------------------------------
    # Add-2
    # ------------------------------------------------------------------------------------------------------------------
    list = ServicesList(driver)
    time.sleep(2)
    list.element_visible(ServicesList.list_header)
    list.click_add_button(ServicesList.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    order = "1"
    name = "add_2"
    # ------------------------------------------------------------------------------------------------------------------
    add = ServiceAdd(driver)
    time.sleep(2)
    add.element_visible(ServiceAdd.header)
    add.input_name(ServiceAdd.name_input, name)
    add.input_measurement(ServiceAdd.measure_input,
                          ServiceAdd.measure_elem)
    add.input_order(ServiceAdd.order_input, order)
    add.click_save_button(ServiceAdd.save_button)
    print('Price: Add-2')
    # ------------------------------------------------------------------------------------------------------------------
    # Status (inactive) (many)
    # ------------------------------------------------------------------------------------------------------------------
    list = ServicesList(driver)
    time.sleep(2)
    list.element_visible(ServicesList.list_header)
    list.click_checkbox_button(ServicesList.checkbox_button)
    list.click_status_many_button(ServicesList.status_many_button,
                                  ServicesList.passive_many_button,
                                  ServicesList.status_yes_button)
    driver.refresh()
    list.click_filter_button(ServicesList.filter_button)
    list.click_show_all_button(ServicesList.show_all_button,
                               ServicesList.show_all_header)
    print('Price: inactive (many)')
    # ------------------------------------------------------------------------------------------------------------------
    # Status (active) (many)
    # ------------------------------------------------------------------------------------------------------------------
    list = ServicesList(driver)
    time.sleep(2)
    list.element_visible(ServicesList.list_header)
    list.click_checkbox_button(ServicesList.checkbox_button)
    list.click_status_many_button(ServicesList.status_many_button,
                                  ServicesList.passive_many_button,
                                  ServicesList.status_yes_button)
    # driver.refresh()
    print('Price: active (many)')
    # ------------------------------------------------------------------------------------------------------------------
    # Delete (many)
    # ------------------------------------------------------------------------------------------------------------------
    list = ServicesList(driver)
    time.sleep(2)
    list.element_visible(ServicesList.list_header)
    list.click_checkbox_button(ServicesList.checkbox_button)
    list.click_delete_many_button(ServicesList.delete_many_button,
                                  ServicesList.delete_yes_button)
    driver.close()
    print('Price: Delete (many)')
    # ------------------------------------------------------------------------------------------------------------------
