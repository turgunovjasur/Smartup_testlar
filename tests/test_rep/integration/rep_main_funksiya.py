import os
import random
import time
import pyautogui
from autotest.core.md.base_page import BasePage


def generate_and_verify_download(driver, file_name, file_type):
    base_page = BasePage(driver)

    # Random file nomi
    file_name = f'{file_name}_{random.randint(10000, 99999)}'

    # Fayl nomini yozish
    time.sleep(5)
    pyautogui.write(file_name, interval=0.2)
    base_page.logger.info(f"File name kiritildi: {file_name}")

    # Enter bosish
    time.sleep(2)
    pyautogui.press('enter')
    base_page.logger.info("Enter bosildi!")

    # Yuklanishni kutish va tekshirish
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
