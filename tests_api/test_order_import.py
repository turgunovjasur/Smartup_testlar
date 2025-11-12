# # tests_api/test_order_import.py
# import pytest
#
# from conftest import load_data
# from tests_api.api_client import APIClient
#
#
# @pytest.mark.api
# def test_order_import_performance(test_data, load_data):
#     data = test_data["data"]
#
#     # API client
#     api = APIClient(
#         base_url=f'{data["url"]}',
#         project_code="trade",
#         filial_id="15405060",
#         username=f'{data["email_user"]}',
#         password=f'{data["password_user"]}',
#     )
#
#     response_body = load_data("response_body", file_name="order_export_import.json")
#     response_body["order"][0]["owner_person_code"] = load_data("supplier_cod")
#     response_body["order"][0]["status"] = "B#W"
#
#     # API chaqirish
#     resp, t_network, t_total = api.order_import(response_body)
#
#     # Tekshirish
#     assert resp.status_code == 200, f"Xato: {resp.text}"
#     assert t_network < 3, f"order_import juda sekin (network): {t_network:.2f} s"
#
#     # Log
#     print(
#         f"[IMPORT] network={t_network:.2f}s | total={t_total:.2f}s "
#         f"| size={len(resp.content)}B | status={resp.status_code}"
#     )
#     print(f"[IMPORT] javob (short): {str(resp.json())[:300]}...")
