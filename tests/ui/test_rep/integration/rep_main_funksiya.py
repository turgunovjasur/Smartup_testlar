import os
import time
from datetime import datetime

DOWNLOAD_DIR = os.path.join(os.environ["USERPROFILE"], "Downloads")

def generate_and_verify_download(base_page, before_files, expected_name, file_type="zip", timeout=30, stable_seconds=3):
    """
    Yangi yuklangan faylni topadi va hajmi `stable_seconds` davomida o‘zgarmasligini kutadi.
    .crdownload → final fayl o'tishini ham kuzatadi.
    """
    final_ext = f".{file_type}"
    elapsed = 0
    stable_counter = 0
    last_size = None
    candidate_file = None

    base_page.logger.info(f"⏳ Yangi fayl kutilyapti: {expected_name}{final_ext} (timeout: {timeout}s)")
    base_page.logger.debug(f"📂 Avvalgi fayllar: {before_files}")

    while elapsed < timeout:
        current_files = set(os.listdir(DOWNLOAD_DIR))
        new_files = current_files - before_files

        if new_files:
            for fname in sorted(new_files):
                if not fname.startswith(expected_name):
                    continue

                full_path = os.path.join(DOWNLOAD_DIR, fname)

                # 1️⃣ Yuklanayotgan fayl (.crdownload)
                if fname.endswith(".crdownload"):
                    candidate_file = fname
                    base_page.logger.debug(f"[{elapsed+1}s] ⌛ Yuklanmoqda: {fname}")
                    break

                # 2️⃣ Tugagan fayl (.zip)
                elif fname.endswith(final_ext) and os.path.exists(full_path):
                    size = os.path.getsize(full_path)
                    mtime = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime('%H:%M:%S')

                    # Stable counter
                    if last_size == size:
                        stable_counter += 1
                    else:
                        stable_counter = 1
                    last_size = size

                    base_page.logger.debug(
                        f"[{elapsed+1}s] 📏 {fname} | {size}B | 🕒 {mtime} | Stable: {stable_counter}/{stable_seconds}"
                    )

                    if stable_counter >= stable_seconds and size > 0:
                        base_page.logger.info(f"✅ Fayl tayyor: {fname} ({size}B)")
                        return full_path

        # 3️⃣ Agar .crdownload yo‘qolib final fayl paydo bo‘lsa
        if candidate_file:
            cr_path = os.path.join(DOWNLOAD_DIR, candidate_file)
            final_path = os.path.join(DOWNLOAD_DIR, candidate_file.replace(".crdownload", final_ext))

            if not os.path.exists(cr_path) and os.path.exists(final_path):
                size = os.path.getsize(final_path)
                mtime = datetime.fromtimestamp(os.path.getmtime(final_path)).strftime('%H:%M:%S')

                if last_size == size:
                    stable_counter += 1
                else:
                    stable_counter = 1
                last_size = size

                base_page.logger.debug(
                    f"[{elapsed+1}s] 📏 {os.path.basename(final_path)} | {size}B | 🕒 {mtime} | Stable: {stable_counter}/{stable_seconds}"
                )

                if stable_counter >= stable_seconds and size > 0:
                    base_page.logger.info(f"✅ Yuklash tugadi: {os.path.basename(final_path)} ({size}B)")
                    return final_path

        time.sleep(1)
        elapsed += 1

    raise FileNotFoundError(f"❌ {timeout}s ichida '{expected_name}{final_ext}' yuklanmadi!")


def clear_old_download(base_page, expected_name, file_type="zip"):
    """
    Yuklashdan oldin eski fayllarni o‘chiradi.
    """
    removed_files = []
    for f in os.listdir(DOWNLOAD_DIR):
        if f.startswith(expected_name) and f.endswith(f".{file_type}"):
            try:
                os.remove(os.path.join(DOWNLOAD_DIR, f))
                removed_files.append(f)
            except Exception as e:
                base_page.logger.warning(f"⚠️ Faylni o‘chirishda xato: {f} - {e}")

    if removed_files:
        base_page.logger.info(f"O‘chirildi: {', '.join(removed_files)}")
    else:
        base_page.logger.info(f"O‘chirish uchun mos fayl topilmadi: {expected_name}*.{file_type}")

# import os
# import random
# import time
# from pages.core.md.base_page import BasePage
# import pyperclip
#

# def wait_for_file_dialog_focus(test_text="check_test", timeout=10):
#     """
#     Save As oynasi ochilib, fayl nomi inputiga yozilgan matn clipboard orqali tasdiqlanadi.
#     Modal ochilmaguncha hech narsa yozilmaydi.
#     """
#     elapsed = 0
#     while elapsed < timeout:
#         time.sleep(5)
#         import pyautogui
#
#         pyautogui.hotkey('ctrl', 'a')
#         time.sleep(0.1)
#         pyautogui.press('delete')
#         time.sleep(0.2)
#
#         pyautogui.write(test_text, interval=0.05)
#         time.sleep(0.2)
#
#         pyautogui.hotkey('ctrl', 'a')
#         time.sleep(0.1)
#         pyautogui.hotkey('ctrl', 'c')
#         time.sleep(0.2)
#
#         pasted = pyperclip.paste().strip()
#
#         if pasted == test_text:
#             pyautogui.hotkey('ctrl', 'a')
#             time.sleep(0.1)
#             pyautogui.press('delete')
#             return True
#
#         pyautogui.hotkey('ctrl', 'a')
#         pyautogui.press('delete')
#         time.sleep(0.5)
#         elapsed += 0.5
#
#     raise TimeoutError("Modal hali ochilmagan bo'lishi mumkin.")
#
#
# def generate_and_verify_download(driver, file_name, file_type):
#     base_page = BasePage(driver)
#
#     file_name = f'{file_name}_{random.randint(10000, 99999)}'
#
#     base_page.logger.info("⏳ Save As oynasiga fokus kutilyapti...")
#     wait_for_file_dialog_focus()
#
#     time.sleep(1)
#     import pyautogui
#
#     pyautogui.write(file_name, interval=0.2)
#     base_page.logger.info(f"File name kiritildi: {file_name}")
#
#     time.sleep(2)
#     pyautogui.press('enter')
#     base_page.logger.info("Enter bosildi!")
#
#     downloads_path = os.path.join(os.environ["USERPROFILE"], "Downloads")
#     timeout = 20
#     poll_interval = 1
#     elapsed = 0
#
#     latest_file = None
#     while elapsed < timeout:
#         matching_files = [f for f in os.listdir(downloads_path)
#                           if f.endswith(f"{file_name}.{file_type}")]
#         if matching_files:
#             latest_file = os.path.join(downloads_path, matching_files[0])
#             if os.path.exists(latest_file) and os.path.getsize(latest_file) > 0:
#                 break
#         time.sleep(poll_interval)
#         elapsed += poll_interval
#
#     assert latest_file is not None, f"{file_name}.{file_type} file not downloaded!"
#     base_page.logger.info(f"✅ Loaded filename: {os.path.basename(latest_file)}")