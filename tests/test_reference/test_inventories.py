import time
from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.reference_navbar import ReferenceNavbar
from autotest.anor.mr.product.inventory_list.inventory_list import InventoryList
from autotest.anor.mr.product.inventory_add.inventory_new import InventoryNew
from autotest.anor.mr.product.inventory_view.product_id import ProductId as ProductView
from autotest.anor.mr.product.inventory_edit.product_id import ProductId as ProductEdit
from utils.driver_setup import driver


def test_inventories(driver):
    # ------------------------------------------------------------------------------------------------------------------
    # Login_page
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
    reference_navbar.element_visible(ReferenceNavbar.reference_navbar_header)
    reference_navbar.click_button_reference(ReferenceNavbar.reference_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    inventory_list.element_visible(InventoryList.inventory_list_header)
    inventory_list.click_add_button(InventoryList.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_new --- (Add product)
    # ------------------------------------------------------------------------------------------------------------------
    name_elem = "olma_test_add"
    product_order = "1"
    # ------------------------------------------------------------------------------------------------------------------
    inventory_new = InventoryNew(driver)
    inventory_new.element_visible(InventoryNew.inventory_new_header)
    inventory_new.input_name(InventoryNew.name_input, name_elem)
    inventory_new.input_measurement(InventoryNew.measurement_input,
                                    InventoryNew.measurement_elem)
    inventory_new.click_goods_checkbox(InventoryNew.goods_checkbox)
    inventory_new.click_product_checkbox(InventoryNew.product_checkbox)
    inventory_new.input_order(InventoryNew.product_order_input, product_order)
    inventory_new.click_save_button(InventoryNew.save_button)
    print('product add')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (View product)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    time.sleep(2)
    inventory_list.element_visible(InventoryList.inventory_list_header)
    inventory_list.click_first_elem_button(InventoryList.inventory_list_first_elem)
    inventory_list.click_view_button(InventoryList.view_button)
    # ------------------------------------------------------------------------------------------------------------------
    product_id = ProductView(driver)
    time.sleep(2)
    product_id.element_visible(ProductView.card_title_header)
    # product_name = product_id.get_elements(ProductView.product_name)
    # print(f"product name: {product_name}")
    product_id.click_close_button(ProductView.close_button)
    print('product view')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (Edit product)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    time.sleep(2)
    inventory_list.element_visible(InventoryList.inventory_list_header)
    inventory_list.click_first_elem_button(InventoryList.inventory_list_first_elem)
    inventory_list.click_edit_button(InventoryList.edit_button)
    # ------------------------------------------------------------------------------------------------------------------
    name_text = "olma_test_edit"
    # ------------------------------------------------------------------------------------------------------------------
    product_id = ProductEdit(driver)
    time.sleep(2)
    product_id.element_visible(ProductEdit.card_title_header)
    product_id.input_name_edit(ProductEdit.name_input, name_text)
    product_id.click_save_button(ProductEdit.save_button)
    print('product edit')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (Inactive product)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    time.sleep(2)
    inventory_list.element_visible(InventoryList.inventory_list_header)
    inventory_list.click_first_elem_button(InventoryList.inventory_list_first_elem)
    inventory_list.click_status_one_button(InventoryList.status_one_button,
                                           InventoryList.click_yes_button)
    print('product no_active')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (Filter product)
    # ------------------------------------------------------------------------------------------------------------------
    product_filter = InventoryList(driver)
    driver.refresh()
    time.sleep(2)
    product_filter.click_filter_button(InventoryList.filter_button)
    time.sleep(2)
    product_filter.click_show_all_button(InventoryList.show_all_button)
    print('product status show all')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (Active product)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    time.sleep(2)
    inventory_list.element_visible(InventoryList.inventory_list_header)
    inventory_list.click_first_elem_button(InventoryList.inventory_list_first_elem)
    inventory_list.click_status_one_button(InventoryList.status_one_button,
                                           InventoryList.click_yes_button)
    print('product active')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (Delete product)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    time.sleep(2)
    inventory_list.element_visible(InventoryList.inventory_list_header)
    inventory_list.click_first_elem_button(InventoryList.inventory_list_first_elem)
    inventory_list.click_delete_one_button(InventoryList.product_delete_one_button,
                                           InventoryList.click_yes_delete_button)
    print('product delete')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    time.sleep(2)
    inventory_list.element_visible(InventoryList.inventory_list_header)
    inventory_list.click_add_button(InventoryList.add_button)
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (Add product (many))
    # ------------------------------------------------------------------------------------------------------------------
    name_elem = "olma_test2_add"
    product_order = "1"
    # ------------------------------------------------------------------------------------------------------------------
    inventory_new = InventoryNew(driver)
    inventory_new.element_visible(InventoryNew.inventory_new_header)
    inventory_new.input_name(InventoryNew.name_input, name_elem)
    inventory_new.input_measurement(InventoryNew.measurement_input,
                                    InventoryNew.measurement_elem)
    inventory_new.click_goods_checkbox(InventoryNew.goods_checkbox)
    inventory_new.click_product_checkbox(InventoryNew.product_checkbox)
    inventory_new.input_order(InventoryNew.product_order_input, product_order)
    inventory_new.click_save_button(InventoryNew.save_button)
    print('product add')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (No-active product (many))
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    time.sleep(2)
    inventory_list.element_visible(InventoryList.inventory_list_header)
    inventory_list.click_checkbox_button(InventoryList.checkbox_button)
    inventory_list.click_status_many_button(InventoryList.status_many_button,
                                            InventoryList.passive_many_button,
                                            InventoryList.click_status_yes_button)
    print('product no-active (many)')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (Filter product (many))
    # ------------------------------------------------------------------------------------------------------------------
    product_filter = InventoryList(driver)
    time.sleep(2)
    product_filter.click_filter_button(InventoryList.filter_button)
    time.sleep(2)
    product_filter.click_show_all_button(InventoryList.show_all_button)
    print('product status show all (many)')
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    time.sleep(2)
    inventory_list.element_visible(InventoryList.inventory_list_header)
    inventory_list.click_checkbox_button(InventoryList.checkbox_button)
    inventory_list.click_status_many_button(InventoryList.status_many_button,
                                            InventoryList.passive_many_button,
                                            InventoryList.click_status_yes_button)
    print('product active (many)')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (Delete product (many))
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    time.sleep(2)
    inventory_list.element_visible(InventoryList.inventory_list_header)
    inventory_list.click_checkbox_button(InventoryList.checkbox_button)
    inventory_list.click_delete_many_button(InventoryList.delete_many_button,
                                            InventoryList.click_delete_yes_button)
    print('product delete (many)')
    # ------------------------------------------------------------------------------------------------------------------
