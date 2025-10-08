import random
import pytest
from qase.pytest import qase
from flows.auth_flow import login_user, login_admin
from tests.ui.test_reference.legal_person_flows import add_flow, view_flow, list_flow

# ----------------------------------------------------------------------------------------------------------------------

def legal_person_add(driver, test_data, soft_assertions, person_name=None, admin_or_user=True):
    """Test adding a legal person"""

    i = random.randint(10000, 99999)
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
             state=True,
             person_name=person_name,
             short_name=short_name,
             main_phone=main_phone,
             telegram=telegram,
             email=email,
             address=address,
             post_address=post_address,
             tin=tin,
             cea=cea,
             vat_code=vat_code,
             lat_lng=lat_lng,
             address_guide=address_guide,
             code=code,
             web=web,
             barcode=barcode,
             zip_code=zip_code)

    list_flow(driver, find_row=code, view=True)

    view_flow(driver, soft_assertions,
              person_name=person_name,
              short_name=short_name,
              code=code,
              barcode=barcode,
              email=email)

    return code

# ----------------------------------------------------------------------------------------------------------------------

@qase.id(164)
@qase.title("Add Legal Person")
@pytest.mark.regression
@pytest.mark.order(10)
def test_add_legal_person(driver, test_data, soft_assertions, save_data):
    """
        Legal Person qo‘shish va tekshirish.

        Preconditions:
            - Admin sifatida login bo‘lishi kerak
            - Legal Person list sahifasi ochiq bo‘lishi kerak

        Checklist:
        1. Admin login qilinadi
        2. Legal Person list sahifasi ochilgani tekshiriladi
        3. Add tugmasi bosiladi
        4. Add formasi ochilgani tekshiriladi
        5. Maydonlar to‘ldiriladi
        6. Save tugmasi bosiladi va Yes tasdiqlanadi
        7. Ro‘yxatda Code orqali qidiriladi
        8. Yozuv topiladi
        9. View tugmasi bosiladi
        10. Qiymatlar tekshiriladi
    """

    data = test_data["data"]
    legal_person = data['legal_person_name']
    code = legal_person_add(driver, test_data, soft_assertions, person_name=legal_person)
    save_data("legal_person_cod", code)

# ----------------------------------------------------------------------------------------------------------------------

@qase.id(165)
@qase.title("Add Legal Person by Supplier")
@pytest.mark.regression
@pytest.mark.order(530)
def test_add_legal_person_by_supplier(driver, test_data, soft_assertions, save_data):
    """
        Supplier orqali sifatida Legal Person qo‘shish va tekshirish.

        Preconditions:
            - Admin sifatida login bo‘lishi kerak
            - Legal Person list sahifasi ochiq bo‘lishi kerak

        Checklist:
        1. Admin login qilinadi
        2. Legal Person list sahifasi ochilgani tekshiriladi
        3. Add tugmasi bosiladi
        4. Add formasi ochilgani tekshiriladi
        5. Forma maydonlari supplier ma’lumotlari bilan to‘ldiriladi
        6. Save tugmasi bosiladi va Yes tasdiqlanadi
        7. Ro‘yxatda Code orqali qidiriladi
        8. Yangi yozuv ro‘yxatdan topiladi
        9. View tugmasi bosiladi
        10. Kiritilgan qiymatlar supplier ma’lumotlariga mosligi tekshiriladi
    """

    data = test_data["data"]
    supplier_name = data['supplier_name']
    code = legal_person_add(driver, test_data, soft_assertions, person_name=supplier_name, admin_or_user=False)
    save_data("supplier_cod", code)

# ----------------------------------------------------------------------------------------------------------------------
