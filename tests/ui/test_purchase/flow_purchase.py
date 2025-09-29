from pages.anor.mkw.purchase_add.purchase_add import PurchaseAdd
from pages.anor.mkw.purchase_list.purchase_list import PurchaseList
from pages.anor.mkw.purchase_view.purchase_view import PurchaseView
from pages.core.md.base_page import BasePage

# ======================================================================================================================

def list_flow(driver, **kwargs):
    purchase_list = PurchaseList(driver)
    purchase_list.element_visible()

    if kwargs.get("add"):
        purchase_list.click_add_button()

    if kwargs.get("reload"):
        purchase_list.click_reload_button()

    if kwargs.get("find_row"):
        purchase_list.find_row(purchase_number=kwargs.get("find_row"))

    if kwargs.get("view"):
        purchase_list.click_view_button()

    if kwargs.get("post"):
        purchase_list.click_post_button()

# ======================================================================================================================

def add_flow(driver, **kwargs):
    purchase_add = PurchaseAdd(driver)
    purchase_add.element_visible()

    if kwargs.get("supplier_name"):
        purchase_add.input_supplier(supplier_name=kwargs.get("supplier_name"))

    if kwargs.get("extra_cost_checkbox"):
        purchase_add.click_extra_cost_checkbox()

    if kwargs.get("input_extra_cost"):
        purchase_add.input_extra_cost()

    if kwargs.get("calc_extra_cost"):
        purchase_add.click_calc_extra_cost_button()

    if kwargs.get("product_name"):
        purchase_add.input_product(product_name=kwargs.get("product_name"))

    if kwargs.get("product_quantity"):
        purchase_add.input_quantity(product_quantity=kwargs.get("product_quantity"))

    if kwargs.get("product_price"):
        purchase_add.input_price(product_price=kwargs.get("product_price"))

    if kwargs.get("purchase_number"):
        purchase_add.input_purchase_number(purchase_number=kwargs.get("purchase_number"))

    if kwargs.get("next_step", True):
        purchase_add.click_next_step_button(save_button=kwargs.get("save", False))

# ======================================================================================================================

def view_flow(driver, **kwargs):
    purchase_view = PurchaseView(driver)
    purchase_view.element_visible()

    if kwargs.get("close", True):
        purchase_view.click_close_button()

# ======================================================================================================================

def check_transaction(driver):
    base_page = BasePage(driver)
    purchase_list = PurchaseList(driver)

    base_page.switch_window(direction="prepare")
    purchase_list.click_transactions_button()
    base_page.switch_window(direction="forward")
    purchase_list.check_transaction_body(timeout=20)
    base_page.switch_window(direction="back")

# ======================================================================================================================

def check_report(driver):
    base_page = BasePage(driver)
    purchase_list = PurchaseList(driver)

    base_page.switch_window(direction="prepare")
    purchase_list.click_report_button()
    base_page.switch_window(direction="forward")
    purchase_list.check_report_body(timeout=20)
    base_page.switch_window(direction="back")

# ======================================================================================================================
