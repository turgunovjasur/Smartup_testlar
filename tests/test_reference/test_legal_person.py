import random
import pytest
from autotest.anor.mr.person.legal_person_add.legal_person_add import LegalPersonAdd
from autotest.anor.mr.person.legal_person_list.legal_person_list import LegalPersonList
from autotest.anor.mr.person.legal_person_view.legal_person_view import LegalPersonView
from flows.auth_flow import login_user, login_admin


def legal_person_add(driver, test_data, person_name=None, admin_or_user=True):
    """Test adding a legal person"""
    url = 'anor/mr/person/legal_person_list'

    # Login
    if admin_or_user:
        login_admin(driver, test_data, url=url)
    else:
        login_user(driver, test_data, url=url)

    # Open Legal Person List
    legal_person_list = LegalPersonList(driver)
    legal_person_list.element_visible()
    legal_person_list.click_add_button()

    # Add Legal Person
    legal_person_add = LegalPersonAdd(driver)
    legal_person_add.element_visible()

    legal_person_add.input_name(person_name)
    tin_number = random.randint(1, 999999999)
    legal_person_add.input_tin(tin_number)
    legal_person_add.click_save_button()

    # Verify in List
    legal_person_list.element_visible()
    legal_person_list.find_row(person_name)
    legal_person_list.click_view_button()

    # Verify in View
    legal_person_view = LegalPersonView(driver)
    legal_person_view.element_visible()
    text = legal_person_view.check_text()

    assert person_name == text, f"{person_name} != {text}"


@pytest.mark.regression
@pytest.mark.order(1)
def test_add_legal_person(driver, test_data):
    """Test adding legal person by filial"""

    data = test_data["data"]
    legal_person = data['legal_person_name']
    legal_person_add(driver, test_data, person_name=legal_person)

@pytest.mark.regression
@pytest.mark.order(56)
def test_add_legal_person_by_supplier(driver, test_data):
    """Test adding legal person by supplier"""

    data = test_data["data"]
    supplier_name = data['supplier_name']
    legal_person_add(driver, test_data, person_name=supplier_name, admin_or_user=False)