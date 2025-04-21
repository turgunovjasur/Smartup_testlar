import os
import random
import time
import pytest
from autotest.core.md.base_page import BasePage
from autotest.trade.rep.integration.cislink.cislink import CisLink
from tests.test_base.test_base import login_user
from utils.driver_setup import driver
from tests.conftest import test_data


def test_check_report_cis_link(driver, test_data):
    base_page = BasePage(driver)
    base_page.logger.info("▶️ Run test: test_check_report_cislink")

    try:
        login_user(driver, test_data, url='trade/rep/integration/cislink')

        # CisLink
        cis_link = CisLink(driver)
        assert cis_link.element_visible(), "CisLink not open!"
        cis_link.click_show_setting()

        # Setting
        assert cis_link.element_visible_setting(), "CisLink Setting not open!"
        cis_link.click_save()

        # CisLink
        assert cis_link.element_visible(), "CisLink not open after setting!"
        cis_link.click_generate()
        time.sleep(3)
        integer = random.randint(10000, 99999)
        file_name = f"cislink_{integer}"
        cis_link.input_file_name_windows(file_name)
        cis_link.click_enter_windows()

        time.sleep(5)
        downloads_path = os.path.join(os.environ["USERPROFILE"], "Downloads")

        # Yuklangan fayllarni olish va tekshirish
        files = os.listdir(downloads_path)
        files = [os.path.join(downloads_path, f) for f in files if f.endswith(f'{file_name}.zip')]
        files.sort(key=os.path.getctime, reverse=True)

        latest_file = files[0] if files else None
        assert latest_file is not None, "❌ cisLink.zip file not download!"

        file_name = os.path.basename(latest_file)

        base_page.logger.info(f"✅ Loaded filename: {file_name}")
        base_page.logger.info(f"✅Test end: test_check_report_cis_link successfully!")

    except AssertionError as ae:
        base_page.logger.error(f'Assertion error: {str(ae)}')
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))
    except Exception as e:
        pytest.fail(str(e))
