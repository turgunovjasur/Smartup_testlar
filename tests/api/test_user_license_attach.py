import calendar
from datetime import datetime
import pytest
from apis.user_license_api import UserLicenseAPI

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(18)
def test_get_purchase_info(load_data, save_data):
    api = UserLicenseAPI(load_data, auth_profile="admin", filial_id=load_data("api/administration_id"))

    body = {}

    resp, t_network, t_total = api.purchase_info(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    person_id = data["payers"][0]["person_id"]
    contract_id = data["payers"][0]["contracts"][0]["contract_id"]
    balance = float(data["payers"][0]["contracts"][0]["balance"])

    service_id = None

    for row in data['licenses']:
        if row['service_name'] == "Подключение к системе (5x)":
            service_id = row['service_id']
            break

    assert service_id is not None, "Service 'Подключение к системе (5x)' not found!"

    file_name = "license_data_store"

    save_data("api/person_id", person_id, file_name=file_name)
    save_data("api/contract_id", contract_id, file_name=file_name)
    save_data("api/balance", balance, file_name=file_name)
    save_data("api/service_id", service_id, file_name=file_name)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(19)
def test_purchase_license(load_data, save_data):
    api = UserLicenseAPI(load_data, auth_profile="admin", filial_id=load_data("api/administration_id"))

    file_name = "license_data_store"

    person_id = load_data("api/person_id", file_name=file_name)
    contract_id = load_data("api/contract_id", file_name=file_name)
    service_id = load_data("api/service_id", file_name=file_name)

    now = datetime.now()
    current_date = now.strftime("%d.%m.%Y")                                          # Joriy sana (kun, oy, yil)
    last_day = calendar.monthrange(now.year, now.month)[1]                           # Joriy oyning oxirgi kuni (kun)
    last_day_of_month = datetime(now.year, now.month, last_day).strftime("%d.%m.%Y") # Joriy oyning oxirgi kuni (kun, oy, yil)
    current_month = now.strftime("%m.%Y")                                            # Joriy oyning (oy, yil)

    body = {
      "autosign_faktura_enabled": "N",
      "posted": "Y",
      "purchases": [
        {
          "begin_date": current_date,
          "end_date": current_month,
          "payer_id": person_id,
          "contract_id": contract_id,
          "licenses": [
            {
              "service_id": service_id,
              "quantity": 1
            }
          ]
        }
      ]
    }

    resp, t_network, t_total = api.purchase_license(body)

    api.handle_response(resp, t_network, t_total, body=body, expect_status=200, allow_empty_response=True)

    save_data("api/current_date", current_date, file_name=file_name)
    save_data("api/last_date", last_day_of_month, file_name=file_name)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(20)
def test_user_license_list(load_data, save_data):
    api = UserLicenseAPI(load_data, auth_profile="admin", filial_id=load_data("api/administration_id"))

    body = {
      "p": {
        "column": [
              "begin_date",
              "end_date",
              "license_id",
        ],
        "filter": [
          "status",
          "=",
          ["A"]
        ],
        "limit": 50,
        "offset": 0,
        "sort": ["-created_on"]
      }
    }

    resp, t_network, t_total = api.license_list(body)

    data = api.handle_response(resp, t_network, t_total, body=body)

    file_name = "license_data_store"
    current_date = load_data("api/current_date", file_name=file_name)
    last_date = load_data("api/last_date", file_name=file_name)

    get_current_date = data['data'][0][0]
    assert get_current_date == current_date, f"{get_current_date} != {current_date}"

    get_last_date = data['data'][0][1]
    assert get_last_date == last_date, f"{get_last_date} != {last_date}"

    license_id = data['data'][0][2]
    save_data("api/license_id", license_id, file_name=file_name)

# ----------------------------------------------------------------------------------------------------------------------

@pytest.mark.api
@pytest.mark.order(21)
def test_user_license_attach(load_data):
    api = UserLicenseAPI(load_data, auth_profile="admin", filial_id=load_data("api/administration_id"))

    file_name = "license_data_store"
    user_id = load_data("api/user_id")
    license_id = load_data("api/license_id", file_name=file_name)

    body = {
      "user_id": user_id,
      "license_id": license_id
    }

    resp, t_network, t_total = api.license_user_attach(body)

    api.handle_response(resp, t_network, t_total, body=body, expect_status=200, allow_empty_response=True)

# ----------------------------------------------------------------------------------------------------------------------