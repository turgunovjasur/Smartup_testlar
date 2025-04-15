# import random
# import json
#
# # O‘yinchi klassi
# class Oyinchi:
#     def __init__(self, ism):
#         self.ism = ism
#
# # Natijalarni saqlovchi klass
# class NatijaSaqlovchi:
#     def __init__(self, fayl_nomi):
#         self.fayl_nomi = fayl_nomi
#
#     def saqlash(self, ism, foydalanuvchi_tanlovi, kompyuter_tanlovi, g_olib):
#         natija = {
#             "ism": ism,
#             "foydalanuvchi": foydalanuvchi_tanlovi,
#             "kompyuter": kompyuter_tanlovi,
#             "g'olib": g_olib
#         }
#
#         try:
#             with open(self.fayl_nomi, "r", encoding="utf-8") as f:
#                 natijalar = json.load(f)
#         except:
#             natijalar = []
#
#         natijalar.append(natija)
#
#         with open(self.fayl_nomi, "w", encoding="utf-8") as f:
#             json.dump(natijalar, f, indent=4, ensure_ascii=False)
#
#     def statistika_korish(self, ism):
#         try:
#             with open(self.fayl_nomi, "r", encoding="utf-8") as f:
#                 natijalar = json.load(f)
#         except:
#             print("Hali hech qanday natija mavjud emas.")
#             return
#
#         jami = yutuq = yutqazish = durrang = 0
#
#         for natija in natijalar:
#             if natija["ism"] == ism:
#                 jami += 1
#                 if natija["g'olib"] == "foydalanuvchi":
#                     yutuq += 1
#                 elif natija["g'olib"] == "kompyuter":
#                     yutqazish += 1
#                 else:
#                     durrang += 1
#
#         print(f"\n📈 {ism} uchun statistika:")
#         print(f"| Jami: {jami} | Yutdi: {yutuq} | Yutqazdi: {yutqazish} | Durrang: {durrang} |")
#
# # O‘yin klassi
# class Oyin:
#     def __init__(self, oyinchi, saqlovchi):
#         self.oyinchi = oyinchi
#         self.saqlovchi = saqlovchi
#         self.varianti = ["tosh", "qaychi", "qogoz"]
#
#     def boshlash(self):
#         print("\nTanlang: \ntosh: 1, \nqaychi: 2, \nqogoz: 3")
#
#         try:
#             tanlov = int(input("Raqam kiriting: "))
#             foydalanuvchi_tanlovi = self.varianti[tanlov - 1]
#         except:
#             print("Noto‘g‘ri kiritish!")
#             return
#
#         kompyuter_tanlovi = random.choice(self.varianti)
#
#         print(f"\nSiz: {foydalanuvchi_tanlovi}")
#         print(f"Kompyuter: {kompyuter_tanlovi}")
#
#         if foydalanuvchi_tanlovi == kompyuter_tanlovi:
#             g_olib = "durrang"
#             print("🤝 Durrang!")
#         elif (foydalanuvchi_tanlovi == "tosh" and kompyuter_tanlovi == "qaychi") or \
#              (foydalanuvchi_tanlovi == "qaychi" and kompyuter_tanlovi == "qogoz") or \
#              (foydalanuvchi_tanlovi == "qogoz" and kompyuter_tanlovi == "tosh"):
#             g_olib = "foydalanuvchi"
#             print("🎉 Siz yutdingiz!")
#         else:
#             g_olib = "kompyuter"
#             print("😢 Kompyuter yutdi!")
#
#         self.saqlovchi.saqlash(self.oyinchi.ism, foydalanuvchi_tanlovi, kompyuter_tanlovi, g_olib)
#
# # === ASOSIY DASTUR ===
# def main():
#     ism = input("Ismingizni kiriting: ")
#     oyinchi = Oyinchi(ism)
#     saqlovchi = NatijaSaqlovchi("natijalar.json")
#     oyiin = Oyin(oyinchi, saqlovchi)
#
#     while True:
#         print("\n=== MENYU ===")
#         print("1) O'yin boshlash")
#         print("2) Statistika ko‘rish")
#         print("3) Chiqish")
#
#         tanlov = input("Tanlovingiz: ")
#
#         if tanlov == "1":
#             oyiin.boshlash()
#         elif tanlov == "2":
#             saqlovchi.statistika_korish(ism)
#         elif tanlov == "3":
#             print("Xayr!")
#             break
#         else:
#             print("Noto‘g‘ri tanlov!")
#
# if __name__ == "__main__":
#     main()
#
#
#
#
#
#

