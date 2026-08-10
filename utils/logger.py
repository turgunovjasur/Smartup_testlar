import os
import inspect
import logging
from contextvars import ContextVar
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

_ACTIVE_TEST_NAME = ContextVar("active_test_name", default=None)
_ACTIVE_LOG_RUN_DIR = None


def set_active_test_name(test_name):
    """Joriy test uchun yagona log kontekstini o'rnatish."""
    return _ACTIVE_TEST_NAME.set(test_name)


def reset_active_test_name(token):
    """Avvalgi log kontekstiga qaytish."""
    _ACTIVE_TEST_NAME.reset(token)


def get_active_test_name():
    """Agar tashqaridan o'rnatilgan bo'lsa, joriy test nomini qaytaradi."""
    return _ACTIVE_TEST_NAME.get()


def build_log_run_timestamp():
    """Joriy test run uchun katalog nomi."""
    return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")


def set_active_log_run_dir(run_dir):
    """Barcha loglar yoziladigan joriy run katalogini o'rnatish."""
    global _ACTIVE_LOG_RUN_DIR
    _ACTIVE_LOG_RUN_DIR = run_dir


def get_active_log_run_dir():
    """Joriy run katalogini olish."""
    return _ACTIVE_LOG_RUN_DIR


def ensure_active_log_run_dir():
    """Barcha artefaktlar saqlanadigan joriy run katalogini qaytaradi."""
    run_dir = get_active_log_run_dir()
    if not run_dir:
        run_dir = os.path.abspath(os.path.join("test_runs", build_log_run_timestamp()))
        set_active_log_run_dir(run_dir)
    os.makedirs(run_dir, exist_ok=True)
    return run_dir


def resolve_request_test_name(request):
    """
    Pytest request'dan haqiqiy test nomini olish.

    `test_ui_runner.py` dagi parametrik wrapper uchun `runner_case["func"].__name__`
    ishlatiladi, shunda driver va yordamchi fixture'lar ham shu faylga yozadi.
    """
    if "runner_case" in getattr(request, "fixturenames", []):
        runner_case = request.getfixturevalue("runner_case")
        if isinstance(runner_case, dict):
            func = runner_case.get("func")
            if callable(func):
                return func.__name__

    return request.node.name


def get_test_name():
    """Test nomini avtomatik aniqlash: funksiyaning yoki sinfning nomini topish."""
    active_test_name = get_active_test_name()
    if active_test_name:
        return active_test_name

    stack = inspect.stack()
    for frame in stack:
        # Test funksiyasi "test_" bilan boshlanadi
        if frame.function.startswith("test"):
            return frame.function
    return "unknown_test"


def configure_logging(test_name):
    """
    Logging konfiguratsiyasi: loglarni yagona faylga yozish
    va test nomi bilan ajratib ko'rsatish.

    Args:
        test_name (str): Test nomi, loglar uchun identifikator sifatida ishlatiladi

    Returns:
        logging.Logger: Sozlangan logger obyekti
    """
    active_test_name = get_active_test_name()
    log_target_name = active_test_name or test_name
    run_dir = ensure_active_log_run_dir()

    log_dir = os.path.join(run_dir, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Har run uchun alohida papka ichida test logi
    log_file_name = os.path.join(log_dir, f"{log_target_name}.log")

    # Logger yaratish
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)

    # Eski handlerlarni tozalash
    if logger.hasHandlers():
        logger.handlers.clear()

    # Log format: test nomini kiritish
    log_format = f"%(asctime)s - [%(levelname)s] - {test_name} - %(message)s"

    # Rangli konsol handler
    class ColorFormatter(logging.Formatter):
        def format(self, record):
            log_message = super().format(record)
            if record.levelno == logging.INFO:
                return f"{Fore.GREEN}{log_message}{Style.RESET_ALL}"
            elif record.levelno == logging.WARNING:
                return f"{Fore.YELLOW}{log_message}{Style.RESET_ALL}"
            elif record.levelno == logging.ERROR:
                return f"{Fore.RED}{log_message}{Style.RESET_ALL}"
            elif record.levelno == logging.DEBUG:
                return f"\033[38;2;160;160;160m{log_message}{Style.RESET_ALL}"
            return log_message

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = ColorFormatter(log_format)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(log_file_name, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(log_format)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Avoid propagating logs to the root logger
    logger.propagate = False

    return logger
