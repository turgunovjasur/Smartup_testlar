"""
TEMPORARY TEST.

Dev delivery-date checkboxni default ishlaydigan qilgach, ushbu faylni o‘chirish mumkin.
SystemSetting page-objectidagi TEMPORARY DELIVERY DATE PERMISSION blokini ham o‘chiring.
"""

import pytest

from flows.auth_flow import login_user
from pages.trade.pref.system_setting.system_setting import SystemSetting


@pytest.mark.regression
@pytest.mark.order_group_C
@pytest.mark.order(390)
def test_temp_setting_delivery_date_change_permission(driver, test_data):
    """Admin roliga buyurtma jo‘natish sanasini o‘zgartirish huquqini beradi."""
    role_name = test_data["data"]["role_name"]
    access_name = "Полный доступ"

    login_user(driver, test_data, url="trade/pref/system_setting")

    system_setting = SystemSetting(driver)
    system_setting.element_visible()
    system_setting.click_navbar_button(navbar_name="Заказ")
    system_setting.element_visible_order()
    system_setting.element_visible_delivery_date_permission()

    if not system_setting.has_delivery_date_permission(role_name, access_name):
        system_setting.click_create_delivery_date_permission()
        system_setting.input_delivery_date_permission_role(role_name)
        system_setting.input_delivery_date_permission_access(access_name)
        system_setting.click_add_delivery_date_permission()
        system_setting.wait_for_delivery_date_permission(role_name, access_name)
        system_setting.click_save_button()
        system_setting.element_visible_order()
    else:
        system_setting.logger.info(
            f"Delivery date permission avvaldan mavjud: {role_name} — {access_name}"
        )

    assert system_setting.has_delivery_date_permission(role_name, access_name), (
        f"Delivery date permission saqlanmadi: {role_name} — {access_name}"
    )
