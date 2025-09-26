from autotest.anor.mr.person.legal_person_add.legal_person_add import LegalPersonAdd
from autotest.anor.mr.person.legal_person_list.legal_person_list import LegalPersonList
from autotest.anor.mr.person.legal_person_view.legal_person_view import LegalPersonView

# ======================================================================================================================

def safe_input(method, value):
    if value not in (None, ""):
        method(value)

# ======================================================================================================================

def add_flow(driver, **kwargs):
    add = LegalPersonAdd(driver)
    add.element_visible()

    add.switch_state(kwargs.get("state", True))

    safe_input(add.input_name,         kwargs.get("person_name"))
    safe_input(add.input_short_name,   kwargs.get("short_name"))
    safe_input(add.input_main_phone,   kwargs.get("main_phone"))
    safe_input(add.input_telegram,     kwargs.get("telegram"))
    safe_input(add.input_email,        kwargs.get("email"))
    safe_input(add.input_address,      kwargs.get("address"))
    safe_input(add.input_post_address, kwargs.get("post_address"))
    safe_input(add.input_tin,          kwargs.get("tin"))
    safe_input(add.input_cea,          kwargs.get("cea"))
    safe_input(add.input_vat_code,     kwargs.get("vat_code"))
    safe_input(add.input_latlng,       kwargs.get("lat_lng"))
    safe_input(add.input_address_guide,kwargs.get("address_guide"))
    safe_input(add.input_code,         kwargs.get("code"))
    safe_input(add.input_web,          kwargs.get("web"))
    safe_input(add.input_barcode,      kwargs.get("barcode"))
    safe_input(add.input_zip_code,     kwargs.get("zip_code"))

    add.click_save_button()

# ======================================================================================================================

def list_flow(driver, **kwargs):
    _list = LegalPersonList(driver)
    _list.element_visible()

    if kwargs.get("add"):
        _list.click_add_button()

    if kwargs.get("find_row"):
        _list.find_row(kwargs.get("find_row"))

    if kwargs.get("view"):
        _list.click_view_button()

# ======================================================================================================================

def view_flow(driver, soft_assertions, **kwargs):
    person_name = kwargs.get("person_name")
    short_name = kwargs.get("short_name")
    code = kwargs.get("code")
    barcode = kwargs.get("barcode")
    email = kwargs.get("email")

    view = LegalPersonView(driver)
    view.element_visible()

    get_person_name = view.get_person_name()
    soft_assertions.assert_equals(get_person_name, person_name)

    # View-form
    view.click_navbar(navbar_name="Основная информация")

    get_name = view.get_input_value(input_name="Название")
    soft_assertions.assert_equals(get_name, person_name)

    get_short_name = view.get_input_value(input_name="Альтернативное название")
    soft_assertions.assert_equals(get_short_name, short_name)

    get_code = view.get_input_value(input_name="Код")
    soft_assertions.assert_equals(get_code, code)

    get_barcode = view.get_input_value(input_name="Штрих-код")
    soft_assertions.assert_equals(get_barcode, barcode)

    # View-card
    get_email = view.get_card_value(card_name="Email")
    soft_assertions.assert_equals(get_email, email)

    get_name = view.get_card_value(card_name="Название")
    soft_assertions.assert_equals(get_name, person_name)

    get_short_name = view.get_card_value(card_name="Альтернативное название")
    soft_assertions.assert_equals(get_short_name, short_name)

    get_code = view.get_card_value(card_name="Код")
    soft_assertions.assert_equals(get_code, code)

    get_barcode = view.get_card_value(card_name="Штрих-код")
    soft_assertions.assert_equals(get_barcode, barcode)
    soft_assertions.assert_all()

# ======================================================================================================================
