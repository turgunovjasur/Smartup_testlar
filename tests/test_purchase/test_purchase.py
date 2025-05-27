import random
import time
from autotest.anor.mkr.expense_article_add.expense_article_add import ExpenseArticleAdd
from autotest.anor.mkw.extra_cost_add.extra_cost_add import ExtraCostAdd
from autotest.anor.mkw.extra_cost_list.extra_cost_list import ExtraCostList
from autotest.anor.mkw.extra_cost_sharing.extra_cost_sharing import ExtraCostSharing
from autotest.anor.mkw.extra_cost_view.extra_cost_view import ExtraCostView
from autotest.anor.mkw.purchase_add.purchase_add import PurchaseAdd
from autotest.anor.mkw.purchase_list.purchase_list import PurchaseList
from autotest.anor.mkw.purchase_view.purchase_view import PurchaseView
from autotest.core.md.base_page import BasePage
from tests.test_base.test_base import login_user, test_grid_setting_
from tests.conftest import driver, test_data, save_data, load_data


def add_purchase(driver, test_data, save_data, save_purchase_number):
    base_page = BasePage(driver)

    # Log
    data = test_data["data"]
    supplier_name = data["supplier_name"]
    product_name = data["product_name"]
    product_quantity = 10
    product_price = data["product_price"]

    login_user(driver, test_data, url='anor/mkw/purchase/purchase_list')

    # List
    purchase_list = PurchaseList(driver)
    purchase_list.element_visible()
    purchase_list.click_add_button()

    # Add
    purchase_add = PurchaseAdd(driver)
    purchase_add.element_visible()
    purchase_add.input_supplier(supplier_name)
    purchase_add.click_next_step_button()

    # Add: 2
    purchase_add.element_visible()
    purchase_add.input_product(product_name)
    purchase_add.input_quantity(product_quantity)
    purchase_add.input_price(product_price)
    purchase_add.click_next_step_button()

    # Add: 3
    purchase_add.element_visible()
    purchase_number = random.randint(1000000, 99999999)
    save_data(save_purchase_number, purchase_number)
    purchase_add.input_purchase_number(purchase_number)
    purchase_add.click_next_step_button(save_button=True)

    # List
    purchase_list.element_visible()
    purchase_list.click_reload_button()
    purchase_list.find_row(purchase_number)
    purchase_list.click_view_button()

    # View
    purchase_view = PurchaseView(driver)
    purchase_view.element_visible()
    purchase_view.click_close_button()

    # List
    purchase_list.element_visible()
    purchase_list.find_row(purchase_number)
    purchase_list.click_post_button()

    # List
    purchase_list.element_visible()
    purchase_list.find_row(purchase_number)

    # Check transactions
    base_page.switch_window(direction="prepare")
    purchase_list.click_transactions_button()
    base_page.switch_window(direction="forward")
    purchase_list.check_transaction_body(timeout=20)
    base_page.switch_window(direction="back")

    # List
    purchase_list.element_visible()

    # Check report
    base_page.switch_window(direction="prepare")
    purchase_list.click_report_button()
    base_page.switch_window(direction="forward")
    purchase_list.check_report_body(timeout=20)
    base_page.switch_window(direction="back")

    # List
    purchase_list.element_visible()


def test_add_purchase(driver, test_data, save_data):
    """Test adding purchase"""

    save_purchase_number = "purchase_number_1"
    add_purchase(driver, test_data, save_data, save_purchase_number)


def test_add_extra_cost(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)

    # Log
    data = test_data["data"]
    expense_article_name = data["expense_article_name"]
    corr_template_name = "Долг поставщикам"
    extra_cost_amount = data["product_price"] / 1.2
    option_name = "note"

    login_user(driver, test_data, url='anor/mkw/extra_cost_list')

    # List
    extra_cost_list = ExtraCostList(driver)
    extra_cost_list.element_visible()
    extra_cost_list.click_add_button()

    # Add
    extra_cost_add = ExtraCostAdd(driver)
    extra_cost_add.element_visible()

    if not extra_cost_add.input_articles():
        # ExpenseArticleAdd
        expense_article_add = ExpenseArticleAdd(driver)
        expense_article_add.element_visible()
        expense_article_add.input_name(expense_article_name)
        expense_article_add.click_save_button()
        extra_cost_add.element_visible()

    extra_cost_add.input_corr_templates(corr_template_name)
    extra_cost_add.input_amount(extra_cost_amount)

    note_text = random.randint(10000, 99999)
    extra_cost_add.input_note(note_text)
    extra_cost_add.click_save_button()

    # List
    extra_cost_list.element_visible()
    if not extra_cost_list.find_row(note_text):
        test_grid_setting_(driver, test_data, option_name)
        extra_cost_list.element_visible()
        base_page.refresh_page()
        extra_cost_list.find_row(note_text)
    extra_cost_list.click_view_button()

    # View
    extra_cost_view = ExtraCostView(driver)
    extra_cost_view.element_visible()
    extra_cost_view.click_close_button()

    extra_cost_list.element_visible()
    extra_cost_list.find_row(note_text)
    extra_cost_list.click_post_one_button()

    # List
    extra_cost_list.element_visible()
    extra_cost_list.find_row(note_text)
    extra_cost_list.click_separate_button()

    # ExtraCostSharing
    extra_cost_sharing = ExtraCostSharing(driver)
    extra_cost_sharing.element_visible()
    purchase_number = load_data("purchase_number_1")
    assert purchase_number is not None, f"{purchase_number} not found!"
    extra_cost_sharing.input_purchases(purchase_number)
    extra_cost_sharing.click_select_items_button()
    extra_cost_sharing.click_close_modal_button()
    extra_cost_sharing.click_separate_button()
    extra_cost_sharing.click_post_button()

    # List
    extra_cost_list.element_visible()
    extra_cost_list.find_row(note_text)

    # Check transaction and report in Purchase
    base_page.switch_window(direction="prepare")
    cut_url = base_page.cut_url()
    base_page.switch_window(direction="new", url=cut_url + 'anor/mkw/purchase/purchase_list')

    # List
    purchase_list = PurchaseList(driver)
    purchase_list.element_visible()
    purchase_list.find_row(purchase_number)

    # Check transactions
    base_page.switch_window(direction="prepare")
    purchase_list.click_transactions_button()
    base_page.switch_window(direction="forward")
    purchase_list.check_transaction_body(timeout=20)
    base_page.switch_window(direction="back")

    # List
    purchase_list.element_visible()

    # Check report
    base_page.switch_window(direction="prepare")
    purchase_list.click_report_button()
    base_page.switch_window(direction="forward")
    purchase_list.check_report_body(timeout=20)
    base_page.switch_window(direction="back")

    # List
    purchase_list.element_visible()


def test_add_purchase_with_extra_cost_sum(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)

    # Log
    data = test_data["data"]
    supplier_name = data["supplier_name"]
    product_name = data["product_name"]
    product_quantity = 10
    product_price = data["product_price"]
    expense_article_name = data["expense_article_name"]
    corr_template_name = "Долг поставщикам"
    extra_cost_amount = data["product_price"] / 1.2

    login_user(driver, test_data, url='anor/mkw/purchase/purchase_list')

    # List
    purchase_list = PurchaseList(driver)
    purchase_list.element_visible()
    purchase_list.click_add_button()

    # Add
    purchase_add = PurchaseAdd(driver)
    purchase_add.element_visible()
    purchase_add.input_supplier(supplier_name)
    purchase_add.click_checkbox()
    purchase_add.click_next_step_button()

    # Add: 2
    purchase_add.element_visible()
    purchase_add.input_product(product_name)
    purchase_add.input_quantity(product_quantity)
    purchase_add.input_price(product_price)
    purchase_add.click_next_step_button()

    # Add: 3
    purchase_add.element_visible()
    purchase_add.input_extra_cost()

    # Add Extra Cost
    extra_cost_add = ExtraCostAdd(driver)
    extra_cost_add.element_visible()
    if not extra_cost_add.input_articles():
        # ExpenseArticleAdd
        expense_article_add = ExpenseArticleAdd(driver)
        expense_article_add.element_visible()
        expense_article_add.input_name(expense_article_name)
        expense_article_add.click_save_button()
        extra_cost_add.element_visible()
    extra_cost_add.input_corr_templates(corr_template_name)
    extra_cost_add.input_amount(extra_cost_amount)

    note_text = random.randint(10000, 99999)
    extra_cost_add.input_note(note_text)
    extra_cost_add.click_price_checkbox()
    extra_cost_add.click_save_button(post=True)

    # Add: 3
    purchase_add.element_visible()
    purchase_add.click_calc_extra_cost_button()
    purchase_add.click_next_step_button()

    # Add: 4
    purchase_add.element_visible()
    purchase_number = random.randint(1000000, 99999999)
    save_data("purchase_number_2", purchase_number)
    purchase_add.input_purchase_number(purchase_number)
    purchase_add.click_next_step_button(save_button=True)

    # List
    purchase_list.element_visible()
    purchase_list.click_reload_button()
    purchase_list.find_row(purchase_number)
    purchase_list.click_view_button()

    # View
    purchase_view = PurchaseView(driver)
    purchase_view.element_visible()
    purchase_view.click_close_button()

    # List
    purchase_list.element_visible()
    purchase_list.find_row(purchase_number)
    purchase_list.click_post_button()

    # List
    purchase_list.element_visible()
    purchase_list.find_row(purchase_number)

    # Check transactions
    base_page.switch_window(direction="prepare")
    purchase_list.click_transactions_button()
    base_page.switch_window(direction="forward")
    purchase_list.check_transaction_body(timeout=20)
    base_page.switch_window(direction="back")

    # List
    purchase_list.element_visible()

    # Check report
    base_page.switch_window(direction="prepare")
    purchase_list.click_report_button()
    base_page.switch_window(direction="forward")
    purchase_list.check_report_body(timeout=20)
    base_page.switch_window(direction="back")

    # List
    purchase_list.element_visible()


def test_add_purchase_with_extra_cost_quantity(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)

    # Log
    data = test_data["data"]
    supplier_name = data["supplier_name"]
    product_name = data["product_name"]
    product_name_2 = data["product_name_2"]
    expense_article_name = data["expense_article_name"]
    corr_template_name = "Долг поставщикам"

    product_quantity_1 = 20
    product_quantity_2 = 100

    product_price = data["product_price"]   # 12_000
    extra_cost_amount = product_price * 10  # 120_000

    login_user(driver, test_data, url='anor/mkw/purchase/purchase_list')

    # List
    purchase_list = PurchaseList(driver)
    purchase_list.element_visible()
    purchase_list.click_add_button()

    # Add
    purchase_add = PurchaseAdd(driver)
    purchase_add.element_visible()
    purchase_add.input_supplier(supplier_name)
    purchase_add.click_checkbox()
    purchase_add.click_next_step_button()

    # Add: 2
    purchase_add.element_visible()
    purchase_add.input_product(product_name)
    purchase_add.input_quantity(product_quantity_1)
    purchase_add.input_price(product_price)

    purchase_add.input_product(product_name_2)
    purchase_add.input_quantity(product_quantity_2)
    purchase_add.input_price(product_price)

    purchase_add.click_next_step_button()
    time.sleep(2)

    # Add: 3
    purchase_add.element_visible()
    purchase_add.input_extra_cost()

    # Add Extra Cost
    extra_cost_add = ExtraCostAdd(driver)
    extra_cost_add.element_visible()
    if not extra_cost_add.input_articles():
        # ExpenseArticleAdd
        expense_article_add = ExpenseArticleAdd(driver)
        expense_article_add.element_visible()
        expense_article_add.input_name(expense_article_name)
        expense_article_add.click_save_button()
        extra_cost_add.element_visible()
    extra_cost_add.input_corr_templates(corr_template_name)
    extra_cost_add.input_amount(extra_cost_amount)

    note_text = random.randint(10000, 99999)
    extra_cost_add.input_note(note_text)
    extra_cost_add.click_price_checkbox(method="Q")
    extra_cost_add.click_save_button(post=True)

    # Add: 3
    purchase_add.element_visible()
    purchase_add.click_calc_extra_cost_button()
    purchase_add.click_next_step_button()

    # Add: 4
    purchase_add.element_visible()
    purchase_number = random.randint(1000000, 99999999)
    save_data("purchase_number_3", purchase_number)
    purchase_add.input_purchase_number(purchase_number)
    purchase_add.click_next_step_button(save_button=True)

    # List
    purchase_list.element_visible()
    purchase_list.click_reload_button()
    purchase_list.find_row(purchase_number)
    purchase_list.click_view_button()

    # View
    purchase_view = PurchaseView(driver)
    purchase_view.element_visible()
    purchase_view.click_close_button()

    # List
    purchase_list.element_visible()
    purchase_list.find_row(purchase_number)
    purchase_list.click_post_button()

    # List
    purchase_list.element_visible()
    purchase_list.find_row(purchase_number)

    # Check transactions
    base_page.switch_window(direction="prepare")
    purchase_list.click_transactions_button()
    base_page.switch_window(direction="forward")
    purchase_list.check_transaction_body(timeout=20)
    base_page.switch_window(direction="back")

    # List
    purchase_list.element_visible()

    # Check report
    base_page.switch_window(direction="prepare")
    purchase_list.click_report_button()
    base_page.switch_window(direction="forward")
    purchase_list.check_report_body(timeout=20)

    # Har bir mahsulotning bazaviy narxi
    purchase_amount_1 = product_quantity_1 * product_price  # 20 * 12000 = 240_000
    purchase_amount_2 = product_quantity_2 * product_price  # 100 * 12000 = 1_200_000

    # Jami purchase narxi
    total_purchase = purchase_amount_1 + purchase_amount_2  # 1_440_000

    # Har bir mahsulotga extra cost ulushini hisoblash
    extra_cost_1 = round((purchase_amount_1 / total_purchase) * extra_cost_amount)  # 20_000
    extra_cost_2 = round((purchase_amount_2 / total_purchase) * extra_cost_amount)  # 100_000

    # Yakuniy summalar (Qo‘shimcha xarajat bilan)
    final_amount_1 = purchase_amount_1 + extra_cost_1  # 260_000
    final_amount_2 = purchase_amount_2 + extra_cost_2  # 1_300_000

    get_extra_cost_amount_rep_1 = purchase_list.get_extra_cost_amount_for_report(product_name, td=7)
    get_extra_cost_amount_rep_2 = purchase_list.get_extra_cost_amount_for_report(product_name_2, td=7)
    get_extra_cost_total_amount = purchase_list.get_extra_cost_total_amount_for_report(td=5)

    assert get_extra_cost_amount_rep_1 == final_amount_1, f"{get_extra_cost_amount_rep_1} != {final_amount_1}"
    assert get_extra_cost_amount_rep_2 == final_amount_2, f"{get_extra_cost_amount_rep_2} != {final_amount_2}"
    assert get_extra_cost_total_amount == get_extra_cost_amount_rep_1 + get_extra_cost_amount_rep_2, \
        f"{get_extra_cost_total_amount} != {get_extra_cost_amount_rep_1} + {get_extra_cost_amount_rep_2}"

    base_page.switch_window(direction="back")

    # List
    purchase_list.element_visible()


def test_add_purchase_with_extra_cost_weight_brutto(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)

    # Log
    data = test_data["data"]
    supplier_name = data["supplier_name"]
    product_name = data["product_name"]
    product_name_2 = data["product_name_2"]
    expense_article_name = data["expense_article_name"]
    corr_template_name = "Долг поставщикам"

    product_quantity_1 = 10
    product_quantity_2 = 10

    product_weight_1 = data["product_weight_brutto"]    # 1_100
    product_weight_2 = data["product_weight_brutto_2"]  # 2_100

    product_price = data["product_price"]   # 12_000
    extra_cost_amount = product_price * 10  # 120_000

    login_user(driver, test_data, url='anor/mkw/purchase/purchase_list')

    # List
    purchase_list = PurchaseList(driver)
    purchase_list.element_visible()
    purchase_list.click_add_button()

    # Add
    purchase_add = PurchaseAdd(driver)
    purchase_add.element_visible()
    purchase_add.input_supplier(supplier_name)
    purchase_add.click_checkbox()
    purchase_add.click_next_step_button()

    # Add: 2
    purchase_add.element_visible()
    purchase_add.input_product(product_name)
    purchase_add.input_quantity(product_quantity_1)
    purchase_add.input_price(product_price)

    purchase_add.input_product(product_name_2)
    purchase_add.input_quantity(product_quantity_2)
    purchase_add.input_price(product_price)

    purchase_add.click_next_step_button()
    time.sleep(2)

    # Add: 3
    purchase_add.element_visible()
    purchase_add.input_extra_cost()

    # Add Extra Cost
    extra_cost_add = ExtraCostAdd(driver)
    extra_cost_add.element_visible()
    if not extra_cost_add.input_articles():
        # ExpenseArticleAdd
        expense_article_add = ExpenseArticleAdd(driver)
        expense_article_add.element_visible()
        expense_article_add.input_name(expense_article_name)
        expense_article_add.click_save_button()
        extra_cost_add.element_visible()
    extra_cost_add.input_corr_templates(corr_template_name)
    extra_cost_add.input_amount(extra_cost_amount)

    note_text = random.randint(10000, 99999)
    extra_cost_add.input_note(note_text)
    extra_cost_add.click_price_checkbox(method="W")
    extra_cost_add.click_save_button(post=True)

    # Add: 3
    purchase_add.element_visible()
    purchase_add.click_calc_extra_cost_button()
    purchase_add.click_next_step_button()

    # Add: 4
    purchase_add.element_visible()
    purchase_number = random.randint(1000000, 99999999)
    save_data("purchase_number_4", purchase_number)
    purchase_add.input_purchase_number(purchase_number)
    purchase_add.click_next_step_button(save_button=True)

    # List
    purchase_list.element_visible()
    purchase_list.click_reload_button()
    purchase_list.find_row(purchase_number)
    purchase_list.click_view_button()

    # View
    purchase_view = PurchaseView(driver)
    purchase_view.element_visible()
    purchase_view.click_close_button()

    # List
    purchase_list.element_visible()
    purchase_list.find_row(purchase_number)
    purchase_list.click_post_button()

    # List
    purchase_list.element_visible()
    purchase_list.find_row(purchase_number)

    # Check transactions
    base_page.switch_window(direction="prepare")
    purchase_list.click_transactions_button()
    base_page.switch_window(direction="forward")
    purchase_list.check_transaction_body(timeout=20)
    base_page.switch_window(direction="back")

    # List
    purchase_list.element_visible()

    # Check report
    base_page.switch_window(direction="prepare")
    purchase_list.click_report_button()
    base_page.switch_window(direction="forward")
    purchase_list.check_report_body(timeout=20)

    total_weight = product_weight_1 + product_weight_2  # 1_100 + 2_100 = 3_200

    extra_cost_1 = (product_weight_1 / total_weight) * extra_cost_amount  # (1_100 / 3_200) * 120_000 = 41_250
    extra_cost_2 = (product_weight_2 / total_weight) * extra_cost_amount  # (2_100 / 3_200) * 120_000 = 78_750

    get_extra_cost_1 = purchase_list.get_extra_cost_amount_for_report(product_name)    # 41_250
    get_extra_cost_2 = purchase_list.get_extra_cost_amount_for_report(product_name_2)  # 78_750
    get_total_amount = purchase_list.get_extra_cost_total_amount_for_report()          # 120_000

    assert get_extra_cost_1 == extra_cost_1, f"{get_extra_cost_1} != {extra_cost_1}"
    assert get_extra_cost_2 == extra_cost_2, f"{get_extra_cost_2} != {extra_cost_2}"
    assert get_total_amount == extra_cost_amount, f"{get_total_amount} != {extra_cost_amount}"

    base_page.switch_window(direction="back")

    # List
    purchase_list.element_visible()