import logging
import time
import traceback
from functools import wraps
from typing import Optional

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotVisibleException,
    ElementNotInteractableException,
    InvalidElementStateException,
    WebDriverException
)

logger = logging.getLogger(__name__)


class WebDriverError(Exception):
    def __init__(self, message, original_error=None):
        self.message = message
        self.original_error = original_error
        self.traceback = traceback.extract_tb(original_error.__traceback__) if original_error else None
        super().__init__(self.message)

    def get_full_trace(self):
        if self.traceback:
            return "".join(traceback.format_list(self.traceback))
        return ""


SELENIUM_EXCEPTIONS = {
    TimeoutException: "Element kutish vaqti tugadi",
    NoSuchElementException: "Element topilmadi",
    StaleElementReferenceException: "Element eskirgan",
    ElementClickInterceptedException: "Element ustida boshqa element bor",
    ElementNotVisibleException: "Element ko'rinmas holatda",
    ElementNotInteractableException: "Element bilan ishlab bo'lmaydi",
    InvalidElementStateException: "Element holati noto'g'ri",
    WebDriverException: "WebDriver xatoligi"
}


def handle_selenium_error(take_screenshot=False):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)

            except Exception as e:
                # Xatolik turini aniqlash
                error_type = type(e)
                error_msg = SELENIUM_EXCEPTIONS.get(error_type, "Kutilmagan xatolik")

                # Xatolik kelib chiqqan funksiya nomini olish
                failing_function = func.__name__

                # Stacktrace orqali qaysi yordamchi funksiya xato berganini aniqlash
                tb = traceback.extract_tb(e.__traceback__)
                helper_function = None
                for frame in tb:
                    if frame.name.startswith('_wait_'):
                        helper_function = frame.name
                        break

                # To'liq xatolik xabarini shakllantirish
                detailed_error = f"{error_msg} in {failing_function}"
                if helper_function:
                    detailed_error += f" (yordamchi funksiya: {helper_function})"
                detailed_error += f": {str(e)}"

                # Screenshot
                if take_screenshot and hasattr(self, 'take_screenshot'):
                    self.take_screenshot(f"{func.__name__}_error")

                # Xatolikni qayta ko'tarish
                raise WebDriverError(detailed_error, original_error=e)

        return wrapper

    return decorator


def handle_with_retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    last_error = e
                    self.logger.warning(
                        f"⚠️ {func.__name__}: Urinish {attempt + 1}/{max_attempts} muvaffaqiyatsiz: {str(e)}"
                    )
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                        self.logger.info(f"🔄 {func.__name__}: Qayta urinish {attempt + 2}/{max_attempts}")
                    else:
                        raise last_error
        return wrapper
    return decorator