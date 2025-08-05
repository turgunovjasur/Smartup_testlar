import random
import pytest
from flows.auth_flow import login_user, login_admin
from tests.test_reference.legal_person_flows import add_flow, view_flow, list_flow


def legal_person_add(driver, test_data, person_name=None, admin_or_user=True):
    """Test adding a legal person"""

    i = random.randint(1000, 9999)
    main_phone = f"+99890000{i}"
    telegram = f"@telegram_{i}"
    email = f"email_{i}@gmail.uz"
    address = f"O'zbekiston, Toshkent sh, Beshyog'och, 22_({i})"
    post_address=f"info@greenwhite_{i}.uz"
    tin = f"tin_{i}"
    cea = f"cea_{i}"
    vat_code = f"vat_code_{i}"
    lat_lng = "41.31127920445961,69.23851132392885,12"
    address_guide = "Glinka ko'cha"
    code = f"code_{i}"
    web = f"https://web_legal_person_{i}.uz"
    barcode = f"barcode_{i}"
    zip_code = f"zip_code_{i}"
    short_name = f"short_name-{person_name}"

    url = 'anor/mr/person/legal_person_list'
    if admin_or_user:
        login_admin(driver, test_data, url=url)
    else:
        login_user(driver, test_data, url=url)

    list_flow(driver, add=True)

    add_flow(driver,
             state=True, person_name=person_name, short_name=short_name, main_phone=main_phone,
             telegram=telegram, email=email, address=address, post_address=post_address,
             tin=tin, cea=cea, vat_code=vat_code, lat_lng=lat_lng, address_guide=address_guide,
             code=code, web=web, barcode=barcode, zip_code=zip_code)

    list_flow(driver, find_row=code, view=True)

    view_flow(driver,
              person_name=person_name, short_name=short_name,
              code=code, barcode=barcode, email=email)


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