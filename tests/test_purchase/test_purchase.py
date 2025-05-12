import random
import time

import pytest
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
from utils.driver_setup import driver
from tests.conftest import test_data, save_data, load_data


def test_add_purchase(driver, test_data, save_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️Test run: test_add_purchase")

    # Log
    data = test_data["data"]
    supplier_name = data["supplier_name"]
    product_name = data["product_name"]
    product_quantity = 10
    product_price = data["product_price"]

    login_user(driver, test_data, url='anor/mkw/purchase/purchase_list')

    # List
    purchase_list = PurchaseList(driver)
    assert purchase_list.element_visible(), "PurchaseList not open!"
    purchase_list.click_add_button()

    # Add
    purchase_add = PurchaseAdd(driver)
    assert purchase_add.element_visible(), "PurchaseAdd not open!"
    purchase_add.input_supplier(supplier_name)
    purchase_add.click_next_step_button()

    # Add: 2
    assert purchase_add.element_visible(), "PurchaseAdd not open after main!"
    purchase_add.input_product(product_name)
    purchase_add.input_quantity(product_quantity)
    purchase_add.input_price(product_price)
    purchase_add.click_next_step_button()

    # Add: 3
    assert purchase_add.element_visible(), "PurchaseAdd not open after product!"
    purchase_number = random.randint(1000000, 99999999)
    save_data("purchase_number", purchase_number)
    purchase_add.input_purchase_number(purchase_number)
    purchase_add.click_next_step_button(save_button=True)

    # List
    assert purchase_list.element_visible(), "PurchaseList not open after save!"
    purchase_list.click_reload_button()
    purchase_list.find_row(purchase_number)
    purchase_list.click_view_button()

    # View
    purchase_view = PurchaseView(driver)
    assert purchase_view.element_visible(), "PurchaseView not open!"
    purchase_view.click_close_button()

    # List
    assert purchase_list.element_visible(), "PurchaseList not open after view!"
    purchase_list.find_row(purchase_number)
    purchase_list.click_post_button()

    # List
    assert purchase_list.element_visible(), "PurchaseList not open after post!"

    base_page.logger.info(f"✅Test end: test_add_purchase successfully!")


def test_add_extra_cost(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️Test run: test_add_extra_cost")

    # Log
    data = test_data["data"]
    expense_article_name = data["expense_article_name"]
    corr_template_name = "Долг поставщикам"
    extra_cost_amount = data["product_price"] / 1.2
    option_name = "note"

    login_user(driver, test_data, url='anor/mkw/extra_cost_list')

    # List
    extra_cost_list = ExtraCostList(driver)
    assert extra_cost_list.element_visible(), "ExtraCostList not open!"
    extra_cost_list.click_add_button()

    # Add
    extra_cost_add = ExtraCostAdd(driver)
    assert extra_cost_add.element_visible(), "ExtraCostAdd not open!"

    if not extra_cost_add.input_articles():
        # ExpenseArticleAdd
        expense_article_add = ExpenseArticleAdd(driver)
        assert expense_article_add.element_visible(), "ExpenseArticleAdd not open!"
        expense_article_add.input_name(expense_article_name)
        expense_article_add.click_save_button()
        assert extra_cost_add.element_visible(), "ExtraCostAdd not open after ExpenseArticleAdd!"

    extra_cost_add.input_corr_templates(corr_template_name)
    extra_cost_add.input_amount(extra_cost_amount)

    note_text = random.randint(10000, 99999)
    save_data("note_text", note_text)
    extra_cost_add.input_note(note_text)
    extra_cost_add.click_save_button()

    # List
    assert extra_cost_list.element_visible(), "ExtraCostList not open!"

    note_text = load_data("note_text")
    assert note_text is not None, "note_text not found in JSON!"

    if not extra_cost_list.find_row(note_text):
        test_grid_setting_(driver, test_data, option_name)
        assert extra_cost_list.element_visible(), "ExtraCostList not open after grid_setting!"
        base_page.refresh_page()
        extra_cost_list.find_row(note_text)

    extra_cost_list.click_view_button()

    # View
    extra_cost_view = ExtraCostView(driver)
    assert extra_cost_view.element_visible(), "ExtraCostView not open!"
    extra_cost_view.click_close_button()

    assert extra_cost_list.element_visible(), "ExtraCostList not open after view!"
    extra_cost_list.find_row(note_text)
    extra_cost_list.click_post_one_button()

    # List
    assert extra_cost_list.element_visible(), "ExtraCostList not open after post!"
    extra_cost_list.find_row(note_text)
    extra_cost_list.click_separate_button()

    # ExtraCostSharing
    extra_cost_sharing = ExtraCostSharing(driver)
    assert extra_cost_sharing.element_visible(), "ExtraCostSharing not open!"
    purchase_number = load_data("purchase_number")
    assert purchase_number is not None, "purchase_number not found!"
    extra_cost_sharing.input_purchases(purchase_number)
    extra_cost_sharing.click_select_items_button()
    extra_cost_sharing.click_close_modal_button()
    extra_cost_sharing.click_separate_button()
    extra_cost_sharing.click_post_button()

    # List
    assert extra_cost_list.element_visible(), "ExtraCostList not open after ExtraCostSharing!"
    extra_cost_list.find_row(note_text)

    # Check transaction Purchase
    cut_url = base_page.cut_url()
    # base_page.open_new_window(cut_url + 'anor/mkw/purchase/purchase_list')
    base_page.switch_window(direction="new", url=cut_url + 'anor/mkw/purchase/purchase_list')

    # List
    purchase_list = PurchaseList(driver)
    assert purchase_list.element_visible(), "PurchaseList not open!"
    purchase_list.find_row(purchase_number)
    purchase_list.click_transactions_button()

    # Check transactions
    base_page.switch_window(direction="forward")
    get_amount = purchase_list.get_extra_cost_amount()
    assert get_amount == extra_cost_amount, f"{get_amount} != {extra_cost_amount}"
    base_page.switch_window(direction="back")

    # List
    assert purchase_list.element_visible(), "PurchaseList not open after check transaction!"
    base_page.logger.info(f"✅Test end: test_add_extra_cost successfully!")


def test_add_purchase_with_extra_cost_sum(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️Test run: test_add_purchase_with_extra_cost_sum")

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
    assert purchase_list.element_visible(), "PurchaseList not open!"
    purchase_list.click_add_button()

    # Add
    purchase_add = PurchaseAdd(driver)
    assert purchase_add.element_visible(), "PurchaseAdd not open!"
    purchase_add.input_supplier(supplier_name)
    purchase_add.click_checkbox()
    purchase_add.click_next_step_button()

    # Add: 2
    assert purchase_add.element_visible(), "PurchaseAdd not open after main!"
    purchase_add.input_product(product_name)
    purchase_add.input_quantity(product_quantity)
    purchase_add.input_price(product_price)
    purchase_add.click_next_step_button()

    # Add: 3
    assert purchase_add.element_visible(), "PurchaseAdd not open after product!"
    purchase_add.input_extra_cost()

    # Add Extra Cost
    extra_cost_add = ExtraCostAdd(driver)
    assert extra_cost_add.element_visible(), "ExtraCostAdd not open!"

    if not extra_cost_add.input_articles():
        # ExpenseArticleAdd
        expense_article_add = ExpenseArticleAdd(driver)
        assert expense_article_add.element_visible(), "ExpenseArticleAdd not open!"
        expense_article_add.input_name(expense_article_name)
        expense_article_add.click_save_button()
        assert extra_cost_add.element_visible(), "ExtraCostAdd not open after ExpenseArticleAdd!"

    extra_cost_add.input_corr_templates(corr_template_name)
    extra_cost_add.input_amount(extra_cost_amount)

    note_text = random.randint(10000, 99999)
    save_data("note_text_2", note_text)
    extra_cost_add.input_note(note_text)
    extra_cost_add.click_price_checkbox()
    extra_cost_add.click_save_button(post=True)

    # Add: 3
    assert purchase_add.element_visible(), "PurchaseAdd not open after ExtraCostAdd!"
    purchase_add.click_calc_extra_cost_button()
    purchase_add.click_next_step_button()

    # Add: 4
    assert purchase_add.element_visible(), "PurchaseAdd not open after Calc Extra Cost!"
    purchase_number = random.randint(1000000, 99999999)
    save_data("purchase_number_2", purchase_number)
    purchase_add.input_purchase_number(purchase_number)
    purchase_add.click_next_step_button(save_button=True)

    # List
    assert purchase_list.element_visible(), "PurchaseList not open after save!"
    purchase_list.click_reload_button()
    purchase_number = load_data("purchase_number_2")
    assert purchase_number is not None, "purchase_number_2 not found!"
    purchase_list.find_row(purchase_number)
    purchase_list.click_view_button()

    # View
    purchase_view = PurchaseView(driver)
    assert purchase_view.element_visible(), "PurchaseView not open!"
    purchase_view.click_close_button()

    # List
    assert purchase_list.element_visible(), "PurchaseList not open after view!"
    purchase_list.find_row(purchase_number)
    purchase_list.click_post_button()

    # List
    assert purchase_list.element_visible(), "PurchaseList not open after post!"
    purchase_list.find_row(purchase_number)
    purchase_list.click_transactions_button()

    # Check transactions
    base_page.switch_window(direction="forward")
    get_amount = purchase_list.get_extra_cost_amount()
    assert get_amount == extra_cost_amount, f"{get_amount} != {extra_cost_amount}"
    base_page.switch_window(direction="back")

    # List
    assert purchase_list.element_visible(), "PurchaseList not open after check transaction!"
    purchase_list.click_report_button()
    # time.sleep(2)

    # Check report
    print(driver.current_url)
    base_page.switch_window(direction="forward")
    print(driver.current_url)

    get_amount_rep = purchase_list.get_extra_cost_total_amount_for_report()
    total_amount = (product_quantity * product_price) + extra_cost_amount
    assert get_amount_rep == total_amount, f"{get_amount_rep} != {total_amount}"
    base_page.switch_window(direction="back")

    # List
    assert purchase_list.element_visible(), "PurchaseList not open after check report!"

    base_page.logger.info(f"✅Test end: test_add_purchase_with_extra_cost_sum")


def test_add_purchase_with_extra_cost_quantity(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️Test run: test_add_purchase_with_extra_cost_quantity")

    # Log
    data = test_data["data"]
    supplier_name = data["supplier_name"]
    product_name = data["product_name"]
    product_name_2 = data["product_name_2"]
    expense_article_name = data["expense_article_name"]
    corr_template_name = "Долг поставщикам"

    product_quantity_1 = 20
    product_quantity_2 = 100

    product_price = data["product_price"]  # 12_000
    extra_cost_amount = product_price * 10  # 120_000

    login_user(driver, test_data, url='anor/mkw/purchase/purchase_list')

    # List
    purchase_list = PurchaseList(driver)
    assert purchase_list.element_visible(), "PurchaseList not open!"
    purchase_list.click_add_button()

    # Add
    purchase_add = PurchaseAdd(driver)
    assert purchase_add.element_visible(), "PurchaseAdd not open!"
    purchase_add.input_supplier(supplier_name)
    purchase_add.click_checkbox()
    purchase_add.click_next_step_button()

    # Add: 2
    assert purchase_add.element_visible(), "PurchaseAdd not open after main!"
    purchase_add.input_product(product_name)
    purchase_add.input_quantity(product_quantity_1)
    purchase_add.input_price(product_price)

    purchase_add.input_product(product_name_2)
    purchase_add.input_quantity(product_quantity_2)
    purchase_add.input_price(product_price)

    purchase_add.click_next_step_button()
    time.sleep(2)

    # Add: 3
    assert purchase_add.element_visible(), "PurchaseAdd not open after product!"
    purchase_add.input_extra_cost()

    # Add Extra Cost
    extra_cost_add = ExtraCostAdd(driver)
    assert extra_cost_add.element_visible(), "ExtraCostAdd not open!"

    if not extra_cost_add.input_articles():
        # ExpenseArticleAdd
        expense_article_add = ExpenseArticleAdd(driver)
        assert expense_article_add.element_visible(), "ExpenseArticleAdd not open!"
        expense_article_add.input_name(expense_article_name)
        expense_article_add.click_save_button()
        assert extra_cost_add.element_visible(), "ExtraCostAdd not open after ExpenseArticleAdd!"

    extra_cost_add.input_corr_templates(corr_template_name)
    extra_cost_add.input_amount(extra_cost_amount)

    note_text = random.randint(10000, 99999)
    save_data("note_text_2", note_text)
    extra_cost_add.input_note(note_text)
    extra_cost_add.click_price_checkbox(method="Q")
    extra_cost_add.click_save_button(post=True)

    # Add: 3
    assert purchase_add.element_visible(), "PurchaseAdd not open after ExtraCostAdd!"
    purchase_add.click_calc_extra_cost_button()
    purchase_add.click_next_step_button()

    # Add: 4
    assert purchase_add.element_visible(), "PurchaseAdd not open after Calc Extra Cost!"
    purchase_number = random.randint(1000000, 99999999)
    save_data("purchase_number_2", purchase_number)
    purchase_add.input_purchase_number(purchase_number)
    purchase_add.click_next_step_button(save_button=True)

    # List
    assert purchase_list.element_visible(), "PurchaseList not open after save!"
    purchase_list.click_reload_button()
    purchase_number = load_data("purchase_number_2")
    assert purchase_number is not None, "purchase_number_2 not found!"
    purchase_list.find_row(purchase_number)
    purchase_list.click_view_button()

    # View
    purchase_view = PurchaseView(driver)
    assert purchase_view.element_visible(), "PurchaseView not open!"
    purchase_view.click_close_button()

    # List
    assert purchase_list.element_visible(), "PurchaseList not open after view!"
    purchase_list.find_row(purchase_number)
    purchase_list.click_report_button()
    time.sleep(2)

    # Check report
    base_page.switch_window(direction="forward")

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

    get_extra_cost_amount_rep_1 = purchase_list.get_extra_cost_amount_for_report(product_name)
    get_extra_cost_amount_rep_2 = purchase_list.get_extra_cost_amount_for_report(product_name_2)
    get_extra_cost_total_amount = purchase_list.get_extra_cost_total_amount_for_report()

    assert get_extra_cost_amount_rep_1 == final_amount_1, f"{get_extra_cost_amount_rep_1} != {final_amount_1}"
    assert get_extra_cost_amount_rep_2 == final_amount_2, f"{get_extra_cost_amount_rep_2} != {final_amount_2}"
    assert get_extra_cost_total_amount == get_extra_cost_amount_rep_1 + get_extra_cost_amount_rep_2, \
        f"{get_extra_cost_total_amount} != {get_extra_cost_amount_rep_1} + {get_extra_cost_amount_rep_2}"

    base_page.switch_window(direction="back")

    # List
    assert purchase_list.element_visible(), "PurchaseList not open after check report!"

    base_page.logger.info(f"✅Test end: test_add_purchase_with_extra_cost_quantity")


def test_add_purchase_with_extra_cost_weight_brutto(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️Test run: test_add_purchase_with_extra_cost_weight_brutto")

    # Log
    data = test_data["data"]
    supplier_name = data["supplier_name"]
    product_name = data["product_name"]
    product_name_2 = data["product_name_2"]
    expense_article_name = data["expense_article_name"]
    corr_template_name = "Долг поставщикам"

    product_quantity_1 = 10
    product_quantity_2 = 10

    product_price = data["product_price"]  # 12_000
    extra_cost_amount = product_price * 10  # 120_000

    login_user(driver, test_data, url='anor/mkw/purchase/purchase_list')

    # List
    purchase_list = PurchaseList(driver)
    assert purchase_list.element_visible(), "PurchaseList not open!"
    purchase_list.click_add_button()

    # Add
    purchase_add = PurchaseAdd(driver)
    assert purchase_add.element_visible(), "PurchaseAdd not open!"
    purchase_add.input_supplier(supplier_name)
    purchase_add.click_checkbox()
    purchase_add.click_next_step_button()

    # Add: 2
    assert purchase_add.element_visible(), "PurchaseAdd not open after main!"
    purchase_add.input_product(product_name)
    purchase_add.input_quantity(product_quantity_1)
    purchase_add.input_price(product_price)

    purchase_add.input_product(product_name_2)
    purchase_add.input_quantity(product_quantity_2)
    purchase_add.input_price(product_price)

    purchase_add.click_next_step_button()
    time.sleep(2)

    # Add: 3
    assert purchase_add.element_visible(), "PurchaseAdd not open after product!"
    purchase_add.input_extra_cost()

    # Add Extra Cost
    extra_cost_add = ExtraCostAdd(driver)
    assert extra_cost_add.element_visible(), "ExtraCostAdd not open!"

    if not extra_cost_add.input_articles():
        # ExpenseArticleAdd
        expense_article_add = ExpenseArticleAdd(driver)
        assert expense_article_add.element_visible(), "ExpenseArticleAdd not open!"
        expense_article_add.input_name(expense_article_name)
        expense_article_add.click_save_button()
        assert extra_cost_add.element_visible(), "ExtraCostAdd not open after ExpenseArticleAdd!"

    extra_cost_add.input_corr_templates(corr_template_name)
    extra_cost_add.input_amount(extra_cost_amount)

    note_text = random.randint(10000, 99999)
    save_data("note_text_2", note_text)
    extra_cost_add.input_note(note_text)
    extra_cost_add.click_price_checkbox(method="Q")
    extra_cost_add.click_save_button(post=True)

    # Add: 3
    assert purchase_add.element_visible(), "PurchaseAdd not open after ExtraCostAdd!"
    purchase_add.click_calc_extra_cost_button()
    purchase_add.click_next_step_button()

    # Add: 4
    assert purchase_add.element_visible(), "PurchaseAdd not open after Calc Extra Cost!"
    purchase_number = random.randint(1000000, 99999999)
    save_data("purchase_number_2", purchase_number)
    purchase_add.input_purchase_number(purchase_number)
    purchase_add.click_next_step_button(save_button=True)

    # List
    assert purchase_list.element_visible(), "PurchaseList not open after save!"
    purchase_list.click_reload_button()
    purchase_number = load_data("purchase_number_2")
    assert purchase_number is not None, "purchase_number_2 not found!"
    purchase_list.find_row(purchase_number)
    purchase_list.click_view_button()

    # View
    purchase_view = PurchaseView(driver)
    assert purchase_view.element_visible(), "PurchaseView not open!"
    purchase_view.click_close_button()

    # List
    assert purchase_list.element_visible(), "PurchaseList not open after view!"
    purchase_list.find_row(purchase_number)
    purchase_list.click_report_button()
    time.sleep(2)

    # Check report
    base_page.switch_window(direction="forward")

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

    get_extra_cost_amount_rep_1 = purchase_list.get_extra_cost_amount_for_report(product_name)
    get_extra_cost_amount_rep_2 = purchase_list.get_extra_cost_amount_for_report(product_name_2)
    get_extra_cost_total_amount = purchase_list.get_extra_cost_total_amount_for_report()

    assert get_extra_cost_amount_rep_1 == final_amount_1, f"{get_extra_cost_amount_rep_1} != {final_amount_1}"
    assert get_extra_cost_amount_rep_2 == final_amount_2, f"{get_extra_cost_amount_rep_2} != {final_amount_2}"
    assert get_extra_cost_total_amount == get_extra_cost_amount_rep_1 + get_extra_cost_amount_rep_2, \
        f"{get_extra_cost_total_amount} != {get_extra_cost_amount_rep_1} + {get_extra_cost_amount_rep_2}"

    base_page.switch_window(direction="back")

    # List
    assert purchase_list.element_visible(), "PurchaseList not open after check report!"

    base_page.logger.info(f"✅Test end: test_add_purchase_with_extra_cost_weight_brutto")