# # test_order_export.py
# import pytest
# from tests_api.api_client import APIClient
#
#
# @pytest.mark.api
# def test_order_export_performance(test_data, load_data, save_data):
#     data = test_data["data"]
#
#     api = APIClient(
#         base_url=f'{data["url"]}',
#         project_code="trade",
#         filial_id="15405060",
#         username=f'{data["email_user"]}',
#         password=f'{data["password_user"]}',
#     )
#
#     body = {
#         "filial_codes": [{"filial_code": f'{load_data("legal_person_cod")}'}],
#         "filial_code": f'{load_data("legal_person_cod")}',
#         "deal_id": f'{load_data("order_id_1")}'
#     }
#
#     resp, t_network, t_total = api.order_export(body)
#
#     # Status code tekshirish
#     assert resp.status_code == 200, f"API xato: {resp.text}"
#
#     # Javobni JSON ga parse qilamiz
#     data = resp.json()
#     save_data("response_body", data, file_name="order_export_import.json")
#
#     # Natijani chiqaryapmiz: network vs total
#     print(
#         f"[EXPORT] network={t_network:.2f}s | total={t_total:.2f}s "
#         f"| size={len(resp.content)}B | status={resp.status_code}"
#     )
#     print(f"[EXPORT] javob (short): {str(data)[:300]}...")
