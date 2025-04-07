import random
import pytest
from autotest.anor.mr.person.legal_person_add.legal_person_add import LegalPersonAdd
from autotest.anor.mr.person.legal_person_list.legal_person_list import LegalPersonList
from autotest.anor.mr.person.legal_person_view.legal_person_view import LegalPersonView
from autotest.core.md.base_page import BasePage
from tests.test_base.test_base import login_admin, login_user
from utils.driver_setup import driver
from tests.conftest import test_data


def legal_person_add(driver, test_data, person_name=None, admin_or_user=True):
    """Test adding a legal person"""

    base_page = BasePage(driver)
    base_page.logger.info("▶️ Running: test_legal_person_add")
    base_page.logger.info(f"Data: name='{person_name}'")

    try:
        # Login
        if admin_or_user:
            login_admin(driver, test_data, url='anor/mr/person/legal_person_list')
        else:
            login_user(driver, test_data, url='anor/mr/person/legal_person_list')

        # Open Legal Person List
        legal_person_list = LegalPersonList(driver)
        assert legal_person_list.element_visible(), "LegalPersonList not open!"
        legal_person_list.click_add_button()

        # Add Legal Person
        legal_person_add = LegalPersonAdd(driver)
        assert legal_person_add.element_visible(), "LegalPersonAdd not open!"

        legal_person_add.input_name(person_name)
        tin_number = random.randint(1, 999999999)
        legal_person_add.input_tin(tin_number)
        legal_person_add.click_save_button()

        # Verify in List
        assert legal_person_list.element_visible(), "LegalPersonList not open after save!"
        legal_person_list.find_row(person_name)
        legal_person_list.click_view_button()

        # Verify in View
        legal_person_view = LegalPersonView(driver)
        assert legal_person_view.element_visible(), "LegalPersonView not open!"
        text = legal_person_view.check_text()

        assert person_name == text, f"{person_name} != {text}"
        base_page.logger.info(f"✅ Verified: '{person_name}'")

    except AssertionError as ae:
        base_page.logger.error(f'❌ AssertionError: {str(ae)}')
        base_page.take_screenshot("assertion_error")
        pytest.fail(str(ae))

    except Exception as e:
        base_page.logger.error(f'❌ Error: {str(e)}')
        pytest.fail(str(e))


def test_add_legal_person(driver, test_data):
    """Test adding legal person by filial"""

    data = test_data["data"]
    legal_person = data['legal_person_name']
    legal_person_add(driver, test_data, person_name=legal_person)


def test_add_legal_person_by_supplier(driver, test_data):
    """Test adding legal person by supplier"""

    data = test_data["data"]
    supplier_name = data['supplier_name']
    legal_person_add(driver, test_data, person_name=supplier_name, admin_or_user=False)