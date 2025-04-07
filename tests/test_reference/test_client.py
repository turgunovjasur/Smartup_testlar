import pytest
from autotest.anor.mrf.client_add.client_add import ClientAdd
from autotest.anor.mrf.client_list.client_list import ClientList
from autotest.anor.mrf.client_view.client_view import ClientView
from autotest.core.md.base_page import BasePage
from tests.test_base.test_base import login_user
from utils.driver_setup import driver
from tests.conftest import test_data


def client_add(driver, test_data, client_name=None):
    """Test adding a client"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: client_add")

    # Test data
    data = test_data["data"]
    client_name = client_name or data["client_name"]

    try:
        # Login
        login_user(driver, test_data, url='anor/mrf/client_list')

        # Open Client List
        client_list = ClientList(driver)
        assert client_list.element_visible(), "ClientList not open!"
        client_list.click_add_button()

        # Add Client
        client_add = ClientAdd(driver)
        assert client_add.element_visible(), "ClientAdd not open!"
        client_add.click_radio_button()
        client_add.input_name(client_name)
        client_add.click_save_button()

        # Verify in List
        assert client_list.element_visible(), "ClientList not open after save!"
        client_list.find_row(client_name)
        client_list.click_view_button()

        # Verify in View
        client_view = ClientView(driver)
        assert client_view.element_visible(), "ClientView not open!"
        client_view.check_client_name()
        client_view.click_close_button()

        base_page.logger.info(f"✅ Client '{client_name}' added successfully!")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        base_page.take_screenshot("unexpected_error")
        pytest.fail(str(e))


def test_client_add_A(driver, test_data):
    """Test adding client A"""

    data = test_data["data"]
    client_name = f"{data['client_name']}-A"
    client_add(driver, test_data, client_name=client_name)


def test_client_add_B(driver, test_data):
    """Test adding client B"""

    data = test_data["data"]
    client_name = f"{data['client_name']}-B"
    client_add(driver, test_data, client_name=client_name)


def test_client_add_C(driver, test_data):
    """Test adding client C"""

    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    client_add(driver, test_data, client_name=client_name)