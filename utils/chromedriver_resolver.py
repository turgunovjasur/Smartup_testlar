import os
from pathlib import Path

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def _find_cached_chromedriver():
    cache_root = Path.home() / ".wdm" / "drivers" / "chromedriver"
    if not cache_root.exists():
        return None

    candidates = []
    for candidate in cache_root.rglob("chromedriver"):
        if candidate.is_file() and os.access(candidate, os.X_OK):
            candidates.append(candidate)

    if not candidates:
        return None

    return str(max(candidates, key=lambda path: path.stat().st_mtime))


def create_chrome_driver(options, logger):
    # Avval cache'dagi driver sinab ko'riladi; u bo'lmasa yoki mos kelmasa,
    # faqat shundan keyin online install fallback ishlatiladi.
    cached_driver_path = _find_cached_chromedriver()
    if cached_driver_path:
        logger.debug(f"Local cached ChromeDriver topildi: {cached_driver_path}")
        try:
            driver = webdriver.Chrome(
                service=ChromeService(cached_driver_path),
                options=options,
            )
            return driver, cached_driver_path, "cache"
        except WebDriverException as e:
            logger.warning(
                "Local cached ChromeDriver ishga tushmadi, online fallback ishlatiladi: "
                f"{e}"
            )

    driver_path = ChromeDriverManager().install()
    logger.debug(f"ChromeDriver online o'rnatildi: {driver_path}")
    driver = webdriver.Chrome(service=ChromeService(driver_path), options=options)
    return driver, driver_path, "online"
