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
    dashboard_page.click_reference_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Reference_navbar
    # ------------------------------------------------------------------------------------------------------------------
    reference_navbar = ReferenceNavbar(driver)
    reference_navbar.element_visible()
    reference_navbar.click_button_inventories()
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    inventory_list.element_visible()
    inventory_list.click_add_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_new --- (Add product)
    # ------------------------------------------------------------------------------------------------------------------
    name_elem = "test"
    product_order = "1"
    # ------------------------------------------------------------------------------------------------------------------
    inventory_new = InventoryNew(driver)
    inventory_new.element_visible()
    inventory_new.input_name(name_elem)
    inventory_new.input_measurement()
    inventory_new.click_goods_checkbox()
    inventory_new.click_product_checkbox()
    inventory_new.input_order(product_order)
    inventory_new.click_save_button()
    print('product add')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (View product)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    inventory_list.element_visible()
    inventory_list.find_and_click_checkbox(name_elem)
    inventory_list.click_view_button()
    # ------------------------------------------------------------------------------------------------------------------
    product_id = ProductView(driver)
    product_id.element_visible()
    get_name = product_id.get_elements()

    try:
        assert name_elem == get_name, f"Add: {name_elem}, View: {get_name}"
        print(f"Successfully! Added: {name_elem}, Seen: {get_name}")
    except AssertionError as e:
        print(f"{str(e)}")
        raise

    product_id.click_close_button()
    print('product view')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (Edit product)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    inventory_list.element_visible()
    inventory_list.find_and_click_checkbox(name_elem)
    inventory_list.click_edit_button()
    # ------------------------------------------------------------------------------------------------------------------
    name_text = "test"
    # ------------------------------------------------------------------------------------------------------------------
    product_id = ProductEdit(driver)
    product_id.element_visible()
    product_id.input_name_edit(name_text)
    product_id.click_save_button()
    print('product edit')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (Inactive product)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    inventory_list.element_visible()
    inventory_list.find_and_click_checkbox(name_text)
    inventory_list.click_status_one_button()
    print('product no_active')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (Filter product)
    # ------------------------------------------------------------------------------------------------------------------
    product_filter = InventoryList(driver)
    driver.refresh()
    product_filter.click_filter_button()
    product_filter.click_show_all_button()
    print('product status show all')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (Active product)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    inventory_list.element_visible()
    inventory_list.find_and_click_checkbox(name_text)
    inventory_list.click_status_one_button()
    print('product active')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (Delete product)
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    inventory_list.element_visible()
    inventory_list.find_and_click_checkbox(name_text)
    inventory_list.click_delete_one_button()
    print('product delete')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    driver.refresh()
    inventory_list.element_visible()
    inventory_list.click_add_button()
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (Add product (many))
    # ------------------------------------------------------------------------------------------------------------------
    name_elem = "test"
    product_order = "1"
    # ------------------------------------------------------------------------------------------------------------------
    inventory_new = InventoryNew(driver)
    inventory_new.element_visible()
    inventory_new.input_name(name_elem)
    inventory_new.input_measurement()
    inventory_new.click_goods_checkbox()
    inventory_new.click_product_checkbox()
    inventory_new.input_order(product_order)
    inventory_new.click_save_button()
    print('product add')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (No-active product (many))
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    inventory_list.element_visible()
    inventory_list.find_and_click_checkbox(name_elem, checkbox=True)
    inventory_list.click_status_many_button()
    print('product no-active (many)')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (Filter product (many))
    # ------------------------------------------------------------------------------------------------------------------
    product_filter = InventoryList(driver)
    product_filter.click_filter_button()
    product_filter.click_show_all_button()
    print('product status show all (many)')
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    inventory_list.element_visible()
    inventory_list.find_and_click_checkbox(name_elem, checkbox=True)
    inventory_list.click_status_many_button()
    print('product active (many)')
    # ------------------------------------------------------------------------------------------------------------------
    # Inventory_list --- (Delete product (many))
    # ------------------------------------------------------------------------------------------------------------------
    inventory_list = InventoryList(driver)
    inventory_list.element_visible()
    inventory_list.find_and_click_checkbox(name_elem, checkbox=True)
    inventory_list.click_delete_many_button()
    print('product delete (many)')
    # ------------------------------------------------------------------------------------------------------------------
