import time

from autotest.core.md.login_page import LoginPage
from autotest.trade.intro.dashboard.dashboard_page import DashboardPage
from autotest.trade.intro.dashboard.warehouse_modal import WarehouseModal
from autotest.anor.mkw.purchase.purchase_list.purchase_list import PurchaseList
from autotest.anor.mkw.purchase.purchase_add.main_page import MainPage

from utils.driver_setup import driver


def test_purchase(driver):

    # Login_page
    login_page = LoginPage(driver)
    time.sleep(2)
    login_page.fill_form(LoginPage.email, LoginPage.password, LoginPage.email_xpath, LoginPage.password_xpath)
    login_page.click_button(LoginPage.signup_xpath)

    # Dashboard_page
    dashboard_page = DashboardPage(driver)
    time.sleep(2)
    dashboard_page.element_visible(dashboard_page.dashboard_header_xpath)
    dashboard_page.click_warehouse_button(dashboard_page.warehouse_button_xpath)

    # Warehouse_modal
    warehouse_modal = WarehouseModal(driver)
    time.sleep(2)
    warehouse_modal.element_visible(warehouse_modal.warehouse_modal_header_xpath)
    warehouse_modal.click_button(WarehouseModal.purchases_button_xpath)

    # Purchase_list
    purchase_list = PurchaseList(driver)
    time.sleep(2)
    purchase_list.element_visible(PurchaseList.purchase_list_header_xpath)
    purchase_list.click_button(PurchaseList.create_button_xpath)

    # Purchase_add
    purchase_add = MainPage(driver)
    purchase_add.element_visible(MainPage.main_page_header_xpath)
    purchase_add.fill_form(MainPage.vendor, MainPage.vendor_elem_xpath)
    purchase_add.click_button(MainPage.main_page_next_button_xpath)
