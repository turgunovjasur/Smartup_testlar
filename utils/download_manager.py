import os
import time
from datetime import datetime
from config.test_settings import WaitTimeouts

DOWNLOAD_DIR = os.path.join(os.environ["USERPROFILE"], "Downloads")

# ======================================================================================================================

def generate_and_verify_download(
        base_page,
        before_files,
        expected_name,
        file_type="zip",
        timeout=WaitTimeouts.FILE_DOWNLOAD_TIMEOUT,
        stable_seconds=3
):
    """
    Yangi yuklangan faylni topadi va hajmi `stable_seconds` davomida o'zgarmasligini kutadi.
    .crdownload → final fayl o'tishini ham kuzatadi.

    Args:
        base_page: Logger mavjud bo'lgan sahifa obyekti
        before_files: Yuklashdan oldingi fayllar to'plami
        expected_name: Kutilayotgan fayl nomi (kengaytmasiz)
        file_type: Fayl kengaytmasi (default: "zip")
        timeout: Maksimal kutish vaqti (soniyalarda)
        stable_seconds: Hajm barqaror turishi kerak bo'lgan vaqt

    Returns:
        str: Yuklangan faylning to'liq yo'li

    Raises:
        FileNotFoundError: Agar timeout ichida fayl yuklanmasa
    """
    final_ext = f".{file_type}"
    crdownload_ext = ".crdownload"

    start_time = time.time()
    stable_counter = 0
    last_size = None
    last_checked_file = None

    base_page.logger.info(
        f"⏳ Yangi fayl kutilyapti: {expected_name}{final_ext} "
        f"(timeout: {timeout}s, stable: {stable_seconds}s)"
    )

    while time.time() - start_time < timeout:
        elapsed = int(time.time() - start_time)

        try:
            current_files = set(os.listdir(DOWNLOAD_DIR))
        except Exception as e:
            base_page.logger.warning(f"⚠️ Downloads papkasini o'qishda xato: {e}")
            time.sleep(1)
            continue

        # Faqat expected_name bilan boshlangan yangi fayllarni topish
        new_files = current_files - before_files
        matching_files = [
            f for f in new_files
            if f.startswith(expected_name) and
               (f.endswith(final_ext) or f.endswith(crdownload_ext))
        ]

        if not matching_files:
            # Hali fayl paydo bo'lmagan
            if elapsed % 5 == 0 and elapsed > 0:  # Har 5 soniyada log
                base_page.logger.debug(f"[{elapsed}s] ⏳ Yuklash boshlanishini kutmoqda...")
            time.sleep(1)
            continue

        # Eng yangi faylni tanlash (agar bir nechta bo'lsa)
        matching_files.sort(
            key=lambda f: os.path.getmtime(os.path.join(DOWNLOAD_DIR, f)),
            reverse=True
        )
        current_file = matching_files[0]
        file_path = os.path.join(DOWNLOAD_DIR, current_file)

        # .crdownload fayl hali yuklanmoqda
        if current_file.endswith(crdownload_ext):
            last_checked_file = current_file
            stable_counter = 0
            last_size = None

            if elapsed % 5 == 0:  # Har 5 soniyada log
                try:
                    size = os.path.getsize(file_path)
                    base_page.logger.debug(
                        f"[{elapsed}s] ⏛ Yuklanmoqda: {current_file} ({size:,} bytes)"
                    )
                except:
                    base_page.logger.debug(f"[{elapsed}s] ⏛ Yuklanmoqda: {current_file}")

            time.sleep(1)
            continue

        # Final fayl (.zip, .pdf, etc.)
        if current_file.endswith(final_ext):
            if not os.path.exists(file_path):
                base_page.logger.warning(f"⚠️ Fayl topilmadi: {current_file}")
                time.sleep(1)
                continue

            try:
                current_size = os.path.getsize(file_path)
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%H:%M:%S')
            except Exception as e:
                base_page.logger.warning(f"⚠️ Fayl ma'lumotlarini o'qishda xato: {e}")
                time.sleep(1)
                continue

            # Bo'sh faylni qabul qilmaslik
            if current_size == 0:
                base_page.logger.debug(f"[{elapsed}s] ⚠️ Fayl bo'sh: {current_file}")
                time.sleep(1)
                continue

            # Hajm barqarorligini tekshirish
            if last_size == current_size and last_checked_file == current_file:
                stable_counter += 1
            else:
                stable_counter = 0
                last_size = current_size
                last_checked_file = current_file

            base_page.logger.debug(
                f"[{elapsed}s] 📄 {current_file} | {current_size:,} bytes | "
                f"🕐 {mtime} | Barqaror: {stable_counter}/{stable_seconds}s"
            )

            # Hajm stable_seconds davomida o'zgarmagan
            if stable_counter >= stable_seconds:
                base_page.logger.info(
                    f"✅ Fayl tayyor: {current_file} ({current_size:,} bytes)"
                )
                return file_path

        time.sleep(1)

    # Timeout
    raise FileNotFoundError(
        f"❌ {timeout}s ichida '{expected_name}{final_ext}' yuklanmadi yoki barqarorlanmadi!"
    )

# ======================================================================================================================

def clear_old_download(base_page, expected_name, file_type="zip"):
    """
    Yuklashdan oldin eski fayllarni o'chiradi.

    Args:
        base_page: Logger mavjud bo'lgan sahifa obyekti
        expected_name: O'chiriladigan fayl nomi (kengaytmasiz)
        file_type: Fayl kengaytmasi (default: "zip")
    """
    pattern_ext = f".{file_type}"
    removed_files = []
    failed_files = []

    try:
        files = os.listdir(DOWNLOAD_DIR)
    except Exception as e:
        base_page.logger.error(f"❌ Downloads papkasini o'qib bo'lmadi: {e}")
        return

    for filename in files:
        # expected_name bilan boshlanib, kerakli kengaytma bilan tugagan fayllar
        if filename.startswith(expected_name) and filename.endswith(pattern_ext):
            file_path = os.path.join(DOWNLOAD_DIR, filename)  # ✅ To'g'rilandi

            try:
                os.remove(file_path)
                removed_files.append(filename)
                base_page.logger.debug(f"🗑️ O'chirildi: {filename}")
            except PermissionError:
                failed_files.append((filename, "Fayl ochiq yoki foydalanilmoqda"))
                base_page.logger.warning(
                    f"⚠️ Faylni o'chirib bo'lmadi (ochiq): {filename}"
                )
            except Exception as e:
                failed_files.append((filename, str(e)))
                base_page.logger.warning(
                    f"⚠️ Faylni o'chirishda xato: {filename} - {e}"
                )

    # Natija hisoboti
    if removed_files:
        base_page.logger.info(
            f"✅ O'chirildi ({len(removed_files)}): {', '.join(removed_files)}"
        )

    if failed_files:
        base_page.logger.warning(
            f"⚠️ O'chirilmadi ({len(failed_files)}): "
            f"{', '.join([f[0] for f in failed_files])}"
        )

    if not removed_files and not failed_files:
        base_page.logger.info(
            f"ℹ️ O'chirish uchun mos fayl topilmadi: {expected_name}*{pattern_ext}"
        )

# ======================================================================================================================
