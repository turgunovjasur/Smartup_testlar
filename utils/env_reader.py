import os
from dotenv import load_dotenv

load_dotenv()  # .env faylni avtomatik yuklaydi (faqat bir marta)

def get_env(var_name, default=None):
    return os.getenv(var_name, default)
