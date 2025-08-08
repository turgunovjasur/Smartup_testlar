from autotest.anor.mkw.balance.balance_list.balance_detail import BalanceDetail
from autotest.anor.mkw.balance.balance_list.balance_list import BalanceList
from autotest.core.md.base_page import BasePage


def flow_get_balance(driver, **kwargs):
    warehouse_name = kwargs.get("warehouse_name")
    product_name = kwargs.get("product_name")
    detail = kwargs.get("detail")

    base_page = BasePage(driver)
    base_page.switch_window(direction="prepare")
    cut_url = base_page.cut_url()
    base_page.switch_window(direction="new", url=cut_url + 'anor/mkw/balance/balance_list')

    balance_list = BalanceList(driver)
    balance_list.element_visible()
    balance_list.click_reload_button()
    get_balance = balance_list.get_balance(warehouse_name, product_name)
    base_page.logger.info(f"Warehouse: '{warehouse_name}' | Product: '{product_name}' | Balance: {get_balance}")

    if detail:
        balance_list.find_row(product_name, warehouse_name)
        balance_list.click_detail_button()

        balance_detail = BalanceDetail(driver)
        balance_detail.element_visible()
        balance_detail.click_reload_button()
        balance_detail.find_row(product_name, warehouse_name)
        balance_detail.click_close_button()

    base_page.switch_window(direction="prepare")
    base_page.switch_window(direction="back")
    return get_balance
