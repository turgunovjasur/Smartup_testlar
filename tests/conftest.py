import pytest


@pytest.fixture(scope="session")
def test_data():
    """Test data"""
    base_data = {
        "email_company": "admin@head",
        "password_company": "greenwhite",
        "name_company": "red test",
        "plan_account": "UZ COA",
        "bank_name": "UZ BANK",
        "base_currency_cod": 860,

        "code_input": "autotest",
        # "code_input": "test",
        # "code_input": "red_test",
        "cod": 4,
        # "cod": 46,
        # "url": "https://smartup.merospharm.uz/login.html",
        # "url": "https://app3.greenwhite.uz/xtrade/login.html",
        "url": "https://smartup.online/login.html",
    }
    filial_data = {
        "email": f"admin@{base_data['code_input']}",
        "password": f"{base_data['password_company']}",
        "Administration_name": "Администрирование",
        "filial_name": f"Test_filial-{base_data['cod']}",
        "login_user": f"test-{base_data['cod']}",
    }
    user_data = {
        "email_user": f'{filial_data["login_user"]}@{base_data["code_input"]}',
        "password_user": 123456789,
    }
    product_data = {
        "legal_person_name": f"legal_person-{base_data['cod']}",
        "natural_person_name": f"natural_person-{base_data['cod']}",
        "client_name": f"client-{base_data['cod']}",
        "contract_name": f"contract-{base_data['cod']}",
        "room_name": f"Test_room-{base_data['cod']}",
        "robot_name": f"Test_robot-{base_data['cod']}",
        "sub_filial_name": f"Test_sub_filial-{base_data['cod']}",
        "sector_name": f"Test_sector-{base_data['cod']}",
        "product_name": f"Test_product-{base_data['cod']}",
        "template_name": f"Test_invoice_report-{base_data['cod']}",
        "role_name": "Админ",
        "warehouse_name": "Основной склад",
        "cash_register_name": "Основная касса",
        "measurement_name": "Количество",

        "price_type_name_UZB": f"Цена продажи UZB-{base_data['cod']}",
        "price_type_name_USA": f"Цена продажи USA-{base_data['cod']}",
        "price_tag_name": "Ценник",

        "margin_name": f"Test_margin-{base_data['cod']}",
        "percent_value": 5,

        "payment_type_name": "Наличные деньги",
        "product_quantity": 1_000,
        "product_price": 12_000,
        "product_price_USA": 12,
    }
    order_status = {
        "Draft": "Черновик",
        "New": "Новый",
        "Processing": "В обработке",
        "Pending": "В ожидании",
        "Shipped": "Отгружен",
        "Delivered": "Доставлен",
        "Archive": "Архив",
        "Cancelled": "Отменен",
    }
    error_massage = {
        "error_massage_1": "H02-ANOR279-015",
        "error_massage_2": "H02-ANOR279-006",
        "error_massage_3": "A02-16-120",
        "error_massage_4": "H02-ANOR66-003",  # error -> sector
    }
    return {
        "data": {
            **base_data,
            **filial_data,
            **user_data,
            **product_data,
            **order_status,
            **error_massage
        }
    }