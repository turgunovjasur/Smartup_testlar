import os
import time
import pytest
from flows.auth_flow import login_admin
from pages.anor.mr.template_list.template_list import TemplateList
from pages.biruni.ker.setting_add.setting_add import SettingAdd
from pages.biruni.ker.template_role_list.template_role_list import TemplateRoleList

# ======================================================================================================================

def get_data_file_path(filename, folder, subfolder):
    """
    Test fayli joylashgan katalogdan nisbiy yo‘l orqali faylning to‘liq pathini qaytaradi.
    Funksiya har doim test bilan bir joyda bo'lsin!
    """
    current_file_dir = os.path.dirname(os.path.abspath(__file__))

    # Smartup_testlar/data ni qidirish
    while True:
        potential_path = os.path.join(current_file_dir, folder, subfolder, filename)
        if os.path.isfile(potential_path):
            return potential_path

        # Bir katalog yuqoriga chiqamiz
        parent_dir = os.path.dirname(current_file_dir)
        if parent_dir == current_file_dir:
            break  # Root katalogga chiqib ketdi
        current_file_dir = parent_dir

    raise FileNotFoundError(f"{folder}/{subfolder}/{filename} not found")

# ======================================================================================================================

@pytest.mark.regression
@pytest.mark.order_group_D
@pytest.mark.order(440)
def test_add_template_for_order_invoice_report(driver, test_data):
    data = test_data["data"]
    template_name = data["template_name"]
    role_name = data["role_name"]
    form_name = 'Накладная (заказ)'
    filename = "test_invoice_report.xlsx"
    folder = "Smartup_testlar"
    subfolder = "data"

    login_admin(driver, test_data, url='anor/mr/template_list')

    template_list = TemplateList(driver)
    template_list.element_visible()
    template_list.click_add_button()

    setting_add = SettingAdd(driver)
    setting_add.element_visible()
    setting_add.input_form_name(form_name)
    setting_add.input_template_name(template_name)
    # setting_add.click_template_input()

    report_path = get_data_file_path(filename, folder, subfolder)
    setting_add.upload_template_file(file_path=report_path)

    time.sleep(2)
    # pyautogui.write(os.path.dirname(report_path), interval=0.2)
    # pyautogui.press('enter')
    # time.sleep(2)
    # pyautogui.write("test_invoice_report.xlsx", interval=0.2)
    # pyautogui.press('enter')

    setting_add.click_save_button()

    template_list.element_visible()
    template_list.find_row(template_name)
    template_list.click_attach_role_button()
    template_list.click_detach_role_button()

    template_role_list = TemplateRoleList(driver)
    template_role_list.element_visible()
    template_role_list.find_row(role_name)
    template_role_list.click_attach_button()
    template_role_list.click_close_button()
    template_list.element_visible()

# ======================================================================================================================
