import os
import time
import shutil
import tempfile
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from tests.ui.test_rep.integration.rep_main_funksiya import DOWNLOAD_DIR
from utils.logger import configure_logging


def create_driver(test_name, test_data):
    """Yangi driver yaratish (eski fixture logikasiga o'xshash, lekin request o'rniga test_name)."""
    logger = configure_logging(test_name)

    logger.info("=" * 80)
    logger.info(f"DRIVER YARATISH BOSHLANDI: {test_name}")
    logger.info("=" * 80)

    start_time = time.time()
    drv = None
    user_data_dir = None

    try:
        # Test ma'lumotlarini olish
        data = test_data["data"]
        url = data["url"]
        logger.info(f"Test URL: {url}")

        # ChromeDriver o'rnatish
        driver_path = ChromeDriverManager().install()
        service = ChromeService(driver_path)
        logger.debug(f"ChromeDriver o'rnatildi: {driver_path}")

        # Headless rejim - faqat environment variable orqali
        headless = os.getenv("GITHUB_ACTIONS") == "true"
        if headless:
            logger.info("Headless rejim yoqildi")
        else:
            logger.info("Normal rejim (GUI)")

        # Chrome options sozlash
        options = Options()

        if headless:
            options.add_argument("--headless=new")

        # Vaqtinchalik profil yaratish
        user_data_dir = tempfile.mkdtemp()
        logger.debug(f"Vaqtinchalik profil yaratildi: {user_data_dir}")
        options.add_argument(f"--user-data-dir={user_data_dir}")

        # Barcha argumentlarni qo'shish
        options.add_argument("--start-maximized")
        options.add_argument("--force-device-scale-factor=0.90")
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--incognito")
        options.add_argument("--disable-features=AutofillServerCommunication,PasswordManagerEnabled,PasswordCheck")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # Preferences sozlash
        all_prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "download.default_directory": DOWNLOAD_DIR,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", all_prefs)
        logger.debug(f"Yuklab olish katalogi: {DOWNLOAD_DIR}")

        # Chrome driver yaratish
        drv = webdriver.Chrome(service=service, options=options)
        logger.info(f"Browser ishga tushdi. Session ID: {drv.session_id}")

        # CDP orqali fayl yuklash sozlamalari
        try:
            drv.execute_cdp_cmd(
                "Page.setDownloadBehavior",
                {"behavior": "allow", "downloadPath": DOWNLOAD_DIR}
            )
        except Exception as e:
            logger.warning(f"CDP sozlashda xatolik: {e}")

        # Timeout sozlash
        drv.set_page_load_timeout(120)

        # URL ochish
        logger.info(f"URL ochilmoqda: {url}")
        drv.get(url)

        setup_time = time.time() - start_time
        logger.info("=" * 80)
        logger.info(f"DRIVER TAYYOR! Setup vaqti: {setup_time:.2f} sekund")
        logger.info("=" * 80)

        return drv, user_data_dir, start_time

    except WebDriverException as e:
        logger.error("=" * 80)
        logger.error(f"WEBDRIVER XATOLIK: {e}")
        logger.error("=" * 80)
        raise
    except Exception as e:
        logger.error("=" * 80)
        logger.error(f"KUTILMAGAN XATOLIK: {e}")
        logger.error("=" * 80)
        raise


def cleanup_driver(drv, user_data_dir, logger, start_time, test_name):
    """Driver ni tozalash."""
    if drv:
        try:
            drv.quit()
            logger.info("Browser yopildi")
        except Exception as e:
            logger.warning(f"Browser yopishda xatolik: {e}")
    else:
        logger.warning("Driver yaratilmagan edi")

    if user_data_dir:
        try:
            shutil.rmtree(user_data_dir)
            logger.info("Vaqtinchalik profil o'chirildi")
        except Exception as e:
            logger.warning(f"Profil o'chirishda xatolik: {user_data_dir} - {e}")

    total_time = time.time() - start_time
    logger.info("=" * 80)
    logger.info(f"DRIVER SESSION TUGADI. Umumiy vaqt: {total_time:.2f} sekund")
    logger.info("=" * 80)