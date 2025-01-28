class AutoTestError(Exception):
    """Asosiy xatolik klassi"""
    pass


class PageLoadError(AutoTestError):
    """Sahifa yuklanish xatosi"""
    pass


class ElementNotFoundError(AutoTestError):
    """Element topilmadi xatosi"""
    pass


class LoginError(AutoTestError):
    """Login jarayoni xatosi"""
    pass


class SessionError(AutoTestError):
    """Session bilan bog'liq xatolik"""
    pass
