import pytest
from autotest.anor.mr.person.natural_person_add.natural_person_add import NaturalPersonAdd
from autotest.anor.mr.person.natural_person_list.natural_person_list import NaturalPersonList
from autotest.anor.mr.person.natural_person_view.natural_person_view import NaturalPersonView
from autotest.core.md.base_page import BasePage
from tests.test_base.test_base import login_admin
from utils.driver_setup import driver
from tests.conftest import test_data

def test_natural_person_add(driver, test_data, person_name=None):
    """Test adding a natural person"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_natural_person_add")

    # Test data
    data = test_data["data"]
    filial_name = data["filial_name"]
    natural_person_name = person_name or data["natural_person_name"]

    try:
        # Login
        login_admin(driver, test_data, filial_name=filial_name, url='anor/mr/person/natural_person_list')

        # Open Natural Person List
        natural_person_list = NaturalPersonList(driver)
        assert natural_person_list.element_visible(), "NaturalPersonList not open!"
        natural_person_list.click_add_button()

        # Add Natural Person
        natural_person_add = NaturalPersonAdd(driver)
        assert natural_person_add.element_visible(), "NaturalPersonAdd not open!"
        natural_person_add.input_name(natural_person_name)
        natural_person_add.click_save_button()

        # Verify in List
        assert natural_person_list.element_visible(), "NaturalPersonList not open after save!"
        natural_person_list.find_row(natural_person_name)
        natural_person_list.click_view_button()

        # Verify in View
        natural_person_view = NaturalPersonView(driver)
        assert natural_person_view.element_visible(), "NaturalPersonView not open!"
        text = natural_person_view.check_text()
        assert text == natural_person_name, f'Expected "{natural_person_name}", got "{text}"'

        base_page.logger.info(f"✅ Natural Person '{natural_person_name}' added successfully!")

    except AssertionError as ae:
        base_page.logger.error(f"❌ AssertionError: {str(ae)}")
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f"❌ Error: {str(e)}")
        pytest.fail(str(e))


def test_natural_person_client_add_A(driver, test_data):
    """Test adding natural person client A"""

    data = test_data["data"]
    client_name = f"{data['client_name']}-A"
    test_natural_person_add(driver, test_data, person_name=client_name)


def test_natural_person_client_add_B(driver, test_data):
    """Test adding natural person client B"""

    data = test_data["data"]
    client_name = f"{data['client_name']}-B"
    test_natural_person_add(driver, test_data, person_name=client_name)


def test_natural_person_client_add_C(driver, test_data):
    """Test adding natural person client C"""

    data = test_data["data"]
    client_name = f"{data['client_name']}-C"
    test_natural_person_add(driver, test_data, person_name=client_name)