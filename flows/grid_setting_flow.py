import time
from autotest.biruni.md.biruni.grid_setting.grid_setting import GridSetting
from autotest.biruni.md.biruni.grid_setting.grid_setting_in_form import GridSettingInForm


# ----------------------------------------------------------------------------------------------------------------------

def grid_setting(driver, option_name=None, search_type=None, save_as_default=False):
    """Test configuring grid settings."""
    # Grid Setting
    grid_setting = GridSetting(driver)
    grid_setting.click_group_button()
    grid_setting.element_visible()

    if option_name:
        grid_setting.click_options_button(option_name)
        time.sleep(0.5)

    if search_type:
        grid_setting.click_search_type_switch(search_type)
        time.sleep(0.5)

    if save_as_default:
        grid_setting.click_save_default_button()
        return

    grid_setting.click_save_button()
    time.sleep(0.5)

# ----------------------------------------------------------------------------------------------------------------------

def grid_setting_in_form(driver):
    """Test configuring grid settings in forms."""
    grid_page = GridSettingInForm(driver)
    grid_page.element_visible()
    grid_page.click_save_default_button()
    time.sleep(0.5)
# ----------------------------------------------------------------------------------------------------------------------
