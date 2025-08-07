import random

import pytest

from autotest.anor.mkr.expense_article_add.expense_article_add import ExpenseArticleAdd
from autotest.anor.mkw.extra_cost_add.extra_cost_add import ExtraCostAdd
from autotest.anor.mkw.input.input_add.input_add import InputAdd
from autotest.anor.mkw.input.input_list.input_list import InputList
from autotest.anor.mkw.input.input_view.input_view import InputView
from autotest.core.md.base_page import BasePage
from flows.auth_flow import login_user

@pytest.mark.regression
@pytest.mark.order(64)
def test_add_input(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)

    # Log
    data = test_data["data"]
    warehouse_name = data["warehouse_name"]
    purchase_quantity = 10

    login_user(driver, test_data, url='anor/mkw/input/input_list')

    # InputList
    input_list = InputList(driver)
    input_list.element_visible()
    input_list.click_add_button()

    # InputAdd
    input_add = InputAdd(driver)
    input_add.element_visible()
    input_number = random.randint(1000000, 9999999)
    save_data("input_number_1", input_number)
    input_add.input_number(input_number)
    input_add.input_warehouse(warehouse_name)
    input_add.click_next_step()

    input_add.element_visible()
    purchase_number = load_data("purchase_number_1")
    assert purchase_number is not None, f"{purchase_number} not found!"
    input_add.input_purchase(purchase_number)
    input_add.input_quantity(purchase_quantity)
    input_add.click_next_step()

    input_add.element_visible()
    input_add.click_next_step(save=True)

    # InputList
    input_list.element_visible()
    input_list.find_row(input_number)
    input_list.click_view_button()

    # InputView
    input_add = InputView(driver)
    input_add.element_visible()
    get_input_number = input_add.check_input_number()
    assert get_input_number == input_number, f"Error: {get_input_number} != {input_number}"
    input_add.click_close_button()

    # InputList
    input_list.element_visible()
    input_list.find_row(input_number)
    input_list.click_change_status_button()

    # InputList
    input_list.element_visible()
    input_list.find_row(input_number)

    # Check transactions
    base_page.switch_window(direction="prepare")
    input_list.click_transactions_button()
    base_page.switch_window(direction="forward")
    input_list.check_transaction_body(timeout=20)
    base_page.switch_window(direction="back")

    # InputList
    input_list.element_visible()

    # Check report
    base_page.switch_window(direction="prepare")
    input_list.click_report_button()
    base_page.switch_window(direction="forward")
    input_list.check_report_body(timeout=20)
    base_page.switch_window(direction="back")

    # InputList
    input_list.element_visible()

@pytest.mark.regression
@pytest.mark.order(65)
def test_add_input_with_extra_cost(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)

    # Log
    data = test_data["data"]
    warehouse_name = data["warehouse_name"]
    purchase_quantity = 10
    expense_article_name = data["expense_article_name"]
    corr_template_name = "Долг поставщикам"
    extra_cost_amount = data["product_price"] / 1.2

    login_user(driver, test_data, url='anor/mkw/input/input_list')

    # InputList
    input_list = InputList(driver)
    input_list.element_visible()
    input_list.click_add_button()

    # InputAdd
    input_add = InputAdd(driver)
    input_add.element_visible()
    input_number = random.randint(1000000, 9999999)
    save_data("input_number_2", input_number)
    input_add.input_number(input_number)
    input_add.input_warehouse(warehouse_name)
    input_add.click_extra_cost_checkbox()
    input_add.click_next_step()

    input_add.element_visible()
    purchase_number = load_data("purchase_number_2")
    assert purchase_number is not None, f"{purchase_number} not found!"
    input_add.input_purchase(purchase_number)
    input_add.input_quantity(purchase_quantity)
    input_add.click_next_step()

    input_add.element_visible()
    input_add.input_extra_cost()

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
    extra_cost_add.click_affects_the_price_checkbox(method="V")
    extra_cost_add.click_save_button(post=True)

    input_add.element_visible()
    input_add.click_distribute_extra_cost_button()
    input_add.click_next_step()

    input_add.element_visible()
    input_add.click_next_step(save=True)

    # InputList
    input_list.element_visible()
    input_list.find_row(input_number)
    input_list.click_view_button()

    # InputView
    input_add = InputView(driver)
    input_add.element_visible()
    get_input_number = input_add.check_input_number()
    assert get_input_number == input_number, f"Error: {get_input_number} != {input_number}"
    input_add.click_close_button()

    # InputList
    input_list.element_visible()
    input_list.find_row(input_number)
    input_list.click_change_status_button()

    # InputList
    input_list.element_visible()
    input_list.find_row(input_number)

    # Check transactions
    base_page.switch_window(direction="prepare")
    input_list.click_transactions_button()
    base_page.switch_window(direction="forward")
    input_list.check_transaction_body(timeout=20)
    base_page.switch_window(direction="back")

    # InputList
    input_list.element_visible()

    # Check report
    base_page.switch_window(direction="prepare")
    input_list.click_report_button()
    base_page.switch_window(direction="forward")
    input_list.check_report_body(timeout=20)
    base_page.switch_window(direction="back")

    # InputList
    input_list.element_visible()