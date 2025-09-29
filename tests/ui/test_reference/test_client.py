import pytest

from pages.anor.mrf.client_add.client_add import ClientAdd
from pages.anor.mrf.client_list.client_list import ClientList
from pages.anor.mrf.client_view.client_view import ClientView
from flows.auth_flow import login_user


def client_add(driver, test_data, client_name=None):
    """Test adding a client"""
    # Test data
    data = test_data["data"]
    client_name = client_name or data["client_name"]

    # Login
    login_user(driver, test_data, url='anor/mrf/client_list')

    # Open Client List
    client_list = ClientList(driver)
    client_list.element_visible()
    client_list.click_add_button()

    # Add Client
    client_add = ClientAdd(driver)
    client_add.element_visible()
    client_add.click_radio_button()
    client_add.input_name(client_name)
    client_add.click_save_button()

    # Verify in List
    client_list.element_visible()
    client_list.find_row(client_name)
    client_list.click_view_button()

    # Verify in View
    client_view = ClientView(driver)
    client_view.element_visible()
    client_view.check_client_name()
    client_view.click_close_button()


@pytest.mark.regression
@pytest.mark.order(200)
def test_client_add_A(driver, test_data):
    """Test adding client A"""

    data = test_data["data"]
    client_name = f"{data['client_name']}-A"
    client_add(driver, test_data, client_name=client_name)


@pytest.mark.regression
@pytest.mark.order(201)
def test_client_add_B(driver, test_data):
    """Test adding client B"""

    data = test_data["data"]
    client_name = f"{data['client_name']}-B"
    client_add(driver, test_data, client_name=client_name)


@pytest.mark.regression
@pytest.mark.order(202)
def test_client_add_C(driver, test_data):
    """Test adding client C"""

    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    client_add(driver, test_data, client_name=client_name)