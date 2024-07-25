# Veb-ilova avtomatlashtirilgan testi

Bu loyiha Python, Pytest va Selenium WebDriver yordamida veb-ilova uchun avtomatlashtirilgan testlarni o'z ichiga oladi.

## Umumiy ma'lumot

Test skripti ilovada foydalanuvchi yo'nalishini simulyatsiya qiladi, jumladan tizimga kirish, navigatsiya va buyurtma yaratish. U yo'l davomida turli sahifa elementlari va funksiyalarini tekshiradi.

## Talablar

- Python 3.x
- Pytest
- Selenium WebDriver
- Veb-brauzer drayveri (masalan: ChromeDriver, Firefox)

## O'rnatish

1. Ushbu repozitoriyni klonlang
2. Kerakli paketlarni o'rnating:
3. Tegishli veb-brauzer(versiya: 127.0.6533.72) drayverini o'rnatganingizga va u tizim PATH'ingizda ekanligiga ishonch hosil qiling

## Loyiha tuzilishi

- `pages/`: Ilovaning turli sahifalari uchun Page Object Model sinflarini o'z ichiga oladi
- `utils/`: Sozlash va konfiguratsiya uchun yordamchi vositalar
- `test_all.py`: Asosiy test skripti

## Testlarni ishga tushirish

Testlarni ishga tushirish uchun loyihaning asosiy katalogida quyidagi buyruqni ishga tushiring:
1. pytest tests/test_registration.py --alluredir=reports/allure_results
2. allure serve reports/allure_results 
3. pytest -k "chrome" -> Chrome bilan
4. pytest -k "firefox" -> Firefox bilan

## Test jarayoni

1. Ilova URL manzilini ochish (https://smartup.online/)
2. Berilgan ma'lumotlar bilan tizimga kirish
3. Boshqaruv paneli va Sotuvlar sahifalari orqali navigatsiya
4. Yangi buyurtma yaratish
5. Buyurtma tafsilotlarini to'ldirish
6. Buyurtma yaratilganini tekshirish

## Eslatmalar

- Test hozirda yangi buyurtma yaratilgandan so'ng buyurtmalar soni o'zgarmasligini tekshiradi. Bu test yoki ilova logikasidagi xato bo'lishi mumkin.
- Testni ishga tushirishdan oldin to'ldiruvchi login ma'lumotlarini haqiqiy ma'lumotlar bilan almashtirishni unutmang.

## Hissa qo'shish

Yaxshilanishlar yoki xatolarni tuzatish uchun muammolar yoki so'rovlar yuborishingiz mumkin.

## Litsenziya

[None]
