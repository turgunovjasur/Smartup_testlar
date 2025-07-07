# Koordinatalarni olish uchun kursorni ekranda joylashtiring va koordinatalarni chiqarish uchun bu kodni ishlating
print("Koordinatalarni olish uchun ekranda kursorni kerakli joyga qo'ying...")
while True:
    import pyautogui

    x, y = pyautogui.position()  # Joriy koordinatalar
    print(f'X: {x}, Y: {y}', end='\r')  # Koordinatalarni ekranda chiqaramiz