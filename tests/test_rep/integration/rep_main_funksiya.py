import os
import random
import time
import pyautogui
from autotest.core.md.base_page import BasePage
import pyperclip


def wait_for_file_dialog_focus(test_text="check_test", timeout=10):
    """
    Save As oynasi ochilib, fayl nomi inputiga yozilgan matn clipboard orqali tasdiqlanadi.
    Modal ochilmaguncha hech narsa yozilmaydi.
    """
    elapsed = 0
    while elapsed < timeout:
        time.sleep(5)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('delete')
        time.sleep(0.2)

        pyautogui.write(test_text, interval=0.05)
        time.sleep(0.2)

        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.2)

        pasted = pyperclip.paste().strip()

        if pasted == test_text:
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.press('delete')
            return True

        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        time.sleep(0.5)
        elapsed += 0.5

    raise TimeoutError("Modal hali ochilmagan bo'lishi mumkin.")


def generate_and_verify_download(driver, file_name, file_type):
    base_page = BasePage(driver)

    file_name = f'{file_name}_{random.randint(10000, 99999)}'

    base_page.logger.info("⏳ Save As oynasiga fokus kutilyapti...")
    wait_for_file_dialog_focus()

    time.sleep(1)
    pyautogui.write(file_name, interval=0.2)
    base_page.logger.info(f"File name kiritildi: {file_name}")

    time.sleep(2)
    pyautogui.press('enter')
    base_page.logger.info("Enter bosildi!")

    downloads_path = os.path.join(os.environ["USERPROFILE"], "Downloads")
    timeout = 20
    poll_interval = 1
    elapsed = 0

    latest_file = None
    while elapsed < timeout:
        matching_files = [f for f in os.listdir(downloads_path)
                          if f.endswith(f"{file_name}.{file_type}")]
        if matching_files:
            latest_file = os.path.join(downloads_path, matching_files[0])
            if os.path.exists(latest_file) and os.path.getsize(latest_file) > 0:
                break
        time.sleep(poll_interval)
        elapsed += poll_interval

    assert latest_file is not None, f"{file_name}.{file_type} file not downloaded!"
    base_page.logger.info(f"✅ Loaded filename: {os.path.basename(latest_file)}")
