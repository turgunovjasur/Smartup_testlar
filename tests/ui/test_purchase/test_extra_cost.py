import random
import pytest
from pages.core.md.base_page import BasePage
from flows.auth_flow import login_user
from tests.ui.test_purchase.flow_extra_cost import list_flow, add_flow, view_flow, extra_cost_sharing_flow
from tests.ui.test_purchase.flow_purchase import list_flow as p_list_flow, check_transaction as p_check_transaction, \
    check_report as p_check_report


@pytest.mark.regression
@pytest.mark.order(570)
def test_add_extra_cost(driver, test_data, save_data, load_data):
    base_page = BasePage(driver)

    data = test_data["data"]
    expense_article_name = data["expense_article_name"]
    corr_template_name = "Долг поставщикам"
    extra_cost_amount = data["product_price"] / 1.2
    option_name = "note"

    login_user(driver, test_data, url='anor/mkw/extra_cost_list')

    list_flow(driver, add=True)

    add_flow(driver,
             expense_article_name=expense_article_name,
             corr_template_name=corr_template_name,
             extra_cost_amount=extra_cost_amount,
             save=False)

    note_text = random.randint(1000000, 9999999)
    add_flow(driver, note_text=note_text, save=True)

    list_flow(driver, find_row=note_text, option_name=option_name, view=True)

    view_flow(driver)

    list_flow(driver, find_row=note_text, post=True)
    list_flow(driver, find_row=note_text, separate=True)
    # ------------------------------------------------------------------------------------------------------------------
    # ExtraCostSharing
    purchase_number = load_data("purchase_number_1")
    assert purchase_number is not None, f"{purchase_number} not found!"
    extra_cost_sharing_flow(driver, purchase_number=purchase_number)

    list_flow(driver, find_row=note_text)
    # ------------------------------------------------------------------------------------------------------------------
    # Check transaction and report in Purchase
    base_page.switch_window(direction="prepare")
    cut_url = base_page.cut_url()
    base_page.switch_window(direction="new", url=cut_url + 'anor/mkw/purchase/purchase_list')

    p_list_flow(driver, find_row=purchase_number)
    p_check_transaction(driver)
    p_list_flow(driver)
    p_check_report(driver)
    p_list_flow(driver)
    # ------------------------------------------------------------------------------------------------------------------
