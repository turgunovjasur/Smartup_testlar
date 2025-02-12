import os
import inspect
import logging
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)


def get_test_name():
    """Test nomini avtomatik aniqlash: funksiyaning yoki sinfning nomini topish."""

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
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Log faylining yagona nomi
    log_file_name = f"{log_dir}/{test_name}_{datetime.now().strftime('%Y_%m_%d')}.log"

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
                return f"{Fore.CYAN}{log_message}{Style.RESET_ALL}"
            return log_message

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
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
