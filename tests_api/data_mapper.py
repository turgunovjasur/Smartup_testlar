# # tests_api/data_mapper.py
# import copy
#
#
# class DataMapper:
#     """Universal response → request mapper (override, add, delete)."""
#
#     @staticmethod
#     def clone_response(response_body: dict,
#                        overrides: dict | None = None,
#                        delete_marker="__delete__") -> dict:
#         """
#         Responseni to'liq ko'chirib, nested keylarni override, qo'shish yoki o'chirish.
#         Path: "order_products.0.product_price"
#
#         :param response_body: API response (dict)
#         :param overrides: dict, masalan:
#             {
#               "deal_id": "",                               # override
#               "total_amount": "65000",                     # override
#               "order_products.0.product_price": "9999",    # nested override
#               "order_products.0.batch_number": None,       # None → o'chirish
#               "order_products.0.new_field": "test",        # yo'q bo'lsa qo'shish
#               "status": "__delete__"                       # delete_marker bilan o'chirish
#             }
#         :param delete_marker: string, keyni o'chirish uchun maxsus marker
#         :return: yangi request body (dict)
#         """
#         request_body = copy.deepcopy(response_body)
#
#         if not overrides:
#             return request_body
#
#         for path, value in overrides.items():
#             DataMapper._apply_path(request_body, path, value, delete_marker)
#
#         return request_body
#
#     @staticmethod
#     def _apply_path(target: dict, path: str, value, delete_marker: str):
#         """
#         Nested path bo'yicha target ichida key ni yangilash, qo'shish yoki o'chirish.
#         """
#         parts = path.split(".")
#         current = target
#
#         for i, part in enumerate(parts):
#             is_last = i == len(parts) - 1
#
#             # Agar array index bo'lsa
#             if part.isdigit():
#                 idx = int(part)
#                 if not isinstance(current, list):
#                     raise TypeError(f"Path xato: {part} list emas")
#                 # Ro'yxat ichida index mavjudligiga qarab ishlaymiz
#                 if idx >= len(current):
#                     raise IndexError(f"Index {idx} yo'q")
#                 current = current[idx]
#             else:
#                 if is_last:
#                     # Override yoki qo'shish yoki o'chirish
#                     if value is None or value == delete_marker:
#                         current.pop(part, None)
#                     else:
#                         current[part] = value
#                 else:
#                     if part not in current or not isinstance(current[part], (dict, list)):
#                         # Key mavjud bo'lmasa, dict yaratamiz
#                         current[part] = {}
#                     current = current[part]
