class ElementInteractionError(Exception):
    def __init__(self, message, locator=None, original_error=None, context=None):
        self.message = message
        self.locator = locator
        self.original_error = original_error
        self.context = context or {}
        super().__init__(message)

    def __str__(self):
        parts = [self.message]

        # locator=BY=selector ko'rinishi
        if self.locator:
            try:
                by, sel = self.locator
                by_name = getattr(by, "name", None) or getattr(by, "__name__", None) or str(by)
                parts.append("locator=%s=%s" % (by_name, sel))
            except Exception:
                parts.append("locator=%s" % (self.locator,))

        # foydali kontekstlar
        page = self.context.get("page")
        url = self.context.get("url")
        caller = self.context.get("caller")
        step = self.context.get("step")

        if page:   parts.append("page=%s" % page)
        if url:    parts.append("url=%s" % url)
        if caller: parts.append("caller=%s" % caller)
        if step:   parts.append("step=%s" % step)

        if self.original_error:
            parts.append("root=%s" % self.original_error.__class__.__name__)

        return " | ".join(parts)


class ElementNotFoundError(ElementInteractionError):
    """Element DOM'da topilmadi (presence yo'q)."""
    pass

class ElementVisibilityError(ElementInteractionError):
    """Element ko'rinmadi (visibility yo'q)."""
    pass

class ElementNotClickableError(ElementInteractionError):
    """Elementni bosib bo'lmadi (intercepted/overlay/disabled va h.k.)."""
    pass

class ElementStaleError(ElementInteractionError):
    """Element stale bo'lib qoldi (DOM yangilangan)."""
    pass

class ScrollError(ElementInteractionError):
    """Scroll qilish paytida xato."""
    pass

class LoaderTimeoutError(ElementInteractionError):
    """Sahifa/loader tugamadi (timeout)."""
    pass

class JavaScriptError(ElementInteractionError):
    """JavaScript bajarilishida xato."""
    pass

class ElementTimeoutError(ElementInteractionError):
    """Umumiy timeout (element bilan ishlashda vaqt tugadi)."""
    pass
