from pages.anor.mkr.expense_article_add.expense_article_add import ExpenseArticleAdd
from pages.anor.mkw.extra_cost_add.extra_cost_add import ExtraCostAdd
from pages.anor.mkw.extra_cost_list.extra_cost_list import ExtraCostList
from pages.anor.mkw.extra_cost_sharing.extra_cost_sharing import ExtraCostSharing
from pages.anor.mkw.extra_cost_view.extra_cost_view import ExtraCostView
from pages.core.md.base_page import BasePage
from flows.grid_setting_flow import grid_setting

# ======================================================================================================================

def list_flow(driver, **kwargs):
    extra_cost_list = ExtraCostList(driver)
    extra_cost_list.element_visible()

    if kwargs.get("add"):
        extra_cost_list.click_add_button()

    if kwargs.get("find_row"):
        if not extra_cost_list.find_row(note_text=kwargs.get("find_row")):
            base_page = BasePage(driver)
            grid_setting(driver, option_name=kwargs.get("option_name"))
            extra_cost_list.element_visible()
            base_page.refresh_page()
            extra_cost_list.find_row(note_text=kwargs.get("find_row"))

    if kwargs.get("view"):
        extra_cost_list.click_view_button()

    if kwargs.get("post"):
        extra_cost_list.click_post_one_button()

    if kwargs.get("separate"):
        extra_cost_list.click_separate_button()

# ======================================================================================================================

def add_flow(driver, **kwargs):
    extra_cost_add = ExtraCostAdd(driver)
    extra_cost_add.element_visible()

    if kwargs.get("expense_article_name"):
        if not extra_cost_add.input_articles():
            expense_article_add = ExpenseArticleAdd(driver)
            expense_article_add.element_visible()
            expense_article_add.input_name(kwargs.get("expense_article_name"))
            expense_article_add.click_save_button()
            extra_cost_add.element_visible()

    if kwargs.get("corr_template_name"):
        extra_cost_add.input_corr_templates(kwargs.get("corr_template_name"))

    if kwargs.get("extra_cost_amount"):
        extra_cost_add.input_amount(kwargs.get("extra_cost_amount"))

    if kwargs.get("note_text"):
        extra_cost_add.input_note(kwargs.get("note_text"))

    method = kwargs.get("method", None)
    if method or kwargs.get("affects_the_price_checkbox"):
        extra_cost_add.click_affects_the_price_checkbox(method=method)

    if kwargs.get("save", True):
        extra_cost_add.click_save_button(post=kwargs.get("post", False))

# ======================================================================================================================

def view_flow(driver, **kwargs):
    extra_cost_view = ExtraCostView(driver)
    extra_cost_view.element_visible()

    if kwargs.get("save", True):
        extra_cost_view.click_close_button()

# ======================================================================================================================

def extra_cost_sharing_flow(driver, **kwargs):
    extra_cost_sharing = ExtraCostSharing(driver)
    extra_cost_sharing.element_visible()

    extra_cost_sharing.input_purchases(purchase_number=kwargs.get("purchase_number"))
    extra_cost_sharing.click_select_items_button()
    extra_cost_sharing.click_close_modal_button()
    extra_cost_sharing.click_separate_button()
    extra_cost_sharing.click_post_button()

# ======================================================================================================================
