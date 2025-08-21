class ElementInteractionError(Exception):
    """Asosiy xatolik klassi"""

    def __init__(self, message, locator=None, original_error=None):
        self.message = message
        self.locator = locator
        self.original_error = original_error
        super().__init__(self.message)


class ElementNotFoundError(ElementInteractionError):
    """Element topilmaganda"""

    def __init__(self, message="Element topilmadi", locator=None, original_error=None):
        super().__init__(message, locator, original_error)


class ElementStaleError(ElementInteractionError):
    """Element yangilanganda"""

    def __init__(self, message="Element yangilandi", locator=None, original_error=None):
        super().__init__(message, locator, original_error)


class ElementNotClickableError(ElementInteractionError):
    """Element bosilmaydigan holatda"""

    def __init__(self, message="Element bosilmaydigan holatda", locator=None, original_error=None):
        super().__init__(message, locator, original_error)


class ElementVisibilityError(ElementInteractionError):
    """Element ko'rinish holati bilan bog'liq xatolik"""

    def __init__(self, message="Element ko'rinish holati kutilganidek emas", locator=None, original_error=None):
        super().__init__(message, locator, original_error)


class ScrollError(ElementInteractionError):
    """Scroll qilish xatoligi"""

    def __init__(self, message="Scroll qilib bo'lmadi", locator=None, original_error=None):
        super().__init__(message, locator, original_error)


class LoaderTimeoutError(ElementInteractionError):
    """Sahifa yuklanish xatoligi"""

    def __init__(self, message="Sahifa yuklanmadi", locator=None, original_error=None):
        super().__init__(message, locator, original_error)


class JavaScriptError(ElementInteractionError):
    """JavaScript bajarilishi bilan bog'liq xatolik"""

    def __init__(self, message="JavaScript ishlatilganda xatolik yuz berdi", locator=None, original_error=None):
        super().__init__(message, locator, original_error)
