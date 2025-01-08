import requests

BASE_URL = "https://reqres.in/api"


def test_create_user():
    url = "https://reqres.in/api/users"

    payload = {
        "name": "jasur",
        "job": "qa"
    }

    response = requests.post(url, json=payload)

    response_data = response.json()

    print("Status Code:", response.status_code)
    print("Response Data:", response_data)

    assert response.status_code == 201, f"Kutilgan kod 201, lekin {response.status_code} qaytdi"

    assert response_data["name"] == payload["name"], f"Ism mos emas: {response_data['name']}"
    assert response_data["job"] == payload["job"], f"Ish mos emas: {response_data['job']}"
    assert "id" in response_data, "ID mavjud emas"
    assert "createdAt" in response_data, "Yaratilgan vaqt mavjud emas"

    print("Test muvaffaqiyatli bajarildi!" if response.status_code == 201 else "Testda xatolik bor")


def test_get_user():
    url = "https://reqres.in/api/users/2"

    response = requests.get(url)

    response_data = response.json()

    print("Status Code:", response.status_code)
    print("Response Data:", response_data)

    assert response.status_code == 200, f"Kutilgan kod 200, lekin {response.status_code} qaytdi"

    assert response_data["data"]["id"] == 2, "ID mos emas"
    assert "email" in response_data["data"], "Email mavjud emas"
    assert "first_name" in response_data["data"], "First name mavjud emas"
    assert "last_name" in response_data["data"], "Last name mavjud emas"
    assert "avatar" in response_data["data"], "Avatar mavjud emas"
    assert "support" in response_data, "Support mavjud emas"

    print("GET testi muvaffaqiyatli bajarildi!")


def test_update_user():
    url = "https://reqres.in/api/users/2"

    payload = {
        "name": "morpheus",
        "job": "zion resident"
    }

    response = requests.put(url, json=payload)
    response_data = response.json()

    print("Status Code:", response.status_code)
    print("Response Data:", response_data)

    assert response.status_code == 200, f"Kutilgan kod 200, lekin {response.status_code} qaytdi"
    assert response_data["name"] == payload["name"], f"Ism mos emas: {response_data['name']}"
    assert response_data["job"] == payload["job"], f"Ish mos emas: {response_data['job']}"
    assert "updatedAt" in response_data, "Yaratilgan vaqt mavjud emas"

    print("PUT testi muvaffaqiyatli bajarildi!")


def test_delete_user():
    url = "https://reqres.in/api/users/2"

    response = requests.delete(url)

    print("Status Code:", response.status_code)

    assert response.status_code == 204, f"Kutilgan kod 204, lekin {response.status_code} qaytdi"

    print("DELETE testi muvaffaqiyatli bajarildi!")


#  ---------------------------------------------------------------------------------------------------------------------

def test_login_user():
    url = "https://reqres.in/api/login"

    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }

    response = requests.post(url, json=payload)
    response_data = response.json()

    print("Status Code:", response.status_code)
    print("Response Data:", response_data)

    assert response.status_code == 200, f"Kutilgan kod 200, lekin {response.status_code} qaytdi"
    assert "token" in response_data, "Token mavjud emas"

    print("Login testi muvaffaqiyatli bajarildi!")


def test_login_user_error():
    url = "https://reqres.in/api/login"

    payload = {
        "email": "peter@klaven"
    }

    response = requests.post(url, json=payload)
    response_data = response.json()

    print("Status Code:", response.status_code)
    print("Response Data:", response_data)

    assert response.status_code == 400, f"Kutilgan kod 400, lekin {response.status_code} qaytdi"
    assert "error" in response_data, "Xatolik mavjud emas"
    assert response_data["error"] == "Missing password", f"Xatolik mos emas: {response_data['error']}"

    print("Login xatolik testi muvaffaqiyatli bajarildi!")


#  ---------------------------------------------------------------------------------------------------------------------


def test_all():
    try:
        print("\nRunning test_create_user...")
        test_create_user()
        print("\nRunning test_get_user...")
        test_get_user()
        print("\nRunning test_update_user...")
        test_update_user()
        print("\nRunning test_delete_user...")
        test_delete_user()
        print("\nRunning test_login_user...")
        test_login_user()
        print("\nRunning test_login_user_error...")
        test_login_user_error()
        print("\nBarcha testlar muvaffaqiyatli bajarildi!")
    except AssertionError as e:
        print(f"Testda xatolik: {e}")


test_all()
