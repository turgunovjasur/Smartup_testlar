import os
import random
import time
import pyautogui
from autotest.core.md.base_page import BasePage


def generate_and_verify_download(driver, file_name, file_type):
    base_page = BasePage(driver)

    time.sleep(5)

    integer = random.randint(10000, 99999)
    file_name = f'{file_name}_{integer}'

    for f in file_name:
        pyautogui.write(f)
        time.sleep(0.1)
    base_page.logger.info(f"File name kiritildi: {file_name}")

    pyautogui.press('enter')
    base_page.logger.info("Enter bosildi!")

    time.sleep(5)
    downloads_path = os.path.join(os.environ["USERPROFILE"], "Downloads")
    files = os.listdir(downloads_path)
    files = [os.path.join(downloads_path, f) for f in files if f.endswith(f'{file_name}.{file_type}')]
    files.sort(key=os.path.getctime, reverse=True)
    latest_file = files[0] if files else None
    assert latest_file is not None, f"{file_name}.{file_type} file not download!"
    file_name = os.path.basename(latest_file)
    base_page.logger.info(f"✅ Loaded filename: {file_name}")