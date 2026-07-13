import os
from dotenv import find_dotenv, load_dotenv

_DOTENV_PATH = find_dotenv(usecwd=True)
load_dotenv(_DOTENV_PATH or None)  # .env faylni avtomatik yuklaydi (faqat bir marta)


def get_env(var_name, default=None):
    return os.getenv(var_name, default)


def get_dotenv_path():
    """Yuklangan .env fayl yo'lini qaytaradi."""
    return _DOTENV_PATH or None
