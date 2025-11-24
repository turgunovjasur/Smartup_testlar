"""
Test sozlamalari - markaziy konfiguratsiya fayli.

Bu faylda barcha timeout'lar, URL'lar va boshqa sozlamalar saqlanadi.
Har bir sozlamani o'zgartirish uchun faqat shu faylni tahrirlash kifoya.
"""

class WaitTimeouts:
    """Element kutish vaqtlari (soniyalarda)."""

    DEFAULT_TIMEOUT = 30
    UI_PAGE_LOADER_TIMEOUT = 60  # Sahifa to'liq yuklanishi

    FILE_DOWNLOAD_TIMEOUT = 30
