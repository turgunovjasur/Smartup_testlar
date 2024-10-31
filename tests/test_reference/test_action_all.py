from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.reference_navbar import ReferenceNavbar
from autotest.anor.mcg.action_list.action_list import ActionList
from autotest.anor.mcg.action_add.action_add import ActionAdd
from autotest.anor.mcg.action_view.action_view import ActionIdView
from autotest.anor.mcg.action_edit.action_edit import ActionIdEdit
from utils.driver_setup import driver


def login(driver, email, password):
    login_page = LoginPage(driver)
    login_page.fill_form(email, password)
    login_page.click_button()


def dashboard(driver):
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
    reference_navbar = ReferenceNavbar(driver)
    reference_navbar.click_action_button()


def list(driver):
    action_list = ActionList(driver)
    action_list.element_visible()
    action_list.click_add_button()


def add(driver, name_text, end_date, tip, inventory_quantity_elem, bonus_inventory_quantity_elem):
    # Page 1
    action_add = ActionAdd(driver)
    action_add.element_visible()
    action_add.input_name(name_text)
    action_add.input_end_date(end_date)
    action_add.input_room()
    action_add.input_bonus_warehouse()
    action_add.input_tip_action(tip=tip)
    action_add.click_step_button()
    # Page 2
    action_add.input_type_condition()
    action_add.input_inventory()
    action_add.input_inventory_quantity(inventory_quantity_elem)
    action_add.input_bonus_inventory()
    action_add.input_bonus_inventory_quantity(bonus_inventory_quantity_elem)
    action_add.click_save_button()
    print('Action add:')


def view(driver, name_elem):
    action_list = ActionList(driver)
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


def edit(driver, name_elem, name_text, inventory_quantity_elem, bonus_inventory_quantity_elem):
    action_list = ActionList(driver)
    action_list.find_and_click_checkbox(name_elem)
    action_list.click_edit_button()
    # ------------------------------------------------------------------------------------------------------------------
    action_edit = ActionIdEdit(driver)
    action_edit.element_visible()
    action_edit.input_name(name_text)
    action_edit.click_step_button()
    action_edit.input_inventory_quantity(inventory_quantity_elem)
    action_edit.input_bonus_inventory_quantity(bonus_inventory_quantity_elem)
    action_edit.click_save_button()
    print('Action edit:')


def inactive(driver, name_text):
    action_list = ActionList(driver)
    action_list.find_and_click_checkbox(name_text)
    action_list.click_status_one_button()
    print('Action inactive:')


def active(driver, name_text):
    action_list = ActionList(driver)
    action_list.element_visible()
    action_list.click_filter_button()
    action_list.click_show_all_button()
    action_list.find_and_click_checkbox(name_text)
    action_list.click_status_one_button()
    print('Action active:')


def delete(driver, name_text):
    action_list = ActionList(driver)
    action_list.find_and_click_checkbox(name_text)
    action_list.click_delete_one_button()
    print('Action delete:')


def add_2(driver, name_text, end_date, tip, inventory_quantity_elem, bonus_inventory_quantity_elem):
    # Page 1
    action_add = ActionAdd(driver)
    action_add.element_visible()
    action_add.input_name(name_text)
    action_add.input_end_date(end_date)
    action_add.input_room()
    action_add.input_bonus_warehouse()
    action_add.input_tip_action(tip=tip)
    action_add.click_step_button()
    # Page 2
    action_add.input_type_condition()
    action_add.input_inventory()
    action_add.input_inventory_quantity(inventory_quantity_elem)
    action_add.input_bonus_inventory()
    action_add.input_bonus_inventory_quantity(bonus_inventory_quantity_elem)
    action_add.click_save_button()
    print('Action add:')


def inactive_many(driver, name_text):
    action_list = ActionList(driver)
    action_list.element_visible()
    action_list.find_and_click_checkbox(name_text, checkbox=True)
    action_list.click_status_many_button()
    print('Action inactive (many):')


def active_many(driver, name_text):
    action_list = ActionList(driver)
    action_list.element_visible()
    action_list.click_filter_button()
    action_list.click_show_all_button()
    action_list.click_row_button()
    action_list.find_and_click_checkbox(name_text, checkbox=True)
    action_list.click_status_many_button()
    print('Action active (many):')


def delete_many(driver, name_text):
    action_list = ActionList(driver)
    action_list.element_visible()
    action_list.find_and_click_checkbox(name_text, checkbox=True)
    action_list.click_delete_many_button()
    print('Action delete (many):')
    driver.quit()


def test_action_quant(driver):
    email = 'admin@auto_test'
    password = 'greenwhite'
    tip = 'quant'
    name_text = 'quant'
    end_date = '31.12.2024'
    inventory_quantity_elem = '10'
    bonus_inventory_quantity_elem = '1'
    # ------------------------------------------------------------------------------------------------------------------
    login(driver, email, password)
    dashboard(driver)
    list(driver)
    add(driver, name_text, end_date, tip, inventory_quantity_elem, bonus_inventory_quantity_elem)
    view(driver, name_text)
    edit(driver, name_text, name_text, inventory_quantity_elem, bonus_inventory_quantity_elem)
    inactive(driver, name_text)
    active(driver, name_text)
    delete(driver, name_text)
    # ------------------------------------------------------------------------------------------------------------------
    driver.refresh()
    list(driver)
    add(driver, name_text, end_date, tip, inventory_quantity_elem, bonus_inventory_quantity_elem)
    inactive_many(driver, name_text)
    active_many(driver, name_text)
    delete_many(driver, name_text)


def test_amount(driver):
    email = 'admin@auto_test'
    password = 'greenwhite'
    tip = 'amount'
    name_text = 'amount'
    end_date = '31.12.2024'
    inventory_quantity_elem = '10'
    bonus_inventory_quantity_elem = '1'
    # ------------------------------------------------------------------------------------------------------------------
    login(driver, email, password)
    dashboard(driver)
    list(driver)
    add(driver, name_text, end_date, tip, inventory_quantity_elem, bonus_inventory_quantity_elem)
    view(driver, name_text)
    edit(driver, name_text, name_text, inventory_quantity_elem, bonus_inventory_quantity_elem)
    inactive(driver, name_text)
    active(driver, name_text)
    delete(driver, name_text)
    # ------------------------------------------------------------------------------------------------------------------
    driver.refresh()
    list(driver)
    add_2(driver, name_text, end_date, tip, inventory_quantity_elem, bonus_inventory_quantity_elem)
    inactive_many(driver, name_text)
    active_many(driver, name_text)
    delete_many(driver, name_text)


def test_weight(driver):
    email = 'admin@auto_test'
    password = 'greenwhite'
    tip = 'weight'
    name_text = 'weight'
    end_date = '31.12.2024'
    inventory_quantity_elem = '10'
    bonus_inventory_quantity_elem = '1'
    # ------------------------------------------------------------------------------------------------------------------
    login(driver, email, password)
    dashboard(driver)
    list(driver)
    add(driver, name_text, end_date, tip, inventory_quantity_elem, bonus_inventory_quantity_elem)
    view(driver, name_text)
    edit(driver, name_text, name_text, inventory_quantity_elem, bonus_inventory_quantity_elem)
    inactive(driver, name_text)
    active(driver, name_text)
    delete(driver, name_text)
    # ------------------------------------------------------------------------------------------------------------------
    driver.refresh()
    list(driver)
    add_2(driver, name_text, end_date, tip, inventory_quantity_elem, bonus_inventory_quantity_elem)
    inactive_many(driver, name_text)
    active_many(driver, name_text)
    delete_many(driver, name_text)


def test_box_quant(driver):
    email = 'admin@auto_test'
    password = 'greenwhite'
    tip = 'box_quant'
    name_text = 'box_quant'
    end_date = '31.12.2024'
    inventory_quantity_elem = '10'
    bonus_inventory_quantity_elem = '1'
    # ------------------------------------------------------------------------------------------------------------------
    login(driver, email, password)
    dashboard(driver)
    list(driver)
    add(driver, name_text, end_date, tip, inventory_quantity_elem, bonus_inventory_quantity_elem)
    view(driver, name_text)
    edit(driver, name_text, name_text, inventory_quantity_elem, bonus_inventory_quantity_elem)
    inactive(driver, name_text)
    active(driver, name_text)
    delete(driver, name_text)
    # ------------------------------------------------------------------------------------------------------------------
    driver.refresh()
    list(driver)
    add_2(driver, name_text, end_date, tip, inventory_quantity_elem, bonus_inventory_quantity_elem)
    inactive_many(driver, name_text)
    active_many(driver, name_text)
    delete_many(driver, name_text)


def run_all_tests(driver):
    try:
        test_action_quant(driver)
        test_amount(driver)
        test_weight(driver)
        test_box_quant(driver)
    except Exception as e:
        print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    from selenium import webdriver
    driver = webdriver.Chrome()
    try:
        run_all_tests(driver)
    finally:
        driver.quit()
