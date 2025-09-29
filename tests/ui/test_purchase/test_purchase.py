import random
import pytest
from pages.anor.mkw.purchase_list.purchase_list import PurchaseList
from pages.core.md.base_page import BasePage
from flows.auth_flow import login_user
from tests.ui.test_purchase.flow_purchase import list_flow, add_flow, view_flow, check_transaction, check_report
from tests.ui.test_purchase.flow_extra_cost import add_flow as extra_cost_add_flow

# ======================================================================================================================

def add_purchase(driver, test_data, save_data, save_purchase_number):
    data = test_data["data"]
    supplier_name = data["supplier_name"]
    product_name = data["product_name"]
    product_quantity = 10
    product_price = data["product_price"]

    login_user(driver, test_data, url='anor/mkw/purchase/purchase_list')

    list_flow(driver, add=True)

    add_flow(driver, supplier_name=supplier_name)
    add_flow(driver, product_name=product_name, product_quantity=product_quantity, product_price=product_price)

    purchase_number = random.randint(1000000, 99999999)
    save_data(save_purchase_number, purchase_number)
    add_flow(driver, purchase_number=purchase_number, save=True)

    list_flow(driver, reload=True, find_row=purchase_number, view=True)

    view_flow(driver)

    list_flow(driver, find_row=purchase_number, post=True)
    list_flow(driver, find_row=purchase_number)

    check_transaction(driver)

    list_flow(driver)

    check_report(driver)

    list_flow(driver)

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order(560)
def test_add_purchase(driver, test_data, save_data):
    """Test adding purchase"""

    save_purchase_number = "purchase_number_1"
    add_purchase(driver, test_data, save_data, save_purchase_number)

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order(580)
def test_add_purchase_with_extra_cost_sum(driver, test_data, save_data, load_data):
    data = test_data["data"]
    supplier_name = data["supplier_name"]
    product_name = data["product_name"]
    product_quantity = 10
    product_price = data["product_price"]
    expense_article_name = data["expense_article_name"]
    corr_template_name = "Долг поставщикам"
    extra_cost_amount = data["product_price"] / 1.2

    login_user(driver, test_data, url='anor/mkw/purchase/purchase_list')

    list_flow(driver, add=True)

    # Add: 1
    add_flow(driver, supplier_name=supplier_name, extra_cost_checkbox=True)

    # Add: 2
    add_flow(driver, product_name=product_name, product_quantity=product_quantity, product_price=product_price)

    # Add: 3
    add_flow(driver, input_extra_cost=True, next_step=False)

    # Add Extra Cost
    note_text = random.randint(1000000, 99999999)
    extra_cost_add_flow(driver,
                        expense_article_name=expense_article_name,
                        corr_template_name=corr_template_name,
                        extra_cost_amount=extra_cost_amount,
                        note_text=note_text,
                        affects_the_price_checkbox=True)

    # Add: 3
    add_flow(driver, calc_extra_cost=True)

    # Add: 4
    purchase_number = random.randint(1000000, 99999999)
    save_data("purchase_number_2", purchase_number)
    add_flow(driver, purchase_number=purchase_number, save=True)

    list_flow(driver, reload=True, find_row=purchase_number, view=True)

    view_flow(driver)

    list_flow(driver, find_row=purchase_number, post=True)
    list_flow(driver, find_row=purchase_number)

    check_transaction(driver)

    list_flow(driver)

    check_report(driver)

    list_flow(driver)

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order(581)
def test_add_purchase_with_extra_cost_quantity(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)

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

    list_flow(driver, add=True)

    # Add: 1
    add_flow(driver, supplier_name=supplier_name, extra_cost_checkbox=True)

    # Add: 2
    add_flow(driver,
             product_name=product_name,
             product_quantity=product_quantity_1,
             product_price=product_price,
             next_step=False)

    add_flow(driver,
             product_name=product_name_2,
             product_quantity=product_quantity_2,
             product_price=product_price)

    # Add: 3
    add_flow(driver, input_extra_cost=True, next_step=False)

    # Add Extra Cost
    note_text = random.randint(1000000, 99999999)
    extra_cost_add_flow(driver,
                        expense_article_name=expense_article_name,
                        corr_template_name=corr_template_name,
                        extra_cost_amount=extra_cost_amount,
                        note_text=note_text,
                        method="Q",
                        post=True)

    # Add: 3
    add_flow(driver, calc_extra_cost=True)

    # Add: 4
    purchase_number = random.randint(1000000, 99999999)
    save_data("purchase_number_3", purchase_number)
    add_flow(driver, purchase_number=purchase_number, save=True)

    list_flow(driver, reload=True, find_row=purchase_number, view=True)

    view_flow(driver)

    list_flow(driver, find_row=purchase_number, post=True)
    list_flow(driver, find_row=purchase_number)

    check_transaction(driver)

    list_flow(driver)

    # Check report
    purchase_list = PurchaseList(driver)
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
    assert get_extra_cost_amount_rep_1 == final_amount_1, f"{get_extra_cost_amount_rep_1} != {final_amount_1}"

    get_extra_cost_amount_rep_2 = purchase_list.get_extra_cost_amount_for_report(product_name_2, td=7)
    assert get_extra_cost_amount_rep_2 == final_amount_2, f"{get_extra_cost_amount_rep_2} != {final_amount_2}"

    get_extra_cost_total_amount = purchase_list.get_extra_cost_total_amount_for_report(td=5)
    assert get_extra_cost_total_amount == get_extra_cost_amount_rep_1 + get_extra_cost_amount_rep_2, \
        f"{get_extra_cost_total_amount} != {get_extra_cost_amount_rep_1} + {get_extra_cost_amount_rep_2}"

    base_page.switch_window(direction="back")

    list_flow(driver)

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order(582)
def test_add_purchase_with_extra_cost_weight_brutto(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)

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

    list_flow(driver, add=True)

    # Add: 1
    add_flow(driver, supplier_name=supplier_name, extra_cost_checkbox=True)

    # Add: 2
    add_flow(driver,
             product_name=product_name,
             product_quantity=product_quantity_1,
             product_price=product_price,
             next_step=False)

    add_flow(driver,
             product_name=product_name_2,
             product_quantity=product_quantity_2,
             product_price=product_price)

    # Add: 3
    add_flow(driver, input_extra_cost=True, next_step=False)

    # Add Extra Cost
    note_text = random.randint(1000000, 99999999)
    extra_cost_add_flow(driver,
                        expense_article_name=expense_article_name,
                        corr_template_name=corr_template_name,
                        extra_cost_amount=extra_cost_amount,
                        note_text=note_text,
                        method="W",
                        post=True)

    # Add: 3
    add_flow(driver, calc_extra_cost=True)

    # Add: 4
    purchase_number = random.randint(1000000, 99999999)
    save_data("purchase_number_4", purchase_number)
    add_flow(driver, purchase_number=purchase_number, save=True)

    list_flow(driver, reload=True, find_row=purchase_number, view=True)

    view_flow(driver)

    list_flow(driver, find_row=purchase_number, post=True)
    list_flow(driver, find_row=purchase_number)

    check_transaction(driver)

    list_flow(driver)

    # Check report
    purchase_list = PurchaseList(driver)
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

    list_flow(driver)

# ======================================================================================================================
