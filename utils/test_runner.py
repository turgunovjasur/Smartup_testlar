# import time
# from contextlib import contextmanager
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
#
# from tests.test_life_cycle import (
#     test_company_creat,
#     test_legal_person_add,
#     test_filial_creat,
#     test_room_add,
#     test_robot_add,
#     test_natural_person_add,
#     test_user_creat,
#     test_adding_permissions_to_user,
#     test_user_change_password,
#     test_price_type_add,
#     test_payment_type_add,
#     test_sector_add,
#     test_product_add,
#     test_natural_person_client_add,
#     test_client_add,
#     test_room_attachment,
#     test_init_balance,
#     test_order_add,
#     test_order_change_status
# )
#
#
# class TestRunner:
#     def __init__(self, base_url):
#         self.base_url = base_url
#         self.driver = None
#
#     @contextmanager
#     def get_driver(self):
#         """WebDriver ni yaratish va uni to'g'ri yopish uchun context manager"""
#         try:
#             service = ChromeService(ChromeDriverManager().install())
#             options = Options()
#             options.add_argument("--start-maximized")
#             options.add_argument("--force-device-scale-factor=0.90")
#
#             self.driver = webdriver.Chrome(service=service, options=options)
#             self.driver.get(self.base_url)
#             yield self.driver
#
#         finally:
#             if self.driver:
#                 try:
#                     self.driver.quit()
#                 except Exception as e:
#                     print(f"Driver yopishda xatolik: {e}")
#                 time.sleep(2)  # Driver to'liq yopilishi uchun kutish
#
#     def run_test(self, test_func, *args, **kwargs):
#         """Bitta testni xavfsiz ishga tushirish"""
#         with self.get_driver() as driver:
#             try:
#                 test_func(driver, *args, **kwargs)
#                 print(f"{test_func.__name__} muvaffaqiyatli o'tdi!")
#                 return True
#             except Exception as e:
#                 print(f"{test_func.__name__} da xatolik: {str(e)}")
#                 return False
#
#     def run_all_tests(self):
#         """Barcha testlarni ketma-ket ishga tushirish"""
#         tests = [
#             test_company_creat,
#             test_legal_person_add,
#             test_filial_creat,
#             test_room_add,
#             test_robot_add,
#             test_natural_person_add,
#             test_user_creat,
#             test_adding_permissions_to_user,
#             test_user_change_password,
#             test_price_type_add,
#             test_payment_type_add,
#             test_sector_add,
#             test_product_add,
#             test_natural_person_client_add,
#             test_client_add,
#             test_room_attachment,
#             test_init_balance,
#             test_order_add,
#             test_order_change_status
#         ]
#
#         results = []
#         for test in tests:
#             success = self.run_test(test)
#             results.append((test.__name__, success))
#
#             if not success:  # Test muvaffaqiyatsiz bo'lsa
#                 print(f"\nTest {test.__name__} da xatolik. Keyingi testlar to'xtatildi.")
#                 break
#
#         # Natijalarni chiqarish
#         print("\nTest natijalari:")
#         for test_name, success in results:
#             status = "✓" if success else "✗"
#             print(f"{status} {test_name}")
#
#
# if __name__ == "__main__":
#     runner = TestRunner("http://gw.greenwhite.uz:8081/xtrade/login.html")
#     runner.run_all_tests()